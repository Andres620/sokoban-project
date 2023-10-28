from agents.wallAgent import WallAgent


class GameRules:
    def __init__(self, model):
        self.model = model

        #prioridad de movimientos (izquierda, arriba, derecha, abajo).
        self.priority_order = [(0, -1), (-1, 0), (0, 1), (1, 0)]

    def is_valid_move(self, agent, target_position):
        x, y = target_position
        if not self.model.grid.out_of_bounds(target_position):
            cell_contents = self.model.grid.get_cell_list_contents(target_position)
            # Verifica si la casilla de destino está vacía o no contiene una pared.
            for content in cell_contents:
                if isinstance(content, WallAgent):
                    return False  # No es un movimiento válido si hay una pared.
            return True  # Es un movimiento válido si la casilla de destino está vacía.
        return False  # No es un movimiento válido

    def get_priority_steps(self, valid_steps, actual_position):
        sorted_valid_steps = sorted(valid_steps, key=lambda step: self.priority_order.index((step[0]-actual_position[0], step[1]-actual_position[1])))
        return sorted_valid_steps
