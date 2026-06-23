import Menu
import MenuItem
import sqlalchemy as db
import pandas as pd


def main():
    # Establish the database connection on app execution
    # use this engine variable for functions requiring database access
    engine = db.create_engine('sqlite:///food.db')
    init_db(engine)
    createEventChooserMenu(engine)

    # Run as normal
    events = {}
    current_event = None
    print("partyfood: coming soon")


def build_intolerance_menu(event, mode):
    """
    Args:
        event: Event to be Modified
        mode: Add (0) or Remove (1)
    """
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
    intolerance_menu = Menu("I", "Intolerances",
                            intolerance_options_dict)
    return intolerance_menu


def build_diets_menu(event, mode):
    """
    Args:
        event: Event to be Modified
        mode: Add (0) or Remove (1)
    """
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
    diet_menu = Menu("D", "Diets", diet_options_dict)
    return diet_menu


def build_edit_event_menu(event):
    # TODO: should be able to pass in which event we're modifying
    # build edit event menu
    edit_event_dict = {
        "A": MenuItem("A", "Add Diets",
                      lambda: build_diets_menu(event, 0)),
        "B": MenuItem("B", "Remove Diets",
                      lambda: build_diets_menu(event, 1)),
        "C": MenuItem("C", "Add Intolerances",
                      lambda: build_intolerances_menu(event, 0)),
        "D": MenuItem("D", "Remove Intolerances",
                      lambda: build_intolerances_menu(event, 1)),
        "E": MenuItem("E", "Add Ingredients", None),
        "F": MenuItem("F", "Remove Ingredients", None),
        "G": MenuItem("G", "Set Attendee Count", None),
        "H": MenuItem("H", "Generate Recipes", None),
        "I": MenuItem("I", "Remove Recipe", None)
    }
    edit_event_menu = Menu("E", "Edit Event", edit_event_dict)
    return edit_event_menu


def build_single_event_menu(event):
    # TODO: should be able to pass in which event we're modifying
    # build event menu
    event_menu_dict = {
        "A": MenuItem("A", "List Info", None),
        "B": MenuItem("B", "View All Recipes", None),
        "C": MenuItem("C", "List Ingredients", None),
        "D": MenuItem("D", "View One Recipe", None),
        "E": build_edit_event_menu(event)
    }
    single_event_menu = Menu("M", "Event Menu", event_menu_dict)
    return single_event_menu


def build_all_events_menu():
    all_events_dict = {
        "A": MenuItem("A", "List All Events", None),
        "B": MenuItem("B", "Choose Event", None)
    }
    all_events_menu = Menu("A", "View and Edit Events")
    return all_events_menu


def build_main_menu():
    # build main menu
    main_menu_dict = {
        "A": build_all_events_menu(),
        "B": MenuItem("B", "Create New Event", None),
        "C": MenuItem("C", "Generate Recipes", None)
    }

# inits the database.
# Intended to be used when the database/tables are not 
def init_db(engine):
    with open("storage/schema.sql", "r") as f:
        schema = f.read()

    raw_conn = engine.raw_connection()
    try:
        raw_conn.executescript(schema)
        raw_conn.commit()
    finally:
        raw_conn.close()

def createEventChooserMenu(engine):
    # This method should fetch the events from database and present
    # them as options in a menu

    with engine.connect() as connection:
        result = connection.execute(db.text("SELECT event_name FROM events;")).fetchall()

        if not result:
            print("No events found. Please create an event first")
            return

        events = [row[0] for row in result]

        print("Select an event:")
        for i, event in enumerate(events, 1):
            print(f"  {i}. {event}")


if __name__ == "__main__":
    main()