import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        if len(self.cells) == self.count:
            return self.cells.copy()

        return set()

    def known_safes(self):
        if self.count == 0:
            return self.cells.copy()

        return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.difference_update({cell})
            self.count = self.count - 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        self.cells.difference_update({cell})


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        print(f"-------MOVE MADE--- cell{cell} --- count: {count}")

        def get_neighboring_cells(cell):
            x = cell[0]
            y = cell[1]
            possible_neighbors = [
                (x-1, y-1), (x, y-1), (x+1, y-1), (x-1, y),
                (x+1, y), (x-1, y+1), (x, y+1), (x+1, y+1)]

            def valid_cell(cell):
                if cell[0] < 0 or cell[0] > self.height - 1:
                    return False
                if cell[1] < 0 or cell[1] > self.width - 1:
                    return False
                return True

            return list(filter(valid_cell, possible_neighbors))

        self.moves_made.add(cell)
        self.mark_safe(cell)

        neighboring_cells = get_neighboring_cells(cell)

        for cell in self.mines:
            if cell in neighboring_cells:
                neighboring_cells.remove(cell)
                count -= 1

        for cell in self.safes:
            if cell in neighboring_cells:
                neighboring_cells.remove(cell)

        self.knowledge.append(Sentence(neighboring_cells.copy(), count))

        def check_mines_or_safe():
            for i, sentence in enumerate(self.knowledge):
                if sentence.known_mines():
                    mines = sentence.known_mines()
                    print(
                        f"******removing {sentence} because it's all mines*****")
                    for cell in mines:
                        self.mark_mine(cell)
                    self.knowledge.pop(i)
                    continue
                if sentence.known_safes():
                    print(
                        f"******removing {sentence} because it's all safes*****")
                    safes = sentence.known_safes()
                    for cell in safes:
                        self.mark_safe(cell)
                    self.knowledge.pop(i)
                    continue

        def check_for_subsets():
            for i, sentence in enumerate(self.knowledge):
                for j, other_sentence in enumerate(self.knowledge):
                    if other_sentence.cells < sentence.cells:
                        print(f"**SUBSET: {other_sentence} of {sentence}")
                        sentence.cells.difference_update(other_sentence.cells)
                        sentence.count = sentence.count - other_sentence.count
                        # sentence.count = sentence.count - other_sentence.count
                        # self.knowledge.pop(j)

        check_mines_or_safe()
        check_for_subsets()
        check_mines_or_safe()

        print(f"moves made: {self.moves_made}")
        print(f"safes: {self.safes}")
        print(f"mines: {self.mines}")

        print('The knowledge is:')
        for s in self.knowledge:
            print(f"s: {s}")

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        avail_moves = self.safes.difference(self.moves_made)
        if len(avail_moves) > 0:
            move = avail_moves.pop()
            print(f"Making safe move: {move}")
            return move
        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        print('making random move')
        all_moves_avail = set()
        for i in range(self.width):
            for j in range(self.height):
                all_moves_avail.add((i, j))
        all_moves_avail.difference_update(self.moves_made.union(self.mines))
        if len(all_moves_avail) > 0:
            return all_moves_avail.pop()

        return None
