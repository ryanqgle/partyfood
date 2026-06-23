class MenuItem:

    def __init__(prompt_char, title, func):
        '''
        Initializes MenuItem
        Args:
            prompt_char: Single-character menu selection key.
            title: Display name of the command.
            func: The function that will run if selected.
        '''
        self.prompt_char = prompt_char
        self.title = title
        self.func = func

    def get_prompt_char(): return self.prompt_char

    def display():
        '''
        To be used when displaying this item as an option
        under another menu
        '''
        print(f"[{self.prompt_char}] {self.title}")

    def select():
        if self.func:
            return self.func()
        else:
            print(f"No action defined for {self.title}")
