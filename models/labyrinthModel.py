from mesa import Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
import mesa

from agents.boxAgent import BoxAgent
from agents.goalAgent import GoalAgent
from agents.pathAgent import PathAgent
from agents.robotAgent import RobotAgent
from agents.searchExplorerAgent import SearchExplorerAgent
from agents.wallAgent import WallAgent
from algorithms.algorithmFactory import AlgorithmFactory


class LabyrinthModel(Model):
    def __init__(self, number_of_agents, algorithm_choice, map, width, height):
        print(algorithm_choice)
        unique_id = 0
        self.num_agents = number_of_agents
        self.map = map
        self.grid = MultiGrid(width, height, torus=False)
        self.algorithm = AlgorithmFactory.create_algorithm(algorithm_choice, grid=self.grid, heuristic_function=None)
        self.schedule = RandomActivation(self)
        self.algorithms_finished = False
        self.running = True

        for agent_type, coordinates in map.items():
            for coordinate in coordinates:
                y, x = coordinate
                y = height - y - 1
                if agent_type == 'R':
                    newAgent = WallAgent(unique_id, self)
                elif agent_type == 'C':
                    newAgent = PathAgent(unique_id, self)
                elif agent_type == 'A':
                    newAgent = RobotAgent(unique_id, self, self.algorithm)
                elif agent_type == 'B':
                    newAgent = BoxAgent(unique_id, self)
                elif agent_type == 'M':
                    newAgent = GoalAgent(unique_id, self)

                self.schedule.add(newAgent)
                self.grid.place_agent(newAgent, (x, y))
                unique_id += 1

    def step(self) -> None:
        self.schedule.step()
        if not self.algorithms_finished:
            # Verifica si todos los agentes han terminado sus algoritmos
            all_robot_agents_finished = all(
                agent.is_algorithm_finished() for agent in self.schedule.agents if isinstance(agent, RobotAgent))

            if all_robot_agents_finished:
                self.algorithms_finished = True
                self.running = False  # Detiene la simulación
