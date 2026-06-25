class Recipe:

    def __init__(self, name, ingredients, id):
        """ Initializes an Event """
        self.name = name
        self.ingredients = ingredients
        self.id = id

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        if not isInstance(other, Recipe):
            return NotImplemented
        return self.id == other.id

    def display(self):
        print("\n" + self.name)
        print("Ingredients: ")
        for ingredient in self.ingredients:
            print("- " + ingredient)
