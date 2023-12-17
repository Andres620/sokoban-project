from mesa import Agent

from agents.wallAgent import WallAgent


class BoxAgent(Agent):
    def __init__(self,unique_id, model, algorithm):
        super().__init__(unique_id, model)
        self.algorithm = algorithm
        self.path = None
        self.expansion_nodes = None
        self.assigned_robot = None  # Atributo para almacenar el robot asignado
        self.assigned_goal = None    # Atributo para almacenar la meta

        self.is_move_finished = False
        self.order_counter = 1
        self.has_collision = False
        self.collision_agent = None
        self.free_position = None
        self.push_position = None
        self.new_position = None

    def step(self) -> None:
        if self.path is None:  # Solo ejecutar el algoritmo si no hay un camino calculado.
            self.calculate_path()
            self.path = self.path[1:]
        # if self.expansion_nodes:  # Si hay nodos de expansion, los crea (Esto quitarlo para no dibjar nodos expansion solo el cmaino)
        #     self.model.create_expansion_agents([self.expansion_nodes.pop(0)], self.order_counter)
        #     self.order_counter += 1
        #
        # if not bool(self.expansion_nodes):
        #     self.model.change_color_path(self.path)
        #
        # if self.is_algorithm_finished():
        self.move()

    def move(self) -> None:
        if self.path:
            self.new_position = self.path[0]
            self.push_position = self.get_push_position(self.new_position) # Posición donde el robot debe ir para empujarl a caja
            print('pos: {}   push pos: {}'.format(self.new_position, self.push_position))
            # Verificar si hay colisión en la nueva posición
            collision_agents = self.model.grid.get_cell_list_contents(self.new_position)

            from agents.robotAgent import RobotAgent
            if any(isinstance(agent, BoxAgent) for agent in collision_agents if agent != self):
                # Hay una colisión, intentar mover el agente colisionado a una posición libre
                for agent in collision_agents:
                    if isinstance(agent, BoxAgent):
                        self.has_collision = True
                        self.collision_agent = agent
                        self.free_position = self.find_free_position(agent, self.path)
                        self.collision_agent.path, self.collision_agent.expansion_nodes = self.algorithm.search(
                                                                                        agent.pos, self.free_position)
                        self.collision_agent.path = self.collision_agent.path[1:]

            elif any(isinstance(agent, RobotAgent) for agent in collision_agents if agent != self):
                for agent in collision_agents:
                    if isinstance(agent, RobotAgent):
                        self.free_position = agent.find_free_position(self.path)
                        self.model.grid.move_agent(agent, self.free_position)

        else:
            self.path = None
            self.is_move_finished = True
            self.push_position = None
            print("Ruta terminada")

    def push(self):
        self.new_position = self.path.pop(0)
        self.model.grid.move_agent(self, self.new_position)

    def find_free_position(self, agent, active_agent_path):
        # Implementar lógica para encontrar la posición libre más cercana y empujable
        max_radius = 5  # Puedes ajustar el radio máximo según sea necesario

        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]  # Movimientos ortogonales

        for radius in range(1, max_radius + 1):
            for direction in directions:
                new_position = (agent.pos[0] + radius * direction[0], agent.pos[1] + radius * direction[1])

                # Verificar si la nueva posición está fuera del path del activeAgent
                if new_position not in active_agent_path and self.is_valid_move(new_position):
                    # Verificar si la nueva posición es empujable
                    path, _ = self.algorithm.search(new_position, agent.assigned_goal.pos)
                    if path:
                        return new_position

        # Si no se encuentra una posición válida, devolver la posición original
        return agent.pos

    def get_push_position(self, next_step):
        """
        Calcula la posición donde el BoxAgent debe estar para ser empujado en la dirección del próximo paso.
        :param next_step: La próxima posición en el camino del BoxAgent.
        :return: La posición a la que el BoxAgent debería moverse para ser empujado correctamente.
        """
        current_position = self.pos

        # Calcula la dirección del próximo paso
        direction = (next_step[0] - current_position[0], next_step[1] - current_position[1])

        # Calcula la posición opuesta en esa dirección
        push_position = (current_position[0] - direction[0], current_position[1] - direction[1])

        return push_position

    def calculate_path(self):
        self.path, self.expansion_nodes = self.algorithm.search(self.pos, self.assigned_goal.pos) #Cambiar para que se ejecute desde la posicion inicial deel robot
        print("Posicion demeta: ", self.assigned_goal.pos)
        print("Ruta del algoritmo:", self.path)
        print("Nodos de expansion:", self.expansion_nodes)

    def is_valid_move(self, target_position):
        if not self.model.grid.out_of_bounds(target_position):
            cell_contents = self.model.grid.get_cell_list_contents(target_position)
            # Verifica si la casilla de destino está vacía o no contiene una pared.
            for content in cell_contents:
                if isinstance(content, WallAgent) or isinstance(content, BoxAgent):
                    return False  # No es un movimiento válido si hay una pared.
            return True  # Es un movimiento válido si la casilla de destino está vacía.
        return False  # No es un movimiento válido

    def is_algorithm_finished(self):
        return not bool(self.expansion_nodes)

    def is_box_move_finished(self):
        return self.is_move_finished

    def set_assigned_goal(self, goal):
        self.assigned_goal = goal

    def set_assigned_robot(self, robot):
        self.assigned_robot = robot
