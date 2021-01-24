from decimal import Decimal
from simulation import Simulation


class Console:
    def __init__(self, simulation: Simulation):
        self.simulation = simulation
        self.running = simulation.running
        self.world_states_lock = simulation.world_states_lock
        self.world_states = simulation.world_states

    def trap(self):
        while self.running.is_running():
            user_input = input("Type command: ")
            self.process_user_input(user_input.strip())

    def process_user_input(self, user_input):
        if user_input == "exit":
            self.running.stop()
        elif user_input == "print world":
            self.print_world()
        elif user_input.startswith("perturb"):
            self.perturb(user_input)
        elif user_input.startswith("tov"):
            self.toggle_optimisation_variable(user_input)
        else:
            self.print_help()

    def print_world(self):
        world_state = self.get_latest_world()
        print(world_state)

    def get_latest_world(self):
        self.world_states_lock.acquire()
        world_state = self.world_states[-1]
        self.world_states_lock.release()
        return world_state

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

    def print_help(self):
        help_msg = """
        Commands:
            print world - Prints the state of the world.
            perturb <var> <value> - Perturbs variable <var> by the decimal amount <value>, positive or negative.
            help - Prints this message.
            #todo
            exit - Exits the program.
        """
        print(help_msg)

    def toggle_optimisation_variable(self, user_input):
        #todo
        pass
