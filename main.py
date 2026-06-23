import Menu
import MenuItem


def main():
    print("partyfood: coming soon")


def buildMenu():
    # build intolerance menu
    intolerance_options_dict = {
        "A": MenuItem("A", "Dairy", None),
        "B": MenuItem("B", "Egg", None),
        "C": MenuItem("C", "Gluten", None),
        "D": MenuItem("D", "Grain", None),
        "E": MenuItem("E", "Peanut", None),
        "F": MenuItem("F", "Seafood", None),
        "G": MenuItem("G", "Sesame", None),
        "H": MenuItem("H", "Shellfish", None),
        "I": MenuItem("I", "Soy", None),
        "J": MenuItem("J", "Sulfite", None),
        "K": MenuItem("K", "Tree Nut", None),
        "L": MenuItem("L", "Wheat", None)
    }
    intolerance_menu = Menu("I", "Intolerances",
                            intolerance_options_dict)
    # TODO: need to decide how to differentiate between remove & add

    # build diets menu
    diet_options_dict = {
        "A": MenuItem("A", "Paleo", None),
        "B": MenuItem("B", "Low FODMAP", None),
        "C": MenuItem("C", "Pescetarian", None),
        "D": MenuItem("D", "Gluten Free", None),
        "E": MenuItem("E", "Keto | Ketogenic", None),
        "F": MenuItem("F", "Vegetarian", None),
        "G": MenuItem("G", "Lacto-Vegetarian", None),
        "H": MenuItem("H", "Ovo-Vegetarian", None),
        "I": MenuItem("I", "Vegan", None),
        "J": MenuItem("J", "Primal", None),
        "K": MenuItem("K", "Whole30", None)
    }
    diet_menu = Menu("D", "Diets", diet_options_dict)
    # TODO: need to decide how to differentiate between remove & add

    # build edit event menu
    edit_event_dict = {
        "A": MenuItem("A", "Add Diets", None),
        "B": MenuItem("B", "Remove Diets", None),
        "C": MenuItem("C", "Add Intolerances", None),
        "D": MenuItem("D", "Remove Intolerances", None),
        "E": MenuItem("E", "Add Ingredients", None),
        "F": MenuItem("F", "Remove Ingredients", None),
        "G": MenuItem("G", "Set Attendee Count", None),
        "H": MenuItem("H", "Generate Recipes", None),
        "I": MenuItem("I", "Remove Recipe", None)
    }
    edit_event_menu = Menu("E", "Edit Event", edit_event_dict)

    # build event menu
    event_menu_dict = {
        "A": MenuItem("A", "List Info", None),
        "B": MenuItem("B", "View All Recipes", None),
        "C": MenuItem("C", "List Ingredients", None),
        "D": MenuItem("D", "View One Recipe", None),
        "E": edit_event_menu
    }
    event_menu = Menu("M", "Event Menu", event_menu_dict)
    # TODO: need to decide how do it if listing the different events

    all_events_dict = {
        "A": MenuItem("A", "List All Events", None),
        "B": MenuItem("B", "Choose Event", None)
    }
    all_events_menu = Menu("A", "View and Edit Events")

    # build main menu
    main_menu_dict = {
        "A": all_events_menu,
        "B": MenuItem("B", "Create New Event", None),
        "C": MenuItem("C", "Generate Recipes", None)
    }


def createEventChooserMenu():
    # TODO
    # This method should fetch the events from database and present
    # them as options in a menu
    return


if __name__ == "__main__":
    main()
