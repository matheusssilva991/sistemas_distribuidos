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

        table = tabulate(board, headers='firstrow', tablefmt='simple_grid',
                         stralign='center')

        print(table)
