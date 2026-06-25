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
        Recipe ID: {recipe.id}
        Recipe: {recipe.name}
        Ingredients: {', '.join(recipe.ingredients)}
        """

    client = genai.Client(api_key=state.gemini_key)

    prompt = f"""
    Estimate the grocery cost for preparing these recipes for {attendees}
    people in the United States. Assume average supermarket prices.

    Recipes:
    {recipe_text}

    Return ONLY valid JSON: an array with one object per recipe, using the
    Recipe ID given above. Use this exact shape:
    [
      {{
        "recipe_id": <the Recipe ID>,
        "recipe_name": "<recipe name>",
        "ingredient_costs": [
          {{"ingredient": "<ingredient name>", "cost": "$x-$y"}}
        ],
        "total_cost": "$x-$y"
      }}
    ]
    Do not include any text, explanation, or markdown outside the JSON.
    """

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            # ensures the response can be parsed as JSON
            config=types.GenerateContentConfig(
                response_mime_type="application/json"
            ),
        )
    except Exception as e:
        print(f"Gemini request failed: {e}")
        return

    try:
        estimates = json.loads(response.text)
    except (json.JSONDecodeError, TypeError):
        # if can't parse for whatever reason, print the raw response
        print("Could not parse cost estimate from Gemini:")
        print(response.text)
        return

    print("==== Estimated Costs ====")
    for item in estimates:
        recipe_id = item.get("recipe_id")

        # store this recipe's cost (as JSON) in its own estimated_cost cell
        cost_json = json.dumps({
            "recipe_name": item.get("recipe_name"),
            "ingredient_costs": item.get("ingredient_costs", []),
            "total_cost": item.get("total_cost"),
        })
        state.current_event.set_recipe_cost(recipe_id, cost_json)

        # print a readable breakdown
        print(f"\n{item.get('recipe_name')} (total: {item.get('total_cost')})")
        for ic in item.get("ingredient_costs", []):
            print(f"  - {ic.get('ingredient')}: {ic.get('cost')}")


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
