import os
import sys
import unittest

# Allow importing the project modules when tests are run from any directory.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from Event import Event


class TestEventInMemory(unittest.TestCase):
    # Tests Event's in-memory behavior. With no id/engine, the db writes
    # should not operate, so these tests *should* never touch a database.

    def setUp(self):
        self.event = Event("Test Party", attendee_count=10)

    def test_initial_state(self):
        self.assertEqual(self.event.name, "Test Party")
        self.assertEqual(self.event.attendee_count, 10)
        self.assertEqual(self.event.diets, set())
        self.assertEqual(self.event.intolerances, set())
        self.assertEqual(self.event.ingredients, set())

    def test_add_diet_is_normalized(self):
        self.event.add_diet("  Vegan ")
        self.assertIn("vegan", self.event.diets)

    def test_no_duplicate_diets(self):
        self.event.add_diet("vegan")
        self.event.add_diet("vegan")
        self.assertEqual(len(self.event.diets), 1)

    def test_remove_diet(self):
        self.event.add_diet("vegan")
        self.event.remove_diet("vegan")
        self.assertNotIn("vegan", self.event.diets)

    def test_add_intolerance_is_normalized(self):
        self.event.add_intolerance(" Soy ")
        self.assertIn("soy", self.event.intolerances)

    def test_update_attendees(self):
        self.event.update_attendees(42)
        self.assertEqual(self.event.attendee_count, 42)

    def test_set_name(self):
        self.event.set_name("Renamed")
        self.assertEqual(self.event.name, "Renamed")

    def test_modify_ingredients_add_then_remove(self):
        self.event.modify_ingredients("Eggs, Butter, Flour", mode=0)
        self.assertEqual(self.event.ingredients, {"eggs", "butter", "flour"})

        self.event.modify_ingredients("butter", mode=1)
        self.assertEqual(self.event.ingredients, {"eggs", "flour"})

    def test_modify_ingredients_ignores_blanks(self):
        self.event.modify_ingredients("eggs,, ,butter", mode=0)
        self.assertEqual(self.event.ingredients, {"eggs", "butter"})

    def test_writes_are_noop_without_engine(self):
        # id/engine are None, so this must not do anything.
        self.assertIsNone(self.event.id)
        self.assertIsNone(self.event.engine)
        self.event.add_diet("keto")  # would explode if it tried to write


class TestRecipeSearchUrl(unittest.TestCase):
    # Validates the Spoonacular search URL Event builds. 

    class _FakeState:
        spoonacular_key = "TESTKEY"

    def setUp(self):
        self.state = self._FakeState()
        self.event = Event("Test Party")

    def test_url_includes_key_and_defaults(self):
        url = self.event.generate_recipe_search_url(self.state, "main course")
        self.assertIn("apiKey=TESTKEY", url)
        self.assertIn("type=main+course", url)
        self.assertTrue(url.startswith(
            "https://api.spoonacular.com/recipes/complexSearch?"))

    def test_url_includes_diet_and_intolerance(self):
        self.event.add_diet("vegan")
        self.event.add_intolerance("soy")
        url = self.event.generate_recipe_search_url(self.state)
        self.assertIn("diet=vegan", url)
        self.assertIn("intolerances=soy", url)

    def test_url_omits_empty_filters(self):
        url = self.event.generate_recipe_search_url(self.state)
        self.assertNotIn("diet=", url)
        self.assertNotIn("intolerances=", url)


if __name__ == "__main__":
    unittest.main()
