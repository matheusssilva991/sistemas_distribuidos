from client.client import Client

client = Client("http://localhost:8000/")

while not client.server.get_has_winner() and client.server.has_empty_cells():
    print("You are player", client.player_id)
    print("Players:", client.server.get_players())
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
        print("Waiting for the other player to play...\n\n")
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
        print(f"\t\t\tPlayer {client.server.get_current_player()} won!")
    client.show_board()
