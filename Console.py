from decimal import Decimal
from collections import namedtuple
from loading.SimulatedSystemLoader import load_system
from simulation import Simulation

Command = namedtuple("Command", ["cmd", "desc", "handler"])


class Console:
    def __init__(self, simulation: Simulation):
        self.simulation = simulation
        self.world_states_lock = simulation.world_states_lock
        self.world_states = simulation.world_states

        self.CMDS = [
            Command("pw", "print world - prints the world state", self.print_world),
            Command("pv", "perturb variable - pv <variable> +/-<value>", self.perturb),
            Command("tov", "toggle optimization variable - TODO", self.toggle_optimisation_variable),
            Command("ls", "load system - ls <path_to_system> <system_name> <key1=val1>...", self.load_system),
            Command("rs", "remove system - rs <system_name>", self.remove_system),
            Command("help", "prints *this* help message", self.print_help),
            Command("exit", "exits the program", self.exit)
        ]

    def trap(self):
        self.print_help(None)
        while self.simulation.is_running():
            user_input = input(">")
            self.process_user_input(user_input.strip())

    def process_user_input(self, user_input):
        for c in self.CMDS:
            if user_input.startswith(c.cmd):
                c.handler(user_input)

    def print_world(self, user_input):
        world_state = self._get_latest_world()
        print(world_state)

    def perturb(self, user_input):
        user_input_list = user_input.split()
        if len(user_input_list) != 3:
            print("Invalid input, try again using a valid variable name!")
            return

        perturbed_variable = user_input_list[1]
        perturbation = Decimal(float(user_input_list[2]))

        self.world_states_lock.acquire()
        world_state = self.world_states[-1]

        # todo guarantee that variable can be perturbed and is not a constant

        perturbation_dict = {perturbed_variable: world_state[perturbed_variable] + perturbation}

        perturbed_world_state = world_state.apply_assignment(perturbation_dict)
        self.world_states.append(perturbed_world_state)
        self.world_states_lock.release()

    def toggle_optimisation_variable(self, user_input):
        # todo
        pass

    def load_system(self, user_input):
        tokens = user_input.split()
        # First two tokens are "load" and "system"
        path = tokens[2]
        name = tokens[3]

        kwargs = {}
        for token in tokens[4:]:
            token_tokens = token.split("=")
            key = token_tokens[0]
            val = token_tokens[1]
            kwargs[key] = val

        system = load_system(path, kwargs)
        self.simulation.add_system(name, system)

    def remove_system(self, user_input):
        tokens = user_input.split()
        # First two tokens are "remove" and "system"
        name = tokens[2]

        self.simulation.remove_system(name)

    def print_help(self, user_input):  # TODO: put commands in constants
        print("Commands: ")
        for c in self.CMDS:
            print("\t{} - {}".format(c.cmd, c.desc))

    def exit(self, user_input):
        self.simulation.stop()

    def _get_latest_world(self):
        self.world_states_lock.acquire()
        world_state = self.world_states[-1]
        self.world_states_lock.release()
        return world_state
