import threading
from decimal import Decimal
from typing import List

from RunningFlag import RunningFlag
from WorldState import WorldState
from controller.Controller import Controller
from model.Model import Model
from visualize.Visualizer import Visualizer


class Simulation:

    def __init__(self, controller: Controller, model: Model, controller_fps: int = 1, model_fps: int = 5):
        self.controller = controller
        self.model = model
        self.controller_fps = controller_fps
        self.model_fps = model_fps
        self.world_states: List[WorldState] = []
        self.world_states_lock = threading.Lock()
        self.running = RunningFlag()

    def run(self):
        self.model.run(self.model_fps, self.world_states, self.world_states_lock, self.running)
        # self.controller.run(self.controller_fps, self.world_states, self.world_states_lock, self.running)

        vis = Visualizer(self.world_states, self.world_states_lock)
        vis.start()

        while self.running.is_running():
            user_input = input("Type command: ")
            self.process_user_input(user_input.strip())

    def print_world(self):
        world_state = self.get_latest_world()
        print(world_state)

    def get_latest_world(self):
        self.world_states_lock.acquire()
        world_state = self.world_states[-1]
        self.world_states_lock.release()
        return world_state

    def process_user_input(self, user_input):
        if user_input == "exit":
            self.running.stop()
        elif user_input == "print world":
            self.print_world()
        elif user_input.startswith("perturb"):
            self.perturb(user_input)

    def perturb(self, user_input):
        user_input_list = user_input.split()
        if len(user_input_list) != 3:
            print("Invalid input, try again!")
            return

        perturbed_variable = user_input_list[1]
        perturbance = Decimal(float(user_input_list[2]))

        self.world_states_lock.acquire()
        world_state = self.world_states[-1]

        perturbance_dict = {perturbed_variable: world_state[perturbed_variable] + perturbance}

        perturbed_world_state = world_state.apply_assignment(perturbance_dict)
        self.world_states.append(perturbed_world_state)
        self.world_states_lock.release()
