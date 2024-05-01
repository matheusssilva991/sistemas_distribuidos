from src.server.server import Server
import unittest
from copy import deepcopy


class Test(unittest.TestCase):
    def test_get_empty_row(self):
        server = Server()

        # Test when there is an empty row
        for i in range(8):
            self.assertEqual(server.get_empty_row(i),
                             {"row": 8, "status": True, "error": None})

        # Test when there is no empty row
        for i in range(1, 9):
            board = server.get_board()
            board[i][0] = 'X'
            server.set_board(board)
        self.assertEqual(server.get_empty_row(0), {"error": "No empty rows",
                                                   "status": False})

    def test_has_empty_cells(self):
        server = Server()

        # Test when there are empty cells
        self.assertTrue(server.has_empty_cells())

        # Test when there are no empty cells
        board = server.get_board()
        for i in range(1, 9):
            for j in range(8):
                board[i][j] = 'X'
        server.set_board(board)
        self.assertFalse(server.has_empty_cells())

    def test_add_players(self):
        server = Server()

        # Test when is possible to add players
        for i in range(2):
            self.assertEqual(server.add_players(),
                             {"player_id": i, "status": True})

        # Test when is not possible to add players
        self.assertEqual(server.add_players(),
                         {"error": "Maximum number of players reached",
                          "status": False})

    def test_update_current_player(self):
        server = Server()

        # Test when the current player is updated
        self.assertEqual(server.update_current_player(),
                         {"status": True, "error": None, "player": 1})
        self.assertEqual(server.update_current_player(),
                         {"status": True, "error": None, "player": 0})

    def test_check_has_winner(self):
        server = Server()
        empty_board = deepcopy(server.get_board())

        # Test when there is no winner
        for i in range(1, 9):
            for j in range(8):
                self.assertFalse(server.check_winner((i, j)))

        # Test when there is a winner in a row
        for i in range(1, 9):
            for j in range(5):
                # Reset the board
                board = deepcopy(empty_board)
                server.set_board(board)

                # Set the board to have a winner
                for k in range(4):
                    board[i][j + k] = 'X'
                server.set_board(board)

                self.assertTrue(server.check_winner((i, j)))

        # Test when there is a winner in a column
        for i in range(8):
            for j in range(1, 6):
                # Reset the board
                board = deepcopy(empty_board)
                server.set_board(board)

                # Set the board to have a winner
                for k in range(4):
                    board[j + k][i] = 'X'
                server.set_board(board)

                self.assertTrue(server.check_winner((j, i)))

        """ # Test when there is a winner in the main diagonal
        board = server.get_board()
        for i in range(4):
            board[i + 1][i] = 'X'
        server.set_board(board)
        self.assertTrue(server.check_winner())

        # Test when there is a winner in the secondary diagonal
        board = server.get_board()
        for i in range(4):
            board[i + 1][3 - i] = 'X'
        server.set_board(board)
        self.assertTrue(server.check_winner()) """
