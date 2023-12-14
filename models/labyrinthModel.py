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
        self.algorithm = AlgorithmFactory.create_algorithm(algorithm_choice, grid=self.grid,
                                                           heuristic_function=heuristic_choice,
                                                           priority_order=[(0, -1), (0, 1), (-1, 0), (1, 0)])
        self.schedule = RandomActivation(self)
        self.algorithms_finished = False
        self.goal_position = None
        self.running = True

        agents_to_assign = []  # Lista para almacenar las cajas que necesitan asignación
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
                    agents_to_assign.append(newAgent)  # Añade la caja a la lista para asignación
                elif agent_type == 'M':
                    newAgent = GoalAgent(self.unique_id, self)
                    self.goal_position = (x, y)

                self.schedule.add(newAgent)
                self.grid.place_agent(newAgent, (x, y))
                self.unique_id += 1

        # Asigna robots y metas después de crear todos los agentes
        print('agents_to_assign', agents_to_assign)

        for box in agents_to_assign:
            box.assigned_robot = self.assign_robot_to_box(box)
            box.assigned_goal = self.assign_goal_to_box(box)
            print('box: ', box.pos)

            # Asigna la caja a los agentes Robot y Meta
            if box.assigned_robot:
                box.assigned_robot.set_assigned_box(box)
                print('assigned robot: ', box.assigned_robot.pos)
            if box.assigned_goal:
                box.assigned_goal.set_assigned_box(box)
                print('assigned goal: ', box.assigned_goal.pos)

    def step(self) -> None:
        # Obtener todos los agentes de caja
        box_agents = [agent for agent in self.schedule.agents if isinstance(agent, BoxAgent)]

        # Filtrar los agentes que aún no han terminado su algoritmo o movimiento
        active_box_agents = [agent for agent in box_agents if
                             not agent.is_algorithm_finished() or not agent.is_box_move_finished()]

        # Verificar si hay agentes activos
        if active_box_agents:
            # Seleccionar el primer agente activo
            active_agent = active_box_agents[0]

            # Ejecutar el paso del agente activo
            active_agent.step()

            # Verificar si el agente activo ha terminado su movimiento
            if active_agent.is_move_finished:
                # Eliminar al agente activo de la lista de agentes activos
                active_box_agents.remove(active_agent)

        # Verificar si todos los agentes han terminado
        all_box_agents_finished = all(
            agent.is_algorithm_finished() and agent.is_box_move_finished() for agent in box_agents)

        if all_box_agents_finished:
            self.algorithms_finished = True
            self.running = False  # Detener la simulación

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

    def assign_robot_to_box(self, box):
        robots = [agent for agent in self.schedule.agents if
                  isinstance(agent, RobotAgent) and agent.assigned_box is None]
        if not robots:
            return None  # Si no hay robots no asignados, no se puede asignar ninguno
        # Encuentra el robot más cercano que no esté asignado a una caja
        closest_robot = min(robots, key=lambda robot: self.calculate_distance(box.pos, robot.pos))
        return closest_robot

    def assign_goal_to_box(self, box):
        goals = [agent for agent in self.schedule.agents if isinstance(agent, GoalAgent) and agent.assigned_box is None]
        if not goals:
            return None  # Si no hay metas no asignadas, no se puede asignar ninguna
        # Encuentra la meta más cercana que no esté asignada a una caja
        closest_goal = min(goals, key=lambda goal: self.calculate_distance(box.pos, goal.pos))
        return closest_goal

    @staticmethod
    def calculate_distance(pos1, pos2):
        return abs(pos2[0] * 10 - pos1[0] * 10) + abs(pos2[1] * 10 - pos1[1] * 10)
