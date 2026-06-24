def set_event_name(state):
    name = input("Event Name: ")
    state.current_event.set_name(name)


def set_event_attendees(state):
    count = int(input("Number of attendees: "))
    state.current_event.update_attendees(count)


def set_event_ingredients(state, mode):
    ing_raw = input("Available ingredients (comma separated): ")
    state.current_event.modify_ingredients(ing_raw)
