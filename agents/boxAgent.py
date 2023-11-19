from mesa import Agent

from agents.wallAgent import WallAgent


class BoxAgent(Agent):
    def __init__(self,unique_id, model, algorithm):
        super().__init__(unique_id, model)
        self.algorithm = algorithm
        self.path = None
        self.expansion_nodes = None

    def step(self) -> None:
        pass
        # if self.path is None:  # Solo ejecutar el algoritmo si no hay un camino calculado.
        #     self.calculate_path()
        # if self.expansion_nodes:  # Si hay nodos de expansion, los crea
        #     self.model.create_expansion_agents([self.expansion_nodes.pop(0)])
        # self.move()

    def move(self) -> None:
        pass
        # if self.path:
        #     new_position = self.path.pop(0)
        #     self.model.grid.move_agent(self, new_position)
        # else:
        #     print("Ruta terminada")

    def is_valid_move(self, target_position):
        if not self.model.grid.out_of_bounds(target_position):
            cell_contents = self.model.grid.get_cell_list_contents(target_position)
            # Verifica si la casilla de destino está vacía o no contiene una pared.
            for content in cell_contents:
                if isinstance(content, WallAgent):
                    return False  # No es un movimiento válido si hay una pared.
            return True  # Es un movimiento válido si la casilla de destino está vacía.
        return False  # No es un movimiento válido

    def calculate_path(self):
        self.path, self.expansion_nodes = self.algorithm.search(self.pos, self.model.get_goal_position()) #Cambiar para que se ejecute desde la posicion inicial deel robot
        print("Ruta del algoritmo:", self.path)
        print("Nodos de expansion:", self.expansion_nodes)

    def is_algorithm_finished(self):
        return not bool(self.path) and not bool(self.expansion_nodes)
