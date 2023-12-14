from mesa import Agent

from agents.wallAgent import WallAgent
from algorithms.uninformed.BFS import BFS


class RobotAgent(Agent):
    def __init__(self,unique_id, model, algorithm):
        super().__init__(unique_id, model)
        self.algorithm = algorithm
        self.path = None
        self.expansion_nodes = None
        self.order_counter = 1
        self.robot_move_finished = False
        self.assigned_box = None # Atributo para almacenar la caja asignada

    def step(self) -> None:
        pass


    def move(self) -> None:
        pass

    def calculate_path(self):
        self.path, self.expansion_nodes = self.algorithm.search(self.pos, self.model.get_goal_position()) #Cambiar para que se ejecute desde la posicion inicial deel robot
        print("Posicion demeta: ", self.model.get_goal_position())
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

    def is_robot_move_finished(self):
        return self.robot_move_finished

    def set_assigned_box(self, box):
        self.assigned_box = box
