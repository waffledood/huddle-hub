class InvalidUserActionException(Exception):
    def __init__(self, message="Organizer can't RSVP for their own Event."):
        super().__init__(message)

    def __str__(self):
        return f"{self.args[0]}"