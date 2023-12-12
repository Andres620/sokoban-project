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

    def step(self) -> None:
        if self.path is None:  # Solo ejecutar el algoritmo si no hay un camino calculado.
            self.calculate_path()
        if self.expansion_nodes:  # Si hay nodos de expansion, los crea (Esto quitarlo para no dibjar nodos expansion solo el cmaino)
            self.model.create_expansion_agents([self.expansion_nodes.pop(0)], self.order_counter)
            self.order_counter += 1

            if not bool(self.expansion_nodes):
                self.model.change_color_path(self.path)

        if self.is_algorithm_finished():
            self.move()
        # if self.path is None:  # Solo ejecutar el algoritmo si no hay un camino calculado.
        #     self.calculate_path()
        # if self.expansion_nodes:  # Si hay nodos de expansion, los crea
        #     self.model.create_expansion_agents([self.expansion_nodes.pop(0)])
        # self.move()

    def move(self) -> None:
        if self.path:
            if not hasattr(self, 'path_copy'):  # Verifica si la copia ya se ha hecho
                self.path_copy = self.path.copy()

            new_position = self.path_copy.pop(0)
            self.model.grid.move_agent(self, new_position)

            if not self.path_copy:
                self.is_move_finished = True
                print("Ruta terminada")
                del self.path_copy
        else:
            self.is_move_finished = True
        # if self.path:
        #     new_position = self.path.pop(0)
        #     self.model.grid.move_agent(self, new_position)
        # else:
        #     print("Ruta terminada")

    def calculate_path(self):
        self.path, self.expansion_nodes = self.algorithm.search(self.pos, self.model.get_goal_position()) #Cambiar para que se ejecute desde la posicion inicial deel robot
        print("Posicion demeta: ", self.assigned_goal.pos)
        print("Ruta del algoritmo:", self.path)
        print("Nodos de expansion:", self.expansion_nodes)

    def is_valid_move(self, target_position):
        if not self.model.grid.out_of_bounds(target_position):
            cell_contents = self.model.grid.get_cell_list_contents(target_position)
            # Verifica si la casilla de destino está vacía o no contiene una pared.
            for content in cell_contents:
                if isinstance(content, WallAgent):
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
