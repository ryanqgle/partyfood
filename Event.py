from urllib.parse import urlencode
import sqlalchemy as db


class Event:

    def __init__(self, name, attendee_count=0, id=None, engine=None):
        """ Initializes an Event """
        self.name = name
        self.attendee_count = attendee_count
        self.ingredients = set()
        self.diets = set()
        self.intolerances = set()
        self.saved_recipes = set()
        self.id = id          # db primary key; None until the event is saved
        self.engine = engine  # shared engine; None disables db writes

    def _write(self, sql, **params):
        """
        Runs a write against the db for this event.

        No-op when the event isn't persisted yet (no id) or has no engine
        (e.g. while it's being loaded from the db), so an in-memory event
        stays usable on its own and loading doesn't re-insert its rows.
        """
        if self.id is None or self.engine is None:
            return

        with self.engine.begin() as conn:  # begin() commits on success
            conn.execute(db.text(sql), {"id": self.id, **params})

    def _rewrite_ingredients(self):
        # Replaces this event's ingredient rows with the current set.
        # The ingredients table stores one comma-joined string per event,
        # so the simplest correct update for an add or remove is to
        # rewrite the row.

        if self.id is None or self.engine is None:
            return
        with self.engine.begin() as conn:
            conn.execute(
                db.text("DELETE FROM ingredients WHERE event_id = :id"),
                {"id": self.id},
            )
            if self.ingredients:
                conn.execute(
                    db.text(
                        "INSERT INTO ingredients (event_id, event_ingredients)"
                        "VALUES (:id, :ingredients)"
                    ),
                    {"id": self.id, "ingredients": ",".join(self.ingredients)},
                )

    def display(self):
        print("\n~ " + self.name + " ~")
        print(f"Number of Attendees: {self.attendee_count}")

        # ingredients_string = (
        #     ', '.join(self.ingredients)
        #     if self.ingredients
        #     else 'None'
        # )
        # print(f"Available Ingredients: {ingredients_string}")

        diets_string = (
            ', '.join(self.diets)
            if self.diets
            else 'None'
        )
        print(f"Diets: {diets_string}")

        intolerances_string = (
            ', '.join(self.intolerances)
            if self.intolerances
            else 'None'
        )
        print(f"Intolerances: {intolerances_string}")

        saved_recipes_string = (
            ', '.join(recipe.name for recipe in self.saved_recipes)
            if self.saved_recipes
            else 'None'
        )
        print(f"Saved Recipes: {saved_recipes_string}")

    def set_name(self, name):
        self.name = name
        self._write("UPDATE events SET event_name = :name WHERE id = :id",
                    name=name)

    # diets
    def add_diet(self, diet):
        if not isinstance(diet, str):
            print("Error adding diet. Invalid input.")
            return

        self.diets.add(diet.strip().lower())
        self._write(
            "INSERT INTO event_diets (event_id, diet) VALUES (:id, :diet)",
            diet=diet)

    def remove_diet(self, diet):
        if not isinstance(diet, str):
            print("Error removing diet. Invalid input.")
            return

        self.diets.remove(diet)
        self._write(
            "DELETE FROM event_diets WHERE event_id = :id AND diet = :diet",
            diet=diet)

    # intolerances
    def add_intolerance(self, intolerance):
        if not isinstance(intolerance, str):
            print("Error adding intolerance. Invalid input.")
            return
        self.intolerances.add(intolerance.strip().lower())
        self._write(
            "INSERT INTO event_intolerances (event_id, intolerance) "
            "VALUES (:id, :intolerance)",
            intolerance=intolerance)

    def remove_intolerance(self, intolerance):
        if not isinstance(intolerance, str):
            print("Error removing intolerance. Invalid input.")
            return
        self.intolerances.remove(intolerance)
        self._write(
            "DELETE FROM event_intolerances "
            "WHERE event_id = :id AND intolerance = :intolerance",
            intolerance=intolerance)

    # ingredients
    def add_ingredient(self, ingredient):
        if not isinstance(ingredient, str):
            print("Error adding ingredient. Invalid input.")
            return
        self.ingredients.add(ingredient)
        self._rewrite_ingredients()

    def remove_ingredient(self, ingredient):
        if not isinstance(ingredient, str):
            print("Error ingredient diet. Invalid input.")
            return
        self.ingredients.remove(ingredient)
        self._rewrite_ingredients()

    def modify_ingredients(self, ingredients_raw, mode=0):
        ingredients = []
        for i in ingredients_raw.split(","):
            if i.strip():
                ingredients.append(i.strip().lower())

        for ingredient in ingredients:
            if mode == 0:
                self.add_ingredient(ingredient)
            else:
                self.remove_ingredient(ingredient)

    # attendees
    def update_attendees(self, count):
        if not isinstance(count, int) or count < 0:
            print("Invalid input. Attendee" +
                  " count should be a positive integer.")
            return

        self.attendee_count = count
        self._write(
            "UPDATE events SET attendee_count = :count WHERE id = :id",
            count=count)

    def generate_recipe_search_url(self, state, meal_type=""):
        """
        Generates a URL for Spoonacular to be able to find recipes that
        are compatible with the event's associated diets and intolerances
        as well as the type of meal, if provided.

        Args:
            state: Global state
            meal_type: Differentiator between main dish, appetizer, etc
        """
        params = {}

        if self.diets:
            params["diet"] = ",".join(self.diets)

        if self.intolerances:
            params["intolerances"] = ",".join(self.intolerances)

        if meal_type:
            params["type"] = meal_type

        # we arbitrarily decide to only take 1 result for api rate
        params["number"] = 2

        params["apiKey"] = state.spoonacular_key

        url = ("https://api.spoonacular.com/recipes/complexSearch?" +
               urlencode(params))

        return url

    def add_recipe(self, recipe, category=None, estimated_cost=None):
        """
        Adds a recipe to this event and also updates the database.

        Args:
            recipe: Recipe object to be added
            category: The meal type (like appetizer, main dish, dessert)
        """
        if recipe in self.saved_recipes:
            return

        self.saved_recipes.add(recipe)
        ingredients = ",".join(recipe.ingredients)

        if self.id is None or self.engine is None:
            return

        with self.engine.begin() as conn:
            conn.execute(
                db.text("""
                    INSERT INTO event_recipes
                        (event_id,
                        recipe_id,
                        recipe_name,
                        category,
                        estimated_cost,
                        ingredients)
                    VALUES
                        (:event_id,
                        :recipe_id,
                        :recipe_name,
                        :category,
                        :estimated_cost,
                        :ingredients)
                    """),
                {
                    "event_id": str(self.id),
                    "recipe_id": str(recipe.id),
                    "recipe_name": recipe.name,
                    "category": category,
                    "estimated_cost": estimated_cost,
                    "ingredients": ingredients
                }
            )
