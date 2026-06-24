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

    # diets
    def add_diet(self, diet):
        assert isinstance(diet, str)
        self.diets.add(diet)
        # TODO: update db

    def remove_diet(self, diet):
        assert isinstance(diet, str)
        self.diets.remove(diet)
        # TODO: update db

    # intolerances
    def add_intolerance(self, intolerance):
        assert isinstance(intolerance, str)
        self.intolerances.add(intolerance)
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

    # attendees
    def update_attendees(self, count):
        assert isinstance(count, int)
        self.attendee_count = count
        # TODO: update db
