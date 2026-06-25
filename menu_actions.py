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
    if not state_event_error_handler(state):
        return

    name = input("Event Name: ")
    state.current_event.set_name(name)


def set_event_attendees(state):
    """
    Sets attendee count of the current_event
    to amount specified based on user input.
    Args:
        state: Global state
    """
    if not state_event_error_handler(state):
        return

    try:
        count = int(input("Number of attendees: "))
        state.current_event.update_attendees(count)
    except ValueError:
        print("Invalid input. Type a whole number.")
        return


def set_event_ingredients(state, mode):
    """
    Args:
        state: Global state
        mode: Add (0) or Remove (1)
    """
    if not state_event_error_handler(state):
        return

    ing_raw = input("Available ingredients (comma separated): ")
    state.current_event.modify_ingredients(ing_raw, mode)


def view_recipes(state):
    """
    Prints recipes for one event

    Args:
        state: Global state
    """
    if not state_event_error_handler(state):
        return

    event = state.current_event

    if not event.saved_recipes:
        print("No saved recipes")
        return

    for recipe in event.saved_recipes:
        recipe.display()
        print("")


def list_all_events(state):
    """
    Displays information for all events

    Args:
        state: Global state
    """
    if not state.events:
        print("No events found.")
    else:
        print("==== ALL EVENTS ====")
        for event in state.events.values():
            event.display()
            print("")


def delete_event(state):
    """
    Delete current event. Removes it from the
    state's stored events as well as the
    database.

    Args:
        state: Global state
    """
    # import statement here to avoid circular imports
    from menu_builders import build_all_events_menu

    if not state_event_error_handler(state):
        return

    confirm = "no input yet"

    while confirm != "y":
        confirm = input("WARNING: This cannot be undone." +
                        "Type 'y' to confirm and 'n' to go back.")
        if (confirm.lower() == "n"):
            print("Event deletion cancelled.")
            return
        elif (confirm != "y"):
            print("Invalid input.")

    event = state.current_event

    # delete from db
    try:
        with event.engine.begin() as conn:
            conn.execute(
                db.text("DELETE FROM event_diets WHERE event_id = :id"),
                {"id": event.id}
            )

            conn.execute(
                db.text("DELETE FROM event_intolerances WHERE event_id = :id"),
                {"id": event.id}
            )

            conn.execute(
                db.text("DELETE FROM ingredients WHERE event_id = :id"),
                {"id": event.id}
            )

            conn.execute(
                db.text("DELETE FROM event_recipes WHERE event_id = :id"),
                {"id": event.id}
            )

            conn.execute(
                db.text("DELETE FROM events WHERE id = :id"),
                {"id": event.id}
            )

        state.current_event = None
        state.events.pop(event.id, None)  # deletes from state
        print("Successfully deleted the event.")
    except SQLAlchemyError as e:
        print(f"Failed to delete event: {e}")

    return build_all_events_menu(state)


def generate_recipes(state):
    """
    Generates recipes using Spoonacular's API for the current_event based on
    the diets and intolerances associated with the event.

    Args:
        state: Global state
    """
    if not state.spoonacular_key:
        print("Missing Spoonacular API key.")
        return

    if not state_event_error_handler(state):
        return

    event = state.current_event

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
        try:
            response = requests.get(url, timeout=25)
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            continue

        if api_error_handler(response):  # returns true if we're chilling
            data = response.json()
            for recipe in data.get("results", []):
                rid = recipe["id"]
                ingreds = get_recipe_ingredients(state, rid)
                recipes[category][rid] = Recipe(recipe["title"], ingreds, rid)

    print("\n!!! MAIN COURSES !!!")
    for recipe in recipes["main course"].values():
        recipe.display()
    print("")

    print("!!! APPETIZERS !!!")
    for recipe in recipes["appetizer"].values():
        recipe.display()
    print("")

    print("!!! DESSERTS !!!")
    for recipe in recipes["dessert"].values():
        recipe.display()
    print("")

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
    if not state.spoonacular_key:
        print("Missing Spoonacular API key.")
        return []

    url = (f"https://api.spoonacular.com/recipes/" +
           f"{recipeid}/ingredientWidget.json?"
           + f"apiKey={state.spoonacular_key}")

    try:
        response = requests.get(url, timeout=25)
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return []

    if api_error_handler(response):
        data = response.json()
        ingredients = []

        for ingredient in data.get("ingredients", []):
            ingredients.append(ingredient["name"])

        return ingredients
    else:
        return []


def estimate_recipe_cost(state):
    """
    Uses Gemini API call to estimate the cost of all recipes affiliated
    with the current event and provide a breakdown based on ingredient.

    Args:
        state: Global state
    """
    if not state_event_error_handler(state):
        return

    attendees = state.current_event.attendee_count
    recipes = state.current_event.saved_recipes

    if not recipes:
        print("No recipes saved for this event.")
        return

    if not state.gemini_key:
        print("Missing Gemini API key.")
        return

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

    try:
        response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
                )
        print(response.text)
    except Exception as e:
        print(f"Gemini request failed: {e}")


def api_error_handler(response):
    """
    Checks if an API call was successful. If not,
    prints error.

    Returns false if there was an error,
    returns true if there was no error.

    Args:
        response: the response of the API call
    """
    if response.ok:
        return True

    print("There was an error with the API request.")
    print(f"Error Code: {response.status_code}")
    print(f"Error Message: {response.reason}")
    return False


def state_event_error_handler(state):
    """
    Checks if there is currently a selected event.
    If so, returns true. Otherwise, returns false.

    Args:
        state: Global state
    """
    if not state.current_event:
        print("No event selected.")
        return False
    return True
