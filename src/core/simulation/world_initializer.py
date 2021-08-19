from .world_state import WorldState


class WorldInitializer:
    """
    Specifies how to create the initial WorldState
    """

    def __init__(self):
        pass

    def create_initial_world(self) -> WorldState:
        raise Exception(
            "WorldInitializer " + str(self.__class__) + " does not implement create_initial_world() function")

    def __str__(self):
        return self.__class__.__name__
