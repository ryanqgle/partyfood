class Menu:

    def __init__(self, title, options=None):
        """
        Initializes Menu object
        Args:
            title: Display name of the menu.
            options: Dictionary mapping prompt characters to
                Menu or MenuCommand objects.
        """
        self.title = title
        self.options = options or {}

    def display(self):
        """
        Display this menu's options
        """
        print(f"==== {self.title} Menu ====")
        for item in self.options.values():
            item.display()


    def select(self, choice):
        """
        Prompts user to select from the options in the menu
        """
        selected = self.options.get(choice) #makes sure the promptchar exists in our options

        if selected:
            return selected
        else:
            print ("Invalid choice")
            return None
