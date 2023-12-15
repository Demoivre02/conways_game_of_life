import itertools
from textwrap import dedent

class Cell:
    def __init__(self, is_alive):
        self.is_alive = is_alive

    def __str__(self):
        return Live.string_form if self.is_alive else Dead.string_form

    @classmethod
    def from_str(cls, string):
        return Live() if string == Live.string_form else Dead()

    def next_state(self, neighbor_count):
        raise NotImplementedError("Subclasses must implement this method")


class Dead(Cell):
    string_form = '·'

    def next_state(self, neighbor_count):
        return Live() if neighbor_count == 3 else Dead()


class Live(Cell):
    string_form = '0'

    def next_state(self, neighbor_count):
        return Live() if neighbor_count in [2, 3] else Dead()


class GameOfLife:
    @classmethod
    def dead_grid(cls, *, height=None, width=None):
        return [[Dead() for _ in range(width)] for _ in range(height)]

    @classmethod
    def from_str(cls, string):
        non_empty_lines = (line for line in string.splitlines() if len(line) > 0)
        parsed_grid = [[Cell.from_str(char) for char in line] for line in non_empty_lines]
        return cls(grid=parsed_grid)

    def __init__(self, grid=None):
        self.grid = grid
        self.height = len(grid)
        self.width = len(grid[0])

    def __str__(self):
        return '\n'.join(''.join(str(cell) for cell in row) for row in self.grid)

    def next_generation(self):
        next_grid = [
            [cell.next_state(neighbor_count) for cell, neighbor_count in row]
            for row in self.grid_with_live_neighbor_counts()
        ]
        return GameOfLife(grid=next_grid)

    def grid_with_live_neighbor_counts(self):
        return (
            ((cell, self.count_live_neighbors(row, col)) for (row, col), cell in coordinated_row)
            for coordinated_row in self.coordinate()
        )

    def coordinate(self):
        return (
            (((row_index, col_index), cell) for col_index, cell in enumerate(row))
            for row_index, row in enumerate(self.grid)
        )

    def count_live_neighbors(self, row, col):
        directions_1D = (-1, 0, 1)
        directions_2D = itertools.product(directions_1D, directions_1D)
        neighbor_coords = (
            (row + d_row, col + d_col)
            for (d_row, d_col) in directions_2D
            if (d_row, d_col) != (0, 0)
        )

        def is_coord_alive(coord):
            cell = self.get(*coord, default=Dead())
            return int(cell.is_alive)

        return sum(map(is_coord_alive, neighbor_coords))

    def get(self, row, col, default=None):
        is_within_rows = 0 <= row < self.height
        is_within_cols = 0 <= col < self.width
        return self.grid[row][col] if is_within_rows and is_within_cols else default


def run_string_example(seed_string=None, seed_name=None, num_gens=10):
    seed_game = GameOfLife.from_str(seed_string)
    seed_name = seed_name or f'A {seed_game.height}x{seed_game.width} grid'
    print(dedent(f'''
        =========================
        | Conway's Game of Life |
        {'':=^50}
        | {f'Starting with seed: "{seed_name:.10}"': <46.46} |
        | {f'Running for {str(num_gens):1.3} generations.': <46.46} |
        {'':=^50}
    '''))
    latest_generation = seed_game
    for gen_num in range(1, num_gens + 1):
        print(f'Generation {gen_num}:')
        print(str(latest_generation))
        latest_generation = latest_generation.next_generation()
    print('Done')


def glider_example():
    glider_string = dedent('''
        ··0····
        0·0····
        ·00····
        ·······
        ·······
        ·······
    ''')
    run_string_example(seed_string=glider_string, seed_name='Glider', num_gens=15)


def question_example():
    game_string = dedent('''
        ·0·
        0·0
    ''')
    run_string_example(seed_string=game_string, num_gens=4)


if __name__ == '__main__':
    glider_example()
    question_example()
