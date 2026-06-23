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
        print(f"Available Ingredients: {', '.join(self.ingredients) if self.ingredients else 'None'}")
        print(f"Diets: {', '.join(self.diets) if self.diets else 'None'}")
        print(f"Intolerances: {', '.join(self.intolerances) if self.intolerances else 'None'}")
        print(f"Saved Recipes: {', '.join(self.saved_recipes) if self.saved_recipes else 'None'}")
    
    # diets
    def add_diet(self, diet):
        assert(isinstance(diet, String))
        self.diets.add(diet)
    
    def remove_diet(self, diet):
        assert(isinstance(diet, String))
        self.diets.remove(diet)
    
    # intolerances
    def add_intolerance(self, intolerance):
        assert(isinstance(intolerance, String))
        self.intolerances.add(diet)
    
    def remove_intolerance(self, intolerance):
        assert(isinstance(intolerance, String))
        self.intolerances.remove(intolerance)

    # ingredients
    def add_ingredient(self, ingredient):
        assert(isinstance(ingredient, String))
        self.ingredients.add(diet)
    
    def remove_ingredient(self, ingredient):
        assert(isinstance(ingredient, String))
        self.ingredients.remove(ingredient)

    # attendees
    def set_attendees(self, count):
        assert(isinstance(count, int))
        self.attendee_count = count