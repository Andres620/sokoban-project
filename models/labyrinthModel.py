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
        self.active_box_agents = []

        agents_to_assign = []  # Lista para almacenar las cajas que necesitan asignación
        robots_to_assign = []
        goals_to_assign = []
        for agent_type, coordinates in map.items():
            for coordinate in coordinates:
                y, x = coordinate
                y = height - y - 1
                if agent_type == 'R':
                    newAgent = WallAgent(self.unique_id, self)
                elif agent_type == 'C':
                    newAgent = PathAgent(self.unique_id, self)
                elif agent_type == 'A':
                    algorithm = AlgorithmFactory.create_algorithm('BFS', grid=self.grid,
                                                           heuristic_function=heuristic_choice,
                                                           priority_order=[(0, -1), (0, 1), (-1, 0), (1, 0)])
                    newAgent = RobotAgent(self.unique_id, self, algorithm)
                    robots_to_assign.append(newAgent)
                elif agent_type == 'B':
                    newAgent = BoxAgent(self.unique_id, self, self.algorithm)
                    agents_to_assign.append(newAgent)  # Añade la caja a la lista para asignación
                elif agent_type == 'M':
                    newAgent = GoalAgent(self.unique_id, self)
                    goals_to_assign.append(newAgent)
                    self.goal_position = (x, y)

                self.schedule.add(newAgent)
                self.grid.place_agent(newAgent, (x, y))
                self.unique_id += 1

        # Asigna robots y metas después de crear todos los agentes
        print('agents_to_assign', agents_to_assign)

        for robot in robots_to_assign:
            robot.assigned_box = self.assign_box_to_robot(robot)
            print('robot: ', robot.pos)
            if robot.assigned_box:
                robot.assigned_box.set_assigned_robot(robot)
                print('assigned box: ', robot.assigned_box.pos)

        for goal in goals_to_assign:
            goal.assigned_box = self.assign_box_to_goal(goal)
            print('goal: ', goal.pos)
            if goal.assigned_box:
                goal.assigned_box.set_assigned_goal(goal)
                print('assigned box: ', goal.assigned_box.pos)

    def step(self) -> None:
        # Obtener todos los agentes de caja y ordenarlos por posición en x y luego por distancia a la meta
        box_agents = sorted([agent for agent in self.schedule.agents if isinstance(agent, BoxAgent)],
                            key=lambda box: (box.pos[0], self.calculate_distance(box.pos, box.assigned_goal.pos)))

        # Filtrar los agentes que aún no han terminado su algoritmo o movimiento
        # Calcular active_box_agents solo si no está calculado
        if not self.active_box_agents:
            self.active_box_agents = [agent for agent in box_agents if
                                      not agent.is_algorithm_finished() or not agent.is_box_move_finished()]

        continue_active_step = True

        # Verificar si hay agentes activos
        if self.active_box_agents:
            # Seleccionar el primer agente activo
            active_agent = self.active_box_agents[0]

            # Verificar si hay un agente colisionado que necesita moverse completamente
            if active_agent.has_collision:
                collision_agent = active_agent.collision_agent
                active_agent.has_collision = False
                self.active_box_agents.remove(collision_agent)  # Colocar el collision_agent en la posición 0
                self.active_box_agents.insert(0, collision_agent)
                active_agent = self.active_box_agents[0]
                continue_active_step = False

            # Ejecutar el paso del agente activo solo si el collision_agent ha terminado su movimiento
            if continue_active_step:
                active_agent.step()
                active_agent.assigned_robot.step()

            # Verificar si el agente activo ha terminado su movimiento
            if active_agent.is_move_finished:
                # Eliminar al agente activo de la lista de agentes activos
                self.active_box_agents.remove(active_agent)

        # Verificar si todos los agentes han terminado
        all_box_agents_finished = all(
            agent.is_algorithm_finished() and agent.is_box_move_finished() for agent in box_agents)

        if all_box_agents_finished:
            for agent in box_agents:
                if not agent.pos == agent.assigned_goal.pos:
                    agent.is_move_finished = False
                    all_box_agents_finished = False

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

    def assign_box_to_robot(self, robot):
        boxes = [agent for agent in self.schedule.agents if
                 isinstance(agent, BoxAgent) and agent.assigned_robot is None]
        if not boxes:
            return None  # Si no hay robots no asignados, no se puede asignar ninguno
        closest_box = min(boxes, key=lambda box: self.calculate_distance(robot.pos, box.pos))
        return closest_box

    def assign_box_to_goal(self, goal):
        boxes = [agent for agent in self.schedule.agents if
                 isinstance(agent, BoxAgent) and agent.assigned_goal is None]
        if not boxes:
            return None  # Si no hay robots no asignados, no se puede asignar ninguno
        closest_box = min(boxes, key=lambda box: self.calculate_distance(goal.pos, box.pos))
        return closest_box

    @staticmethod
    def calculate_distance(pos1, pos2):
        return abs(pos2[0] * 10 - pos1[0] * 10) + abs(pos2[1] * 10 - pos1[1] * 10)
