from mesa import Agent

from agents.wallAgent import WallAgent
from algorithms.uninformed.BFS import BFS


class RobotAgent(Agent):
    def __init__(self,unique_id, model):
        super().__init__(unique_id, model)
        self.priority_order = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        self.algorithm = BFS(self.model.grid, priority_order=[(-1, 0), (0, -1), (1, 0), (0, 1)]) # Izquierda, Arriba, Derecha, Abajo
        self.i = True
        self.path = []


    def step(self) -> None:
        self.move()

    def move(self) -> None:
        if self.i:
            self.path = self.algorithm.search(self.pos, (13, 1))
            print("Ruta del algoritmo:", self.path)
            self.i = False

        if self.path:
            new_position = self.path.pop(0)
            self.model.grid.move_agent(self, new_position)
        else:
            print("Ruta terminada")
        # neighbors = self.model.grid.get_neighborhood(
        #     self.pos, moore=False, include_center=False
        # )
        # print("Vecinos: ", neighbors)
        #
        # valid_steps = [step for step in neighbors if self.is_valid_move(step)]
        # print("Movimientos validos: ", valid_steps)
        #
        # prioritized_steps = self.prioritize_steps(valid_steps)
        # print("Priodad de movimieto: ", prioritized_steps)
        # new_position = prioritized_steps[0]
        # self.model.grid.move_agent(self, new_position)

    def is_valid_move(self, target_position):
        if not self.model.grid.out_of_bounds(target_position):
            cell_contents = self.model.grid.get_cell_list_contents(target_position)
            # Verifica si la casilla de destino está vacía o no contiene una pared.
            for content in cell_contents:
                if isinstance(content, WallAgent):
                    return False  # No es un movimiento válido si hay una pared.
            return True  # Es un movimiento válido si la casilla de destino está vacía.
        return False  # No es un movimiento válido

    def prioritize_steps(self, valid_steps):
        return sorted(valid_steps,
                      key=lambda step: self.priority_order.index((step[0] - self.pos[0], step[1] - self.pos[1])))