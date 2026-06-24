from Menu import Menu
from MenuItem import MenuItem
from Event import Event
from AppState import AppState
import sqlalchemy as db
import pandas as pd


def main():
    # Establish the database connection on app execution
    # use this engine variable for functions requiring database access
    engine = db.create_engine('sqlite:///food.db')
    init_db(engine)

    # Run as normal
    print("partyfood: coming soon")
    state = AppState(engine)
    state.populate_events()
    run_app(state)


def run_app(state):
    """
    Runs the CLI.
    """
    current_menu = build_main_menu(state)

    while current_menu:
        current_menu.display()
        choice = input("Select: ")
        selected = current_menu.select(choice)  # could be a menu or a function

        if selected:
            result = selected.select()

            if isinstance(result, Menu):
                current_menu = result  # change to new menu


def init_db(engine):
    # inits the database.
    # Intended to be used when the database/tables are empty.
    with open("storage/schema.sql", "r") as f:
        schema = f.read()

    raw_conn = engine.raw_connection()
    try:
        raw_conn.executescript(schema)
        raw_conn.commit()
    finally:
        raw_conn.close()


# EVENT BUILDERS

def build_intolerances_menu(state, mode, next_menu):
    """
    Builds the menu to add / remove intolerances.

    Args:
        state: Global state
        mode: Add (0) or Remove (1)
        next_menu: The menu to be sent to upon exit.
    """
    event = state.current_event

    def handler(choice):
        if mode == 0:
            event.add_intolerance(choice)
        else:
            event.remove_intolerance(choice)

    # TODO: check how spoonful api takes these as args
    intolerance_options_dict = {
        "A": MenuItem("A", "Dairy",
                      lambda: handler("dairy")),
        "B": MenuItem("B", "Egg",
                      lambda: handler("egg")),
        "C": MenuItem("C", "Gluten",
                      lambda: handler("gluten")),
        "D": MenuItem("D", "Grain",
                      lambda: handler("grain")),
        "E": MenuItem("E", "Peanut",
                      lambda: handler("peanut")),
        "F": MenuItem("F", "Seafood",
                      lambda: handler("seafood")),
        "G": MenuItem("G", "Sesame",
                      lambda: handler("sesame")),
        "H": MenuItem("H", "Shellfish",
                      lambda: handler("shellfish")),
        "I": MenuItem("I", "Soy",
                      lambda: handler("soy")),
        "J": MenuItem("J", "Sulfite",
                      lambda: handler("sulfite")),
        "K": MenuItem("K", "Tree Nut",
                      lambda: handler("tree nut")),
        "L": MenuItem("L", "Wheat",
                      lambda: handler("wheat")),
        "X": MenuItem("X", "Back", lambda: next_menu())
    }
    intolerance_menu = Menu("Intolerances",
                            intolerance_options_dict)
    return intolerance_menu


def build_diets_menu(state, mode, next_menu):
    """
    Builds the menu to add / remove diets.

    Args:
        state: Global state
        mode: Add (0) or Remove (1)
        next_menu: The menu to be sent to upon exit.
    """
    event = state.current_event

    def handler(choice):
        if mode == 0:
            event.add_diet(choice)
        else:
            event.remove_diet(choice)

    # TODO: check how spoonful api takes these as args
    diet_options_dict = {
        "A": MenuItem("A", "Paleo",
                      lambda: handler("paleo")),
        "B": MenuItem("B", "Low FODMAP",
                      lambda: handler("low fodmap")),
        "C": MenuItem("C", "Pescetarian",
                      lambda: handler("pescetarian")),
        "D": MenuItem("D", "Gluten Free",
                      lambda: handler("gluten free")),
        "E": MenuItem("E", "Keto | Ketogenic",
                      lambda: handler("keto")),
        "F": MenuItem("F", "Vegetarian",
                      lambda: handler("vegetarian")),
        "G": MenuItem("G", "Lacto-Vegetarian",
                      lambda: handler("lacto-vegetarian")),
        "H": MenuItem("H", "Ovo-Vegetarian",
                      lambda: handler("ovo-vegetarian")),
        "I": MenuItem("I", "Vegan",
                      lambda: handler("vegan")),
        "J": MenuItem("J", "Primal",
                      lambda: handler("primal")),
        "K": MenuItem("K", "Whole30",
                      lambda: handler("whole30")),
        "X": MenuItem("X", "Back", lambda: next_menu())
    }
    diet_menu = Menu("Diets", diet_options_dict)
    return diet_menu


