import requests
import json
import os
from Recipe import Recipe


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

    if not event.recipes:
        print("No saved recipes")
        return

    # I think we will eventually need to make a class for recipes
    # and each recipe will have it's own display function
    # then we can loop through displays recipes here and display
    # FOR NOW, not a priority!!
    return


def list_all_events(state):
    """
    Displays information for all events

    Args:
        state: Global state
    """
    print("==== ALL EVENTS ====")
    for event in state.events.values():
        event.display()
        print("")  # create newline

    return


def generate_recipes(state):
    """
    Generates recipes using Spoonacular's API for the current_event.

    Args:
        state: Global state
    """
    event = state.current_event
    if event == None:
        print("No event selected.")
        return

    # GET https://api.spoonacular.com/recipes/complexSearch/

    # output should be a print statement of the recipes
    
    main_url = event.generate_recipe_search_url(state, "main course")
    appetizer_url = event.generate_recipe_search_url(state, "appetizer")
    dessert_url = event.generate_recipe_search_url(state, "dessert")
    categories = {
        "main course": main_url,
        "appetizer": appetizer_url,
        "dessert": dessert_url,
    }

    recipes = {
        "main course": {},
        "appetizer": {},
        "dessert": {}
    }

    for category, url in categories.items():
        response = requests.get(url)
        data = response.json()
        for recipe in data["results"]:
            rid = recipe["id"]
            ingreds = get_recipe_ingredients(state, rid)
            recipes[category][rid] = Recipe(recipe["title"], ingreds, rid)

    print("!!! main course !!!")
    for recipe in recipes["main course"].values():
        recipe.display()

    print("!!! appetizah !!!")
    for recipe in recipes["appetizer"].values():
        recipe.display()

    print("!!! dessert !!!")
    for recipe in recipes["dessert"].values():
        recipe.display()


def get_recipe_ingredients(state, recipeid):
    url = f"https://api.spoonacular.com/recipes/{recipeid}/ingredientWidget.json?apiKey={state.spoonacular_key}"

    response = requests.get(url)
    data = response.json()

    ingredients = []

    for ingredient in data["ingredients"]:
        ingredients.append(ingredient["name"])

    return ingredients