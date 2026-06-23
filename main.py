from Menu import Menu
from MenuItem import MenuItem
from Event import Event
from AppState import AppState


def main():
    print("partyfood: coming soon")
    run_app()


def run_app():
    state = AppState()
    state.set_current_event(Event("dummy", 10))

    current_menu = build_main_menu(state)

    while current_menu:
        current_menu.display()
        choice = input("Select: ")
        selected = current_menu.select(choice)  # could be a menu or a function

        if selected:
            result = selected.select()

            if isinstance(result, Menu):
                current_menu = result  # change to new menu


def build_intolerance_menu(state, mode):
    """
    Args:
        event: Event to be Modified
        mode: Add (0) or Remove (1)
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
                      lambda: handler("wheat"))
    }
    intolerance_menu = Menu("Intolerances",
                            intolerance_options_dict)
    return intolerance_menu


def build_diets_menu(state, mode):
    """
    Args:
        event: Event to be Modified
        mode: Add (0) or Remove (1)
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
                      lambda: handler("whole30"))
    }
    diet_menu = Menu("Diets", diet_options_dict)
    return diet_menu


def build_edit_event_menu(state):
    # TODO: should be able to pass in which event we're modifying
    # build edit event menu
    event = state.current_event

    edit_event_dict = {
        "A": MenuItem("A", "Add Diets",
                      lambda: build_diets_menu(state, 0)),
        "B": MenuItem("B", "Remove Diets",
                      lambda: build_diets_menu(state, 1)),
        "C": MenuItem("C", "Add Intolerances",
                      lambda: build_intolerances_menu(state, 0)),
        "D": MenuItem("D", "Remove Intolerances",
                      lambda: build_intolerances_menu(state, 1)),
        "E": MenuItem("E", "Add Ingredients", None),
        "F": MenuItem("F", "Remove Ingredients", None),
        "G": MenuItem("G", "Set Attendee Count", None),
        "H": MenuItem("H", "Generate Recipes", None),
        "I": MenuItem("I", "Remove Recipe", None)
    }
    edit_event_menu = Menu("Edit Event", edit_event_dict)
    return edit_event_menu


def build_single_event_menu(state):
    event = state.current_event

    event_menu_dict = {
        "A": MenuItem("A", "List Info",
                      lambda: event.display()),
        "B": MenuItem("B", "View All Recipes", None),
        "C": MenuItem("C", "List Ingredients", None),
        "D": MenuItem("D", "View One Recipe", None),
        "E": MenuItem("E", "Edit Event",
                      lambda: build_edit_event_menu(state))
    }
    single_event_menu = Menu("Event Menu", event_menu_dict)
    return single_event_menu


def build_all_events_menu(state):
    all_events_dict = {
        "A": MenuItem("A", "List All Events", None),
        "B": MenuItem("B", "Choose Event", None)
    }
    all_events_menu = Menu("View and Edit Events", all_events_dict)
    return all_events_menu


def build_main_menu(state):
    # build main menu
    main_menu_dict = {
        "A": MenuItem("A", "View and Edit Events",
                      lambda: build_all_events_menu(state)),
        "B": MenuItem("B", "Create New Event", None),
        "C": MenuItem("C", "Generate Recipes", None)
    }
    return Menu("Main Menu", main_menu_dict)


def createEventChooserMenu():
    # TODO
    # This method should fetch the events from database and present
    # them as options in a menu
    return


if __name__ == "__main__":
    main()
