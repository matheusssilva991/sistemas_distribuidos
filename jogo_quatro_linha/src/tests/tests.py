from src.server.server import Server
import unittest
from copy import deepcopy


class Test(unittest.TestCase):
    def test_has_empty_row(self):
        server = Server()
        _, num_cols = server.get_board_dimensions()

        # Test when there is an empty row
        for i in range(num_cols):
            self.assertEqual(server.get_empty_row(i),
                             {"row": num_cols - 1, "success": True,
                              "error": None})

    def test_has_no_empty_row(self):
        server = Server()
        num_rows, num_cols = server.get_board_dimensions()

        # Test when there is no empty row
        for i in range(num_cols):
            for j in range(num_rows):
                board = server.get_board()
                board[j][i] = 'X'
                server.set_board(board)
            self.assertEqual(server.get_empty_row(i),
                             {"error": "No empty rows",
                              "success": False})

    def test_has_empty_cells(self):
        server = Server()

        # Test when there are empty cells
        self.assertTrue(server.has_empty_cells())

    def test_has_no_empty_cells(self):
        server = Server()
        num_rows, num_cols = server.get_board_dimensions()

        # Test when there are no empty cells
        board = server.get_board()
        for i in range(num_rows):
            for j in range(num_cols):
                board[i][j] = 'X'
        server.set_board(board)
        self.assertFalse(server.has_empty_cells())

    def test_it_is_possible_to_add_players(self):
        server = Server()

        # Test when is possible to add players
        for i in range(2):
            self.assertEqual(server.add_players(),
                             {"player_id": i, "success": True})

    def test_it_is_not_possible_to_add_players(self):
        server = Server()

        for _ in range(2):
            server.add_players()

        # Test when is not possible to add players
        self.assertEqual(server.add_players(),
                         {"error": "Maximum number of players reached",
                          "success": False})

    def test_update_current_player(self):
        server = Server()

        # Test when the current player is updated
        self.assertEqual(server.update_current_player(),
                         {"success": True, "error": None, "player": 1})
        self.assertEqual(server.update_current_player(),
                         {"success": True, "error": None, "player": 0})

    def test_check_has_no_winner(self):
        server = Server()
        num_rows, num_cols = server.get_board_dimensions()

        # Test when there is no winner
        for i in range(num_rows):
            for j in range(num_cols):
                self.assertFalse(server.check_winner((i, j)))

    def test_check_has_winner_in_row(self):
        server = Server()
        empty_board = deepcopy(server.get_board())
        num_rows, num_cols = server.get_board_dimensions()
        points_to_win = server.get_points_to_win()
        lim_middle_cols = num_cols - points_to_win + 1

        # Test when there is a winner in a row
        for i in range(num_rows):
            for j in range(lim_middle_cols):
                # Reset the board
                board = deepcopy(empty_board)
                server.set_board(board)

                # Set the board to have a winner
                for k in range(points_to_win):
                    board[i][j + k] = 'X'
                server.set_board(board)

                self.assertTrue(server.check_winner((i, j)))

    def test_check_has_winner_in_column(self):
        server = Server()
        empty_board = deepcopy(server.get_board())
        num_rows, num_cols = server.get_board_dimensions()
        points_to_win = server.get_points_to_win()
        lim_middle_rows = num_rows - points_to_win + 1

        # Test when there is a winner in a column
        for i in range(num_cols):
            for j in range(lim_middle_rows):
                # Reset the board
                board = deepcopy(empty_board)
                server.set_board(board)

                # Set the board to have a winner
                for k in range(points_to_win):
                    board[j + k][i] = 'X'
                server.set_board(board)

                self.assertTrue(server.check_winner((j, i)))

    def test_check_has_winner_in_main_diagonal(self):
        server = Server()
        empty_board = deepcopy(server.get_board())
        num_rows, num_cols = server.get_board_dimensions()
        points_to_win = server.get_points_to_win()
        lim_middle_rows = num_rows - points_to_win + 1
        lim_middle_cols = num_cols - points_to_win + 1

        # Test when there is a winner in the main diagonal and row >= col
        for i in range(lim_middle_rows):
            for offset in range((lim_middle_rows) - i):
                board = deepcopy(empty_board)
                for j in range(points_to_win):
                    board[i + j + offset][j + offset] = 'X'
                server.set_board(board)
                self.assertTrue(server.check_winner((i, 0)))

        # Test when there is a winner in the main diagonal and row < col
        for i in range(lim_middle_cols):
            for offset in range(lim_middle_cols - i):
                board = deepcopy(empty_board)
                for j in range(points_to_win):
                    board[j + offset][i + j + offset] = 'X'
                server.set_board(board)
                self.assertTrue(server.check_winner((0, i)))

    def test_check_has_winner_in_secondary_diagonal(self):
        server = Server()
        empty_board = deepcopy(server.get_board())
        num_rows, num_cols = server.get_board_dimensions()
        points_to_win = server.get_points_to_win()
        lim_middle_rows = num_rows - points_to_win + 1
        lim_middle_cols = num_cols - points_to_win + 1

        # Test when there is a winner in the secondary diagonal and row + col >
        # num_rows - 1
        for i in range(lim_middle_rows):
            for offset in range(lim_middle_rows - i):
                board = deepcopy(empty_board)
                for j in range(points_to_win):
                    board[i + j + offset][num_cols - 1 - j - offset] = 'X'
                server.set_board(board)
                self.assertTrue(server.check_winner((i, num_cols - 1)))

        # Test when there is a winner in the secondary diagonal and row + col<=
        # num_rows - 1
        for i in range(lim_middle_cols):
            for offset in range(lim_middle_cols - i):
                board = deepcopy(empty_board)
                for j in range(points_to_win):
                    board[j + offset][num_cols - 1 - i - j - offset] = 'X'
                server.set_board(board)

                self.assertTrue(server.check_winner((0, num_cols - 1 - i)))
