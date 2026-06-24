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


def list_all_events(state):
    # Prints every event stored in the database. 
    engine = state.engine

    with engine.connect() as connection:
        result = connection.execute(
            db.text("SELECT id, event_name, attendee_count FROM events;")
        ).fetchall()

    if not result:
        print("No events found. Please create an event first.")
        return

    print("==== All Events ====")
    for event_id, name, attendee_count in result:
        print(f"  {event_id}. {name} ({attendee_count} attendees)")
