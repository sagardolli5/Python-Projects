from art import ascii_art

is_game_on = input("Do you want to play a game of Tic Tac Toe? Type 'Y' or 'N': ").lower()
player_name = str(input("Please enter your name: ").title())

if is_game_on == "y":
    print(ascii_art["banner"])
    print(f"Welcome! {player_name}, Let's Play!")
else:
    print("Good Bye!")

board = {
    1: "1", 2: "2", 3: "3",
    4: "4", 5: "5", 6: "6",
    7: "7", 8: "8", 9: "9"
}

def print_board(b):
    print(f"""
 {b[1]} | {b[2]} | {b[3]}
---+---+---
 {b[4]} | {b[5]} | {b[6]}
---+---+---
 {b[7]} | {b[8]} | {b[9]}
""")

winning_combinations = [
    (1,2,3),(4,5,6),(7,8,9),(1,4,7),
    (2,5,8),(3,6,9),(1,5,9),(3,5,7)
]

def check_winner(game_board, player):
    for combo in winning_combinations:
        a, b, c = combo
        if game_board[a] == game_board[b] == game_board[c] == player:
            return True
    return False

def check_draw(game_board):
    for value in game_board.values():
        if value not in ["X", "O"]:
            return False
    return True

def computer_move(game_board):

    for combo in winning_combinations:
        a,b,c = combo
        values = [game_board[a], game_board[b], game_board[c]]
        # Try to win
        if values.count("O") == 2:
            for pos in combo:
                if game_board[pos] not in ["X","O"]:
                    return pos
        # Block player win
        elif values.count("X") == 2:
            for pos in combo:
                if game_board[pos] not in ["X","O"]:
                    return pos

    # Otherwise, pick first empty space
    for pos in game_board:
        if game_board[pos] not in ["X","O"]:
            return pos


# Choose player/computer signs
player_sign = input("Choose which sign you want to play as 'X' or 'O': ").upper()
computer_sign = "O" if player_sign == "X" else "X"

while is_game_on == "y":
    print_board(board)

    # Player move
    print(f"{player_name}! It's your turn.")
    select_number = int(input("Enter the number 1-9 where you want to play your move: "))

    if board[select_number] not in ["X","O"]:
        board[select_number] = player_sign
        print(f"{player_name} played at position {select_number}!")
    else:
        print("That square is already taken. Choose a different move.")
        continue

    # Check if player won
    if check_winner(board, player_sign):
        print_board(board)
        print(ascii_art["win"])
        print(f"Congratulations {player_name}!")
        is_game_on = "n"
    else:
        # Computer move
        comp_move = computer_move(board)
        board[comp_move] = computer_sign
        print(f"Computer played at position {comp_move}!")

        # Check if computer won
        if check_winner(board, computer_sign):
            print_board(board)
            print(ascii_art["computer_won"])
            print("Better luck next time.")
            is_game_on = "n"
        # Check draw after computer move
        elif check_draw(board):
            print_board(board)
            print(ascii_art["draw"])
            is_game_on = "n"