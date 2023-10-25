
from handscorestate import HandScoreState

# constants for colours


class bcolours:
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'


class StatePlotter:
    def format_choice(self, choice: str):
        if choice == "H":
            return bcolours.GREEN+choice+bcolours.ENDC
        elif choice == "S":
            return bcolours.YELLOW+choice+bcolours.ENDC
        return bcolours.RED+choice+bcolours.ENDC

    def print(self, hstate: HandScoreState):
        grid = []
        for stud, val in hstate.result_dict.items():
            row = []
            for k, v in val.items():
                if type(v).__name__ == "HandScore":
                    row.append(v.favoured_strategy())
            grid.append(row)

        col_digits = 2
        n_rows = len(grid)
        n_cols = len(grid[0])
        result = (
            ' ' * (col_digits + 1) + ''.join(str(i+1)
                                             for i in range(n_cols)) + '\n'
            + ' ' * (col_digits + 1) + ''.join('-' for i in range(n_cols)) + '\n')
        for i, row in enumerate(grid):
            result += (
                str(i+2).zfill(col_digits) + '|'
                + ''.join(self.format_choice(elem) for elem in row) + '\n')
        print(result)
