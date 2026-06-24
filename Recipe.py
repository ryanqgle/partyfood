class Recipe:

    def __init__(self, name, ingredients, id):
        """ Initializes an Event """
        self.name = name
        self.ingredients = ingredients
        self.id = id

    def display(self):
        print(self.name)
        print("Ingredients: ")
        for ingredient in self.ingredients:
            print(ingredient)