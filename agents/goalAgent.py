from mesa import Agent


class GoalAgent(Agent):
    def __init__(self,unique_id, model):
        super().__init__(unique_id, model)
        self.assigned_box = None  # Atributo para almacenar la caja asignada

    def step(self) -> None:
        pass

    def move(self) -> None:
        pass

    def set_assigned_box(self, box):
        self.assigned_box = box
