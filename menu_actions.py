import sqlalchemy as db


def set_event_name(state):
    name = input("Event Name: ")
    state.current_event.set_name(name)


def set_event_attendees(state):
    count = int(input("Number of attendees: "))
    state.current_event.update_attendees(count)


def set_event_ingredients(state, mode):
    ing_raw = input("Available ingredients (comma separated): ")
    state.current_event.modify_ingredients(ing_raw)


def view_recipes(state):
    """
    Prints recipes for one event
    """
    event = state.current_event

    if not event.recipes:
        print("No saved recipes")
        return

    # I think we will eventually need to make a class for recipes
    # and each recipe will have it's own display function
    # then we can loop through displays recipes here and display
    return


def list_all_events(state):
    """
    Displays information for all events
    """
    print("==== ALL EVENTS ====")
    for event in state.events.values():
        event.display()
        print("")  # create newline

    return


def generate_recipes():
    """
    this is the scary part
    """
    return
