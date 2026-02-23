# -*- coding: utf-8 -*-
import sys
import io

# Force UTF-8 output so Lithuanian characters print correctly on Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from search import *

# 5x5 labirinto žemėlapis: 0 = laisva ląstelė, 1 = siena
# Eilutės atitinka y koordinatę (0 = viršus), stulpeliai – x koordinatę (0 = kairė)
MAZE = [
    [0, 0, 1, 0, 0],  # y=0
    [1, 0, 1, 0, 1],  # y=1
    [0, 0, 0, 0, 1],  # y=2
    [0, 1, 1, 0, 0],  # y=3
    [0, 0, 0, 1, 0],  # y=4
]


class MazeProblem(Problem):
    """
    Labirinto problema, naudojanti AIMA Problem bazinę klasę.

    Būsena (state): (x, y) koordinatės labirinte.
    Pradinė būsena (initial): (0, 0) – viršutinis kairysis kampas.
    Tikslas (goal): (4, 4) – apatinis dešinysis kampas.
    """

    def __init__(self):
        # Pradinė būsena – koordinatės (0, 0)
        # Tikslas – koordinatės (4, 4)
        super().__init__(initial=(0, 0), goal=(4, 4))

    def actions(self, state):
        """
        Grąžina galimus veiksmus iš dabartinės būsenos.
        Veiksmai: 'U' (aukštyn), 'D' (žemyn), 'L' (kairėn), 'R' (dešinėn).
        Veiksmas leidžiamas tik jei nauja pozicija nepereina labirinto ribų
        ir nėra siena (MAZE reikšmė != 1).
        """
        x, y = state
        possible = []

        # Judėjimo kryptys: veiksmas -> (dx, dy)
        moves = {
            'U': (0, -1),  # aukštyn: y mažėja
            'D': (0, +1),  # žemyn:   y didėja
            'L': (-1, 0),  # kairėn:  x mažėja
            'R': (+1, 0),  # dešinėn: x didėja
        }

        for action, (dx, dy) in moves.items():
            nx, ny = x + dx, y + dy
            # Tikrinama, ar nauja pozicija yra labirinto ribose ir laisva
            if 0 <= nx < 5 and 0 <= ny < 5 and MAZE[ny][nx] == 0:
                possible.append(action)

        return possible

    def result(self, state, action):
        """
        Grąžina naują būseną (x, y) po veiksmo atlikimo.
        Kiekvienas veiksmas pakeičia x arba y koordinatę vienetu.
        """
        x, y = state
        moves = {
            'U': (0, -1),
            'D': (0, +1),
            'L': (-1, 0),
            'R': (+1, 0),
        }
        dx, dy = moves[action]
        return (x + dx, y + dy)

    def goal_test(self, state):
        """
        Grąžina True, jei dabartinė būsena yra tikslas (4, 4).
        """
        return state == self.goal

    def path_cost(self, c, state1, action, state2):
        """
        Kiekvienas žingsnis kainuoja +1.
        """
        return c + 1


# Sukuriamas MazeProblem objektas
problem = MazeProblem()

# Ieškoma sprendimo naudojant plataus pirmumo paiešką (BFS)
result_node = breadth_first_graph_search(problem)

if result_node:
    # Rastas kelias – sąrašas būsenų nuo pradinės iki tikslinės
    path = result_node.path()
    states = [node.state for node in path]

    # Veiksmų seka, vedanti į tikslą
    actions_sequence = result_node.solution()

    print("Rastas kelias (koordinatės):")
    print(states)

    print("\nVeiksmų seka:")
    print(actions_sequence)
else:
    print("Sprendimas nerastas!")
