from urllib.parse import urlencode


class Event:

    def __init__(self, name, attendee_count=0):
        """ Initializes an Event """
        self.name = name
        self.attendee_count = attendee_count
        self.ingredients = set()
        self.diets = set()
        self.intolerances = set()
        self.saved_recipes = set()

    def display(self):
        print(self.name)
        print(f"Number of Attendees: {self.attendee_count}")

        ingredients_string = (
            ', '.join(self.ingredients)
            if self.ingredients
            else 'None'
        )
        print(f"Available Ingredients: {ingredients_string}")

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
            ', '.join(self.saved_recipes)
            if self.saved_recipes
            else 'None'
        )
        print(f"Saved Recipes: {saved_recipes_string}")

    def set_name(self, name):
        state.current_event.name = name
        # TODO: update db

    # diets
    def add_diet(self, diet):
        assert isinstance(diet, str)
        self.diets.add(diet.strip().lower())
        # TODO: update db

    def remove_diet(self, diet):
        assert isinstance(diet, str)
        self.diets.remove(diet)
        # TODO: update db

    # intolerances
    def add_intolerance(self, intolerance):
        assert isinstance(intolerance, str)
        self.intolerances.add(intolerance.strip().lower())
        # TODO: update db

    def remove_intolerance(self, intolerance):
        assert isinstance(intolerance, str)
        self.intolerances.remove(intolerance)
        # TODO: update db

    # ingredients
    def add_ingredient(self, ingredient):
        assert isinstance(ingredient, str)
        self.ingredients.add(ingredient)
        # TODO: update db

    def remove_ingredient(self, ingredient):
        assert isinstance(ingredient, str)
        self.ingredients.remove(ingredient)
        # TODO: update db

    def modify_ingredients(self, ingredients_raw):
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
        assert isinstance(count, int)
        self.attendee_count = count
        # TODO: update db

    def generate_recipe_search_url(self, state, meal_type=""):
        params = {}

        if self.diets:
            params["diet"] = ",".join(self.diets)

        if self.intolerances:
            params["intolerances"] = ",".join(self.intolerances)
        
        if meal_type:
            params["type"] = meal_type

        params["number"] = 3  # we arbitrarily decide to only take 3 results
        params["apiKey"] = state.spoonacular_key

        url = "https://api.spoonacular.com/recipes/complexSearch?" + urlencode(params)

        return url