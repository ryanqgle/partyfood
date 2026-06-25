from Recipe import Recipe
from google import genai
from google.genai import types
import requests
import json
import os
import sqlalchemy as db


def set_event_name(state):
    """
    Changes the name of the current_event
    based on user input.

    Args:
        state: Global state
    """
    name = input("Event Name: ")
    state.current_event.set_name(name)


def set_event_attendees(state):
    """
    Sets attendee count of the current_event
    to amount specified based on user input.
    Args:
        state: Global state
    """
    count = int(input("Number of attendees: "))
    if not isinstance(count, int):
        print("Invalid input. Type in a number.")

    state.current_event.update_attendees(count)


def set_event_ingredients(state, mode):
    """
    Args:
        state: Global state
        mode: Add (0) or Remove (1)
    """
    ing_raw = input("Available ingredients (comma separated): ")
    state.current_event.modify_ingredients(ing_raw, mode)


def view_recipes(state):
    """
    Prints recipes for one event

    Args:
        state: Global state
    """
    event = state.current_event

    if not event.saved_recipes:
        print("No saved recipes")
        return

    # I think we will eventually need to make a class for recipes
    # and each recipe will have it's own display function
    # then we can loop through displays recipes here and display
    # FOR NOW, not a priority!!

    for recipe in event.saved_recipes:
        recipe.display()
        print("")


def list_all_events(state):
    """
    Displays information for all events

    Args:
        state: Global state
    """
    print("==== ALL EVENTS ====")
    for event in state.events.values():
        event.display()
        print("")

    return


def generate_recipes(state):
    """
    Generates recipes using Spoonacular's API for the current_event based on
    the diets and intolerances associated with the event.

    Args:
        state: Global state
    """
    event = state.current_event
    if event is None:
        print("No event selected.")
        return

    # GET https://api.spoonacular.com/recipes/complexSearch/

    # output should be a print statement of the recipes

    main_url = event.generate_recipe_search_url(state, "main course")
    # appetizer_url = event.generate_recipe_search_url(state, "appetizer")
    # dessert_url = event.generate_recipe_search_url(state, "dessert")
    categories = {
        "main course": main_url,
        # "appetizer": appetizer_url,
        # "dessert": dessert_url,
    }

    recipes = {
        "main course": {},
        "appetizer": {},
        "dessert": {}
    }

    for category, url in categories.items():
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Failed to get recipes")
            print("Status code: " + str(response.status_code))
            return

        data = response.json()
        for recipe in data["results"]:
            rid = recipe["id"]
            ingreds = get_recipe_ingredients(state, rid)
            recipes[category][rid] = Recipe(recipe["title"], ingreds, rid)

    print("!!! MAIN COURSES !!!")
    for recipe in recipes["main course"].values():
        recipe.display()
    print("")

    # print("!!! APPETIZERS !!!")
    # for recipe in recipes["appetizer"].values():
    #     recipe.display()
    # print("")

    # print("!!! DESSERTS !!!")
    # for recipe in recipes["dessert"].values():
    #     recipe.display()
    # print("")

    for category in recipes:
        for recipe in recipes[category].values():
            state.current_event.add_recipe(
                recipe,
                category=category,
                estimated_cost=None
            )


def get_recipe_ingredients(state, recipeid):
    """
    Uses Spoonacular API call to fetch the ingredients of a single
    recipe.

    Args:
        state: Global state
        recipeid: The ID associated with a recipe.
    """
    url = (f"https://api.spoonacular.com/recipes/" +
           f"{recipeid}/ingredientWidget.json?"
           + f"apiKey={state.spoonacular_key}")

    response = requests.get(url)

    if response.status_code != 200:
        print(f"Failed for recipe {recipeid}")
        print("Status code: " + str(response.status_code))
        return []

    data = response.json()
    ingredients = []

    for ingredient in data["ingredients"]:
        ingredients.append(ingredient["name"])

    return ingredients


def estimate_recipe_cost(state):
    """
    Uses Gemini API call to estimate the cost of all recipes affiliated
    with the current event and provide a breakdown based on ingredient.

    Args:
        state: Global state
    """
    attendees = state.current_event.attendee_count
    recipes = state.current_event.saved_recipes
    recipe_text = ""

    for recipe in recipes:
        recipe_text += f"""
        Recipe: {recipe.name}
        Ingredients: {', '.join(recipe.ingredients)}
        """

    client = genai.Client(api_key=state.gemini_key)

    prompt = f"""
    Estimate the grocery cost for preparing this recipe for {attendees}
    people in the United states.
    Assume average supermarket prices

    Recipes:
    {recipe_text}

    Requirements:
    - Estimate the cost of each ingredient.
    - Show the subtotal for each recipe.
    - Show a reasonable price range for each recipe.
    - Show a grand total range for all recipes combined.
    - Do not explain your reasoning.
    - Do not include introductions or conclusions.
    - Format exactly like:

    Recipe: <recipe name>
    Ingredient costs:
    - ingredient: $x-$y
    - ingredient: $x-$y
    Recipe total: $x-$y

    Recipe: <recipe name>
    ...

    Grand Total: $x-$y
    """

    response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
                )

    print(response.text)
