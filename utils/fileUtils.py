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

    for row, line in enumerate(lines):
        cells = line.rstrip(', ').split(', ')
        for col, cell in enumerate(cells):
            print(cell)
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

    return agent_dict


file_name = "C:/Users/alamb/OneDrive/Escritorio/map.txt"  # Replace with the path to your file
content = loadFile(file_name)


if content is not None:
    agents = parseText(content)
    print(agents)
else:
    print("File not found.")