def build_edit_event_menu(state):
    """ Builds the menu to edit a single event. """
    event = state.current_event

    menu = Menu("Edit Event", {})
    edit_event_menu.options = {
        "A": MenuItem("A", "Add Diets",
                      lambda: build_diets_menu(state, 0, menu)),
        "B": MenuItem("B", "Remove Diets",
                      lambda: build_diets_menu(state, 1, menu)),
        "C": MenuItem("C", "Add Intolerances",
                      lambda: build_intolerances_menu(state, 0, menu)),
        "D": MenuItem("D", "Remove Intolerances",
                      lambda: build_intolerances_menu(state, 1, menu)),
        "E": MenuItem("E", "Add Ingredients", None),
        "F": MenuItem("F", "Remove Ingredients", None),
        "G": MenuItem("G", "Set Attendee Count", None),
        "H": MenuItem("H", "Generate Recipes", None),
        "I": MenuItem("I", "Remove Recipe", None)  # could be later
    }
    return menu


def build_single_event_menu(state):
    """ Builds the menu to view information for a single event. """
    event = state.current_event

    event_menu_dict = {
        "A": MenuItem("A", "List Info",
                      lambda: event.display()),
        "B": MenuItem("B", "View All Recipes", None),
        "C": MenuItem("C", "List Ingredients", None),  # could be later
        "D": MenuItem("D", "View One Recipe", None),  # could be later
        "E": MenuItem("E", "Edit Event",
                      lambda: build_edit_event_menu(state))
    }
    single_event_menu = Menu("Event Menu", event_menu_dict)
    return single_event_menu


def build_all_events_menu(state):
    """ Builds the events menu. """
    all_events_dict = {
        "A": MenuItem("A", "List All Events", None),
        "B": MenuItem("B", "Choose Event",
                      lambda: build_event_selector(state))
    }
    all_events_menu = Menu("View and Edit Events", all_events_dict)
    return all_events_menu


def build_main_menu(state):
    """ Builds the main menu. """
    main_menu_dict = {
        "A": MenuItem("A", "View and Edit Events",
                      lambda: build_all_events_menu(state)),
        "B": MenuItem("B", "Create New Event",
                      lambda: build_create_event_menu(state)),
        "C": MenuItem("C", "Generate Recipes", None)
    }
    return Menu("Main Menu", main_menu_dict)


def build_event_selector(state):
    # WIP
    # This method should fetch the events from database and present
    # them as options in a menu
    engine = state.engine

    with engine.connect() as connection:
        result = connection.execute(
            db.text("SELECT event_name FROM events;")
        ).fetchall()

        if not result:
            print("No events found. Please create an event first")
            return

        def select(event_id):
            state.set_current_event() # TODO: add functionality (in AppState.py) to get the event associated with ID
            return build_edit_event_menu(state)


        options = {}
        for i in range(len(result)):
            row = result[i]
            event_id = row[0]
            event_name = row[1]

            options[i] = MenuItem(
                i, event_name, lambda eid=event_id: select(eid)
            )

        options["X"] = MenuItem("X", "Back", lambda: build_all_events_menu(state))

    
    return Menu("Select Event", options)


def build_create_event_menu(state):
    """
    Builds the menu to create a new event
    """
    state.current_event = Event("New Event")
    menu = Menu("Options", {})
    menu.options = {
        "A": MenuItem("A", "Set Name",
                      lambda: set_event_name(state)),
        "B": MenuItem("B", "Add Existing Ingredients",
                      lambda: set_event_ingredients(state, 0)),
        "C": MenuItem("C", "Add Diets",
                      lambda: build_diets_menu(state,
                                               0, lambda: menu)),
        "D": MenuItem("D", "Add Intolerances",
                      lambda: build_intolerances_menu(state,
                                                      0, lambda: menu)),
        "E": MenuItem("E", "Set Attendees",
                      lambda: set_event_attendees(state)),
        "X": MenuItem("X", "Save Event",
                      lambda: build_main_menu(state))
    }

    def custom_display():
        event = state.current_event
        print("==== Create Event ====")
        event.display()
        for item in menu.options.values():
            item.display()

    menu.display = custom_display
    return menu


# FUNCTIONS TO RUN FOR OPTIONS

def set_event_name(state):
    name = input("Event Name: ")
    state.current_event.set_name(name)


def set_event_attendees(state):
    count = int(input("Number of attendees: "))
    state.current_event.update_attendees(count)


def set_event_ingredients(state, mode):
    ing_raw = input("Available ingredients (comma separated): ")
    state.current_event.modify_ingredients(ing_raw)


if __name__ == "__main__":
    main()
