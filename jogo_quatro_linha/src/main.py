from client.client import Client
from time import sleep

client = Client("http://localhost:8000/")

while not client.server.get_has_winner() or client.server.has_empty_cells():
    print(f"Player {client.server.get_current_player()} turn")

    client.show_board()
    if client.server.get_current_player() == client.player_id:
        pos = input("Enter the position to play (row, col): ")
        row, col = map(int, pos.split(","))

        result = client.server.set_play((row, col))

        if result['error']:
            print(result['error'])
            sleep(2)
            continue

        if client.server.get_has_winner():
            continue
    else:
        print("Waiting for the other player to play...\n\n")
        board = client.server.get_board()
        new_board = client.server.get_board()
        while board == new_board:
            new_board = client.server.get_board()
        continue
else:
    if not client.server.has_empty_cells():
        print("It's a tie!")
        client.show_board()
    else:
        print(f"Player {client.server.get_current_player()} won!")
        client.show_board()
