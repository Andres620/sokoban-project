import mesa
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer

from agents.boxAgent import BoxAgent
from agents.goalAgent import GoalAgent
from agents.pathAgent import PathAgent
from agents.robotAgent import RobotAgent
from agents.stoneAgent import StoneAgent
from models.labyrinthModel import LabyrinthModel
from agents.searchExplorerAgent import SearchExplorerAgent
from utils.fileUtils import *

NUM_ROWS = 7
NUM_COLS = 5
SIZE_OF_CANVAS_IN_PIXELS_X = 500
SIZE_OF_CANVAS_IN_PIXELS_Y = 500


#Carga del archivo
file_name = "C:/Users/alamb/OneDrive/Escritorio/map.txt"
content = loadFile(file_name)


simulation_params = {
    "number_of_agents": mesa.visualization.Slider(name='Number of Agents', value=2, min_value=1, max_value=200, step=1, description="seleccionar numero de agentes"),
    "map": parseText(content),
    "width": NUM_COLS,
    "height": NUM_ROWS
}


def agent_portrayal(agent):
    portrayal = {"Shape": "circle", "Filled": "true", "r": 0.5}
    if isinstance(agent, StoneAgent):
        portrayal["Shape"] = "icons/muro.png"
        portrayal["Layer"] = 0
        portrayal["w"] = 1
        portrayal["h"] = 1
    elif isinstance(agent, PathAgent):
        portrayal["Shape"] = "icons/pavimentacion.png"
        portrayal["Layer"] = 0
        portrayal["w"] = 1
        portrayal["h"] = 1
    elif isinstance(agent, RobotAgent):
        portrayal["Shape"] = "icons/robot.png"
        portrayal["Layer"] = 1
        portrayal["w"] = 1
        portrayal["h"] = 1
    elif isinstance(agent, BoxAgent):
        portrayal["Shape"] = "icons/paquete.png"
        portrayal["Layer"] = 2
        portrayal["w"] = 0.5
        portrayal["h"] = 0.5
    else:
        portrayal["Shape"] = "icons/bandera.png"
        portrayal["Layer"] = 3
        portrayal["w"] = 1
        portrayal["h"] = 1
    return portrayal


grid = CanvasGrid(agent_portrayal, NUM_COLS, NUM_ROWS, SIZE_OF_CANVAS_IN_PIXELS_X, SIZE_OF_CANVAS_IN_PIXELS_Y)
server = ModularServer(LabyrinthModel, [grid], "Sokoban", model_params=simulation_params)
server.port = 8200
server.launch()
