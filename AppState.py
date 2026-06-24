from Menu import Menu
from MenuItem import MenuItem
from Event import Event
import sqlalchemy as db
import pandas as pd


class AppState:
    """
    Holds shared state and does database stuff
    """

    def __init__(self, engine):
        self.current_event = None
        # TODO: put all the existing 
        self.events = {} #key: eventid from db, value: event obj
        self.engine = engine

    def set_event_by_obj(self, event):
        """
        Sets current event by receiving an event object
        """
        self.current_event = event
        # we should also make sure this event is in self.events

    def set_event_by_id(self, eventid):
        """
        Sets current event by receiving the eventID
        """
        obj = self.events.get(eventid)
        if obj:
            self.current_event = obj
        else:
            print("Invalid ID")

    def set_engine(self, engine):
        self.engine = engine

    def populate_events(self):
        """
        Fills the events dict with events from the db
        """
        with self.engine.connect() as connection:
            result = connection.execute(
                db.text("SELECT * FROM events;")
                ).fetchall()

            if not result:
                print("No events found. Please create an event first")
                return

            self.events = {}

            for row in result:
                event_id = row[0]
                event_name = row[1]
                attendees = row[2]

                event = Event(event_name, attendees)

                self.load_diets(connection, event, event_id)
                self.load_intolerances(connection, event, event_id)
                self.load_ingredients(connection, event, event_id)

                self.events[event_id] = event


    def load_diets(self, connection, event, event_id):
        """
        Loads all diets associated with an event from the db
        """
        result = connection.execute(
            db.text("""
                SELECT diet
                FROM event_diets
                WHERE event_id = :id
            """),
            {"id": event_id}
        ).fetchall()

        for row in result:
            diet = row[0]
            event.add_diet(diet)

    def load_intolerances(self, connection, event, event_id):
        result = connection.execute(
            db.text("""
                SELECT intolerance
                FROM event_intolerances
                WHERE event_id = :id
                """),
            {"id": event_id}
        ).fetchall()

        for row in result:
            intolerance = row[0]
            event.add_intolerance(intolerance)

    def load_ingredients(self, connection, event, event_id):
        result = connection.execute(
            db.text("""
                SELECT event_ingredients
                FROM ingredients
                WHERE event_id = :id
                """),
            {"id": event_id}
        ).fetchall()

        for row in result:
            ingredient = row[0]
            event.add_ingredient(ingredient)
