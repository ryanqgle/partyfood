class AppState:
    """
    Holds shared state
    """

    def __init__(self):
        self.current_event = None

    def set_current_event(self, event):
        self.current_event = event
