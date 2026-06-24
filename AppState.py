class AppState:
    """
    Holds shared state
    """

    def __init__(self):
        self.current_event = None
        self.events = []

    def set_current_event(self, event):
        self.current_event = event
    
    def set_engine(self, engine):
        self.engine = engine
