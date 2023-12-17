import mesa
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer

from agents.boxAgent import BoxAgent
from agents.expansionAgent import ExpansionAgent
from agents.goalAgent import GoalAgent
from agents.pathAgent import PathAgent
from agents.robotAgent import RobotAgent
from agents.wallAgent import WallAgent
from models.labyrinthModel import LabyrinthModel
from utils.fileUtils import *

NUM_ROWS = 0
NUM_COLS = 0
SIZE_OF_CANVAS_IN_PIXELS_X = 500
SIZE_OF_CANVAS_IN_PIXELS_Y = 400


#Carga del archivo
file_name = "resources/text_files/map.txt"
content = loadFile(file_name)
map, NUM_ROWS, NUM_COLS = parseText(content)

simulation_params = {
    "number_of_agents": mesa.visualization.Slider(name='Number of Agents', value=2, min_value=1, max_value=200, step=1, description="seleccionar numero de agentes"),
    "algorithm_choice": mesa.visualization.Choice(name='Choice Algorithm', value='BFS', choices=['BFS', 'DFS', 'UCS', 'ASTAR', 'HILL CLIMBING', 'BEAM SEARCH']),
    "heuristic_choice": mesa.visualization.Choice(name='Choice Heuristic', value='EUCLIDEAN', choices=['EUCLIDEAN', 'MANHATTAN']),
    "map": map,
    "width": NUM_COLS,
    "height": NUM_ROWS
}


def agent_portrayal(agent):
    portrayal = {"Shape": "circle", "Filled": "true", "r": 0.5}
    if isinstance(agent, WallAgent):
        portrayal["Shape"] = "resources/icons/muro.png"
        portrayal["Layer"] = 0
        portrayal["w"] = 1
        portrayal["h"] = 1
    elif isinstance(agent, PathAgent):
        portrayal["Shape"] = "circle"#"resources/icons/pavimentacion.png"
        portrayal["Color"] = "blue"
        portrayal["Layer"] = 0
        portrayal["w"] = 1
        portrayal["h"] = 1
    elif isinstance(agent, RobotAgent):
        portrayal["Shape"] = "resources/icons/robot.png"
        portrayal["Layer"] = 1
        portrayal["w"] = 1
        portrayal["h"] = 1
    elif isinstance(agent, BoxAgent):
        portrayal["Shape"] = "resources/icons/paquete.png"
        portrayal["Layer"] = 2
        portrayal["w"] = 0.5
        portrayal["h"] = 0.5
    elif isinstance(agent, GoalAgent):
        portrayal["Shape"] = "resources/icons/bandera.png"
        portrayal["Layer"] = 3
        portrayal["w"] = 1
        portrayal["h"] = 1
    elif isinstance(agent, ExpansionAgent):
        portrayal["Shape"] = "circle"
        portrayal["Color"] = agent.color
        portrayal["Layer"] = 4
        portrayal["text"] = agent.order_number
        portrayal["text_color"] = "black"
    else:
        portrayal["Shape"] = "circle"
        portrayal["Color"] = 'green'
        portrayal["Layer"] = 5
    return portrayal


grid = CanvasGrid(agent_portrayal, NUM_COLS, NUM_ROWS, SIZE_OF_CANVAS_IN_PIXELS_X, SIZE_OF_CANVAS_IN_PIXELS_Y)
server = ModularServer(LabyrinthModel, [grid], "Sokoban", model_params=simulation_params)
server.port = 8200
server.launch()
