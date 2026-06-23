class Event:

    def __init__(self, name, attendee_count=0):
        """ Initializes an Event """
        self.name = name
        self.attendee_count = attendee_count
        self.ingredients = set()
        self.diets = set()
        self.intolerances = set()
        self.saved_recipes = set()
