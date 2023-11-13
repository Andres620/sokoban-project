from mesa import Agent


class ExpansionAgent(Agent):
    def __init__(self,unique_id, model, order_counter):
        super().__init__(unique_id, model)
        self.order_number = order_counter
        self.color = "red"

    def step(self) -> None:
        pass

    def move(self) -> None:
        pass
