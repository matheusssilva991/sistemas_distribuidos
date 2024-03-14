import xmlrpc.server


class Server:
    def __init__(self) -> None:
        self.__board = [[' ' for _ in range(8)] for _ in range(9)]
        self.__board[0] = [str(i) for i in range(8)]
        self.__players = []
        self.__current_player = 0
        self.__markers = ["X", "O"]
        self.__has_winner = False

    def get_board(self) -> list:
        return self.__board

    def set_play(self, pos: tuple) -> bool:
        row, col = pos
        row += 1
        try:
            if self.__board[row][col] == ' ':
                self.__board[row][col] = self.__markers[self.__current_player]
                self.__has_winner = self.check_winner(pos)
                self.update_current_player()
                return {"status": True, "error": None}
            else:
                return {"error": "Position already taken", "status": False}
        except IndexError:
            return {"error": "Invalid position", "status": False}

    def check_winner(self, pos: tuple) -> bool:
        row, col = pos
        row += 1

        if col > 7 or row > 8:
            raise IndexError("Invalid position")

        # Check row
        for i in range(5):
            start = i
            if all([self.__board[row][start + j] ==
                    self.__markers[self.__current_player] for j in range(4)]):
                return True

        # Check column
        for i in range(5):
            start = i
            if all([self.__board[start + j][col] ==
                    self.__markers[self.__current_player] for j in range(4)]):
                return True

        return False

    def has_empty_cells(self) -> bool:
        for row in self.__board[1:]:
            if ' ' in row:
                return True
        return False

    def get_has_winner(self) -> bool:
        return self.__has_winner

    def get_players(self) -> list:
        return self.__players

    def add_players(self) -> dict:
        if len(self.__players) < 2:
            player_id = len(self.__players)
            self.__players.append(player_id)
            return {"player_id": player_id, "status": True}
        else:
            return {"error": "Maximum number of players reached",
                    "status": False}

    def get_current_player(self) -> list:
        return self.__current_player

    def update_current_player(self) -> dict:
        self.__current_player = (self.__current_player + 1) % 2
        return {"status": True, "error": None, "player": self.__current_player}


server = xmlrpc.server.SimpleXMLRPCServer(("localhost", 8000), allow_none=True)
server.register_instance(Server())
server.serve_forever()
