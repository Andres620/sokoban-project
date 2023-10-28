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


class LabyrinthModel(Model):
    def __init__(self, number_of_agents, map, width, height):
        unique_id = 0
        self.num_agents = number_of_agents
        self.map = map
        self.grid = MultiGrid(width, height, torus=False)
        self.schedule = RandomActivation(self)

        for agent_type, coordinates in map.items():
            for coordinate in coordinates:
                y, x = coordinate
                y = height - y - 1
                if agent_type == 'R':
                    newAgent = WallAgent(unique_id, self)
                elif agent_type == 'C':
                    newAgent = PathAgent(unique_id, self)
                elif agent_type == 'A':
                    newAgent = RobotAgent(unique_id, self)
                elif agent_type == 'B':
                    newAgent = BoxAgent(unique_id, self)
                elif agent_type == 'M':
                    newAgent = GoalAgent(unique_id, self)

                self.schedule.add(newAgent)
                self.grid.place_agent(newAgent, (x, y))
                unique_id += 1


    def step(self) -> None:
        self.schedule.step()
