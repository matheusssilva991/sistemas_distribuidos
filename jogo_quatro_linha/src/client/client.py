import xmlrpc.client
from tabulate import tabulate


class Client:
    def __init__(self, url) -> None:
        self.server = xmlrpc.client.ServerProxy(url, allow_none=True)
        result = self.server.add_players()

        if result['status']:
            self.player_id = result['player_id']
        else:
            print(result['error'])
            exit()

    def show_board(self):
        board = self.server.get_board()
        index_column = [list(range(len(board[0])))]
        board = index_column + board

        table = tabulate(board, headers='firstrow', tablefmt='simple_grid',
                         stralign='center')

        print(table)


if __name__ == "__main__":
    client = Client("http://localhost:8000/")

    while not client.server.get_has_winner() and client.server.has_empty_cells(): # noqa
        print("You are player", client.player_id)
        print(f"Player {client.server.get_current_player()} turn")

        client.show_board()
        if client.server.get_current_player() == client.player_id:
            # Keep trying to play until the position is valid
            while True:
                try:
                    col = int(input("Enter the column to play: "))
                except ValueError:
                    print("Invalid column")
                    continue
                result = client.server.get_empty_row(col)

                # If there's an error, print it and try again
                if result['error']:
                    print(result['error'])
                    continue

                row = result['row']
                result = client.server.set_play((row, col))

                # If there's an error, print it and try again
                if result['error']:
                    print(result['error'])
                    continue
                # If the position is valid, break the loop
                else:
                    break

            if client.server.get_has_winner():
                break

            print("\n\n")
        else:
            print("Waiting for the other player to play...")
            board = client.server.get_board()
            new_board = client.server.get_board()
            while board == new_board:
                new_board = client.server.get_board()
            continue

    if not client.server.has_empty_cells():
        print("\n\t\t\tIt's a tie!")
        client.show_board()
    else:
        if client.server.get_current_player() == client.player_id:
            print("\n\t\t\tYou won!")
        else:
            current_player = client.server.get_current_player()
            print(f"\t\t\tYou lost, player {current_player} won!")
        client.show_board()
