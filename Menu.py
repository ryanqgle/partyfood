class Menu:

    def __init__(self, prompt_char, title, options=None):
        """
        Initializes Menu object
        Args:
            prompt_char: Single-character menu selection key.
            title: Display name of the menu.
            options: Dictionary mapping prompt characters to
                Menu or MenuCommand objects.
        """

        self.prompt_char = prompt_char
        self.title = title
        self.options = options or {}

    def get_prompt_char(): return self.prompt_char

    def display():
        """
        To be used when displaying this menu as an option
        under another menu
        """
        print(f"[{self.prompt_char}] {self.title}")

    def select():
        """
        Prompts user to select from the options in the menu
        """
        # in original project i did, i had it continuously
        # prompting the user... unsure if i want that here
        print(f"==== {self.title} Menu ====")

        for option in self.options.values:
            option.display()

        # if i want to be able to choose multiple, should i
        # just prompt many times? then print selection at end?
        choice = input("Enter choice: ")

        # need to catch if it's an invalid choice
        selected = self.options.get(choice)

        if selected:
            selected.select()
        else:
            print("Invalid choice")
