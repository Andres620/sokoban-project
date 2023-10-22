from mesa import Agent


class BoxAgent(Agent):
    def __init__(self,unique_id, model):
        super().__init__(unique_id, model)

    def step(self) -> None:
        pass

    def move(self) -> None:
        pass
