import xmlrpc.server


class Server:
    def __init__(self) -> None:
        self.__num_cols = 8
        self.__num_rows = 8
        self.__points_to_win = 4
        self.__board = [[' ' for _ in range(self.__num_cols)]
                        for _ in range(self.__num_rows)]
        self.__players = []
        self.__current_player = 0
        self.__markers = ["X", "O"]
        self.__lim_middle_rows = self.__num_rows - self.__points_to_win + 1
        self.__lim_middle_cols = self.__num_cols - self.__points_to_win + 1
        self.__has_winner = False

    def get_points_to_win(self) -> int:
        return self.__points_to_win

    def get_board(self) -> list:
        return self.__board

    def set_board(self, board: list) -> None:
        self.__board = board

    def get_players(self) -> list:
        return self.__players

    def get_has_winner(self) -> bool:
        return self.__has_winner

    def get_board_dimensions(self) -> dict:
        return self.__num_rows, self.__num_cols

    def get_empty_row(self, column) -> int:
        for i in range(self.__num_rows - 1, -1, -1):
            if ' ' == self.__board[i][column]:
                return {"row": i, "success": True, "error": None}
        return {"error": "No empty rows", "success": False}

    def set_play(self, pos: tuple) -> bool:
        row, col = pos
        try:
            if self.__board[row][col] == ' ':
                self.__board[row][col] = self.__markers[self.__current_player]
                self.__has_winner = self.check_winner(pos)
                if not self.__has_winner:
                    self.update_current_player()
                return {"success": True, "error": None}
            else:
                return {"error": "Position already taken", "success": False}
        except IndexError:
            return {"error": "Invalid position", "success": False}

    def check_winner(self, pos: tuple) -> bool:
        row, col = pos

        if (col > self.__num_cols - 1) or (row > self.__num_rows - 1) or \
           (row < 0) or (col < 0):
            raise IndexError("Invalid position")

        # Check row
        for i in range(self.__lim_middle_cols):
            if all([self.__board[row][i + j] ==
                    self.__markers[self.__current_player]
                    for j in range(self.__points_to_win)]):
                return True

        # Check column
        for i in range(self.__lim_middle_rows):
            if all([self.__board[i + j][col] ==
                    self.__markers[self.__current_player]
                    for j in range(self.__points_to_win)]):
                return True

        # Check main diagonal
        starts = [0, 0]
        if row > col:
            starts[0] = row - col
        elif row < col:
            starts[1] = col - row

        # Check if not possible to have a winner in the main diagonal
        if not (starts[0] > self.__num_rows - self.__points_to_win or
           starts[1] > self.__num_cols - self.__points_to_win):

            # check if the player has won in the main diagonal
            for i in range(self.__lim_middle_cols - starts[0] - starts[1]):
                if all([self.__board[i + j + starts[0]][starts[1] + j + i] ==
                        self.__markers[self.__current_player]
                        for j in range(self.__points_to_win)]):
                    return True

        # Check secondary diagonal
        starts = [0, self.__num_cols - 1]
        if row + col <= self.__num_cols - 1:
            starts[1] = row + col
        elif row + col > self.__num_cols - 1:
            starts[0] = (row + col) - (self.__num_cols - 1)

        # Check if not possible to have a winner in the secondary diagonal
        if not (row + col > self.__num_rows + self.__points_to_win - 1 or
           row + col < self.__points_to_win - 1):

            for i in range(self.__lim_middle_rows - starts[0]):
                # check if the player has won in the secondary diagonal
                if all([self.__board[j + i + starts[0]][starts[1] - j - i] ==
                        self.__markers[self.__current_player]
                        for j in range(self.__points_to_win)]):
                    return True

        return False

    def has_empty_cells(self) -> bool:
        for row in self.__board:
            if ' ' in row:
                return True
        return False

    def add_players(self) -> dict:
        if len(self.__players) < 2:
            player_id = len(self.__players)
            self.__players.append(player_id)
            return {"player_id": player_id, "success": True}
        else:
            return {"error": "Maximum number of players reached",
                    "success": False}

    def get_current_player(self) -> list:
        return self.__current_player

    def update_current_player(self) -> dict:
        self.__current_player = (self.__current_player + 1) % 2
        return {"success": True, "error": None,
                "player": self.__current_player}


if __name__ == '__main__':
    IP = "localhost"
    PORT = 8000

    with xmlrpc.server.SimpleXMLRPCServer((IP, PORT),
                                          allow_none=True,
                                          logRequests=True) as server:
        server.register_instance(Server())
        print(f"Server started and running in {IP}:{PORT}")
        server.serve_forever()
