from Menu import Menu
from MenuItem import MenuItem
from Event import Event
from menu_actions import *


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
        "X": MenuItem("X", "Back", lambda: next_menu)
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
        "X": MenuItem("X", "Back", lambda: next_menu)
    }
    diet_menu = Menu("Diets", diet_options_dict)
    return diet_menu


def build_edit_event_menu(state):
    """ Builds the menu to edit a single event. """
    event = state.current_event

    menu = Menu("Edit Event", {})
    menu.options = {
        "A": MenuItem("A", "Add Diets",
                      lambda: build_diets_menu(state, 0, menu)),
        "B": MenuItem("B", "Remove Diets",
                      lambda: build_diets_menu(state, 1, menu)),
        "C": MenuItem("C", "Add Intolerances",
                      lambda: build_intolerances_menu(state, 0, menu)),
        "D": MenuItem("D", "Remove Intolerances",
                      lambda: build_intolerances_menu(state, 1, menu)),
        "E": MenuItem("E", "Add Ingredients",
                      set_event_ingredients(state, 0)),
        "F": MenuItem("F", "Remove Ingredients",
                      set_event_ingredients(state, 1)),
        "G": MenuItem("G", "Set Attendee Count", set_event_attendees(state)),
        "H": MenuItem("H", "Generate Recipes", None),  # TODO
        # "I": MenuItem("I", "Remove Recipe", None)  # could be later
        "X": MenuItem("X", "Save Event",
                      lambda: build_single_event_menu(state))
    }
    return menu


def build_single_event_menu(state):
    """ Builds the menu to view information for a single event. """
    event = state.current_event

    event_menu_dict = {
        "A": MenuItem("A", "List Info",
                      lambda: event.display()),
        "B": MenuItem("B", "View All Recipes", None),  # TODO
        # "C": MenuItem("C", "List Ingredients", None),  # could be later
        # "D": MenuItem("D", "View One Recipe", None),  # could be later
        "E": MenuItem("E", "Edit Event",
                      lambda: build_edit_event_menu(state)),
        "X": MenuItem("X", "Back to All Events",
                      lambda: build_all_events_menu(state))
    }
    single_event_menu = Menu("Event Menu", event_menu_dict)
    return single_event_menu


def build_all_events_menu(state):
    """ Builds the events menu. """
    all_events_dict = {
        "A": MenuItem("A", "List All Events",
                      lambda: list_all_events(state)),
        "B": MenuItem("B", "Choose Event",
                      lambda: build_event_selector(state)),
        "X": MenuItem("X", "Back to Main Menu",
                      lambda: build_main_menu(state))
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
        "C": MenuItem("C", "Generate Recipes", None)  # TODO
    }
    return Menu("Main", main_menu_dict)


def build_event_selector(state):
    """
    Builds a menu to select events
    """
    def select(event):
        state.set_event_by_obj(event)
        return build_single_event_menu(state)

    options = {}
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    for i, (eid, event) in enumerate(state.events.items()):
        key = letters[i]
        options[key] = MenuItem(key, event.name,
                                lambda event=event: select(event))

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
                      lambda: save_event(state))
    }

    def custom_display():
        event = state.current_event
        print("==== Create Event ====")
        event.display()
        print("\nOptions:")
        for item in menu.options.values():
            item.display()

    menu.display = custom_display
    return menu


def save_event(state):
    # Persists the current in-memory event (and its diets, intolerances,
    # and ingredients) to the database, then returns to the main menu.
    event = state.current_event
    engine = state.engine

    with engine.begin() as conn:  # begin() commits automatically on success
        result = conn.execute(
            db.text(
                "INSERT INTO events (event_name, attendee_count) "
                "VALUES (:name, :count)"
            ),
            {"name": event.name, "count": event.attendee_count},
        )

        # get the auto-incremented id so child rows can reference it
        event.id = result.lastrowid

        for diet in event.diets:
            conn.execute(
                db.text(
                    "INSERT INTO event_diets (event_id, diet) "
                    "VALUES (:id, :diet)"
                ),
                {"id": event.id, "diet": diet},
            )

        for intolerance in event.intolerances:
            conn.execute(
                db.text(
                    "INSERT INTO event_intolerances (event_id, intolerance) "
                    "VALUES (:id, :intolerance)"
                ),
                {"id": event.id, "intolerance": intolerance},
            )

        # schema stores ingredients as a single comma-joined string per event
        if event.ingredients:
            conn.execute(
                db.text(
                    "INSERT INTO ingredients (event_id, event_ingredients) "
                    "VALUES (:id, :ingredients)"
                ),
                {"id": event.id, "ingredients": ",".join(event.ingredients)},
            )

    # keep the in-memory dict in sync with the db so menus that read
    # state.events (e.g. the event selector) include the new event
    state.events[event.id] = event

    print(f"Saved '{event.name}' (id {event.id}).")
    return build_main_menu(state)
