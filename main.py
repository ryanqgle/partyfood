from Menu import Menu
from MenuItem import MenuItem
from menu_builders import build_main_menu
from Event import Event
from AppState import AppState
import sqlalchemy as db


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

        print("")  # newline


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


if __name__ == "__main__":
    main()
