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

    def step(self) -> None:
        if self.path is None:  # Solo ejecutar el algoritmo si no hay un camino calculado.
            self.calculate_path()
        if self.expansion_nodes:  # Si hay nodos de expansion, los crea
            self.model.create_expansion_agents([self.expansion_nodes.pop(0)], self.order_counter)
            self.order_counter += 1

            if not bool(self.expansion_nodes):
                self.model.change_color_path(self.path)
        self.move()

    def move(self) -> None:
        pass

    def calculate_path(self):
        self.path, self.expansion_nodes = self.algorithm.search(self.pos, self.model.get_goal_position()) #Cambiar para que se ejecute desde la posicion inicial deel robot
        print("Posicion demeta: ", self.model.get_goal_position())
        print("Ruta del algoritmo:", self.path)
        print("Nodos de expansion:", self.expansion_nodes)

    def is_algorithm_finished(self):
        return not bool(self.expansion_nodes)