def loadFile(file_name):
    try:
        with open(file_name, 'r') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        return None


def parseText(text):
    lines = text.strip().split('\n')
    agent_dict = {'R': [], 'C': [], 'M': [], 'A': [], 'B': []}
    num_rows = len(lines)
    num_cols = 0
    for row, line in enumerate(lines):
        cells = line.rstrip(', ').split(', ')
        num_cols = max(num_cols, len(cells))
        for col, cell in enumerate(cells):
            if cell == "R":
                agent_dict['R'].append((row, col))
            elif cell == "M":
                agent_dict['M'].append((row, col))
            elif cell == "C":
                agent_dict['C'].append((row, col))
            elif cell.startswith("C-"):
                agent_dict['C'].append((row, col))
                agent_type = cell.split('-')[1]
                if agent_type == "a":
                    agent_dict['A'].append((row, col))
                elif agent_type == "b":
                    agent_dict['B'].append((row, col))

    return agent_dict, num_rows, num_cols

