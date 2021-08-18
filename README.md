# Process Controller Simulator

A simulation framework, on which models, processes and controllers can be easily, flexibly and concurrently simulated. 
Includes automatic real-time visualization of process variables and an interactive CLI.
Intended for educational use, for people interested in learning about modelling, simulation, control and optimization. 

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. 

### Running the example

This example will run a Continuous Stirred Tank Reactor (CSTR) model. A MPC Controller will aim to steer the manipulated variables in order to reach the control objectives (maximizing product yield). The example model is available [here](examples/cstr/CSTRModel.py), the controller is defined [here](controller/MPCController.py).

```
#Install Dependencies
pip install  dash pandas scipy numpy

#Clone the project
git clone https://github.com/marianaipmonteiro/ProcessControllerSimulator

#Change into project directory
cd ProcessControllerSimulator

#Run Main, which will run our example
python3 Main.py
```

### Visualization

Connecting to **localhost:8050** should present the automatic real-time visualization of process variables:

![data-viz](https://i.postimg.cc/bNQv48z8/data-viz.png)

### CLI Interaction

A CLI is provided which allows several interactions with the running simulation:

```bash
# Help message
Commands:
            print world - Prints the state of the world.
            perturb <var> <value> - Perturbs variable <var> by the decimal amount <value>, positive or negative.
            help - Prints this message.
            exit - Exits the program.
```

## Computational Model

The main abstractions in the framework are that of a [WorldState](simulation/WorldState.py), which contains the current state of the world (constants and variables). A [Simulation](simulation/Simulation.py) owns a list of WorldStates, and will use a [WorldInitializer](simulation/WorldInitializer.py) to create the initial world, providing definitions for constants and variables. A Simulation is initialized by providing it with a number of [SimulatedSystems](simulation/SimulatedSystem.py). 

Each SimulatedSystem is instantiated by the Simulation, and runs a simulation loop on a separate thread. This loop will periodically poll the WorldState list, obtaining the most recent WorldState, which is used by the SimulatedSystem to compute a new WorldState, and appending it to the WorldState list, thus progressing the state of the world. A simple lock is used to provide exclusive acess during accesses to the world state list, but users are abstracted from that.

Both [Models](model/Model.py) and [Controllers](controller/Controller.py) are SimulatedSystems, with specific simulation loops. To create a model, users may extend either [Model.py](model/Model.py) or [SelfInitializingModel.py](model/SelfInitializingModel.py) (which is both a Model and a WorldInitializer). An example Controller is provided in the form of an [MPC Controller](controller/MPCController.py).

Visualization is achieved by periodically rendering the values of a variable in all the WorldStates over time.

## TO-DO

- [x] Flexible Simulation Framework
- [x] Initial Examples
- [x] Visualization
- [x] Logging
- [ ] Figure out why Data Visualizer takes so long
- [ ] GUI for Simulation Customization
- [ ] Reinforcement Learning Controller Framework
- [ ] Surrogate Model Framework
- [ ] Benchmarks
- [ ] Documentation
- [ ] Testing

## Authors
Mariana Monteiro - @marianaipmonteiro - Modelling the CSTR, implementing MPC strategy, computational model.

Pedro Silvestre - @PSilvestre - Computational model.


