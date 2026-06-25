import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import sqlalchemy as db
from AppState import AppState

SCHEMA_PATH = os.path.join(os.path.dirname(__file__), "..", "storage", "schema.sql")


class TestAppStateDb(unittest.TestCase):
    # Round-trips events through a real (temporary) SQLite database to verify
    # that loading works and that Event edits persist to disk.

    def setUp(self):
        # A temp file (not :memory:) so separate connections share one db.
        fd, self.db_path = tempfile.mkstemp(suffix=".db")
        os.close(fd)
        self.engine = db.create_engine(f"sqlite:///{self.db_path}")

        with open(SCHEMA_PATH) as f:
            raw = self.engine.raw_connection()
            raw.executescript(f.read())
            raw.commit()
            raw.close()

        # Get one known event to load.
        with self.engine.begin() as conn:
            result = conn.execute(
                db.text("INSERT INTO events (event_name, attendee_count) "
                        "VALUES ('Birthday', 20)")
            )
            self.event_id = result.lastrowid
            conn.execute(
                db.text("INSERT INTO event_diets (event_id, diet) "
                        "VALUES (:id, 'vegetarian')"),
                {"id": self.event_id},
            )

    def tearDown(self):
        self.engine.dispose()
        os.remove(self.db_path)

    def test_populate_events_loads_event(self):
        state = AppState(self.engine)
        state.populate_events()

        self.assertIn(self.event_id, state.events)
        event = state.events[self.event_id]
        self.assertEqual(event.name, "Birthday")
        self.assertEqual(event.attendee_count, 20)
        self.assertIn("vegetarian", event.diets)

    def test_loaded_event_has_engine_attached(self):
        state = AppState(self.engine)
        state.populate_events()
        event = state.events[self.event_id]
        # After loading, the engine should be attached so edits persist.
        self.assertIsNotNone(event.engine)
        self.assertEqual(event.id, self.event_id)

    def test_edits_persist_across_reload(self):
        state = AppState(self.engine)
        state.populate_events()
        event = state.events[self.event_id]

        event.update_attendees(99)
        event.set_name("Renamed Party")
        event.add_diet("vegan")
        event.add_intolerance("soy")
        event.add_ingredient("flour")

        # Fresh state reads straight from disk -> proves the writes committed.
        reloaded = AppState(self.engine)
        reloaded.populate_events()
        event2 = reloaded.events[self.event_id]

        self.assertEqual(event2.name, "Renamed Party")
        self.assertEqual(event2.attendee_count, 99)
        self.assertIn("vegan", event2.diets)
        self.assertIn("soy", event2.intolerances)
        self.assertIn("flour", event2.ingredients)


if __name__ == "__main__":
    unittest.main()
