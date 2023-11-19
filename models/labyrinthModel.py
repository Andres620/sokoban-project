from mesa import Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
import mesa

from agents.boxAgent import BoxAgent
from agents.goalAgent import GoalAgent
from agents.pathAgent import PathAgent
from agents.robotAgent import RobotAgent
from agents.expansionAgent import ExpansionAgent
from agents.wallAgent import WallAgent
from algorithms.algorithmFactory import AlgorithmFactory


class LabyrinthModel(Model):
    def __init__(self, number_of_agents, algorithm_choice, heuristic_choice, map, width, height):
        print(algorithm_choice)
        print(heuristic_choice)
        self.unique_id = 0
        self.num_agents = number_of_agents
        self.map = map
        self.grid = MultiGrid(width, height, torus=False)
        self.algorithm = AlgorithmFactory.create_algorithm(algorithm_choice, grid=self.grid, heuristic_function=heuristic_choice)
        self.schedule = RandomActivation(self)
        self.algorithms_finished = False
        self.goal_position = None
        self.running = True

        for agent_type, coordinates in map.items():
            for coordinate in coordinates:
                y, x = coordinate
                y = height - y - 1
                if agent_type == 'R':
                    newAgent = WallAgent(self.unique_id, self)
                elif agent_type == 'C':
                    newAgent = PathAgent(self.unique_id, self)
                elif agent_type == 'A':
                    newAgent = RobotAgent(self.unique_id, self, self.algorithm)
                elif agent_type == 'B':
                    newAgent = BoxAgent(self.unique_id, self, self.algorithm)
                elif agent_type == 'M':
                    newAgent = GoalAgent(self.unique_id, self)
                    self.goal_position = (x, y)

                self.schedule.add(newAgent)
                self.grid.place_agent(newAgent, (x, y))
                self.unique_id += 1

    def step(self) -> None:
        self.schedule.step()
        if not self.algorithms_finished:
            # Verifica si todos los agentes han terminado sus algoritmos
            all_robot_agents_finished = all(
                agent.is_algorithm_finished() for agent in self.schedule.agents if isinstance(agent, RobotAgent))

            if all_robot_agents_finished:
                self.algorithms_finished = True
                self.running = False  # Detiene la simulación

    def create_expansion_agents(self, expansion_nodes, order_counter):
        for node_position in expansion_nodes:
            y, x = node_position
            expansion_agent = ExpansionAgent(self.unique_id, self, order_counter)
            self.schedule.add(expansion_agent)
            self.grid.place_agent(expansion_agent, node_position)
            self.unique_id += 1

    def change_color_path(self, path):
        for agent in self.schedule.agents:
            if isinstance(agent, ExpansionAgent) and agent.pos in path:
                agent.color = "green"


    def get_goal_position(self):
        return self.goal_position
