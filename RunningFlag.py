

class RunningFlag:
    def __init__(self):
        self.running = True

    def stop(self):
        self.running = False

    def is_running(self):
        return self.running
