pip install flask flask-cors python-chess

how can we make a gui for this in html 

!pip install python-chess

### Engine
import chess
from collections import Counter
import random
import math
import time

board = chess.Board()

# Define piece values
piece_values = {
    1: 1.00,   # Pawn
    2: 3.05,   # Knight
    3: 3.33,   # Bishop
    4: 5.63,   # Rook
    5: 9.50,   # Queen
    6: 40.00,    # King (usually excluded from evaluation)
}

# Piece-square tables
piece_square_tables = {
    chess.PAWN: [
        0.00,  0.00,  0.00,  0.00,  0.00,  0.00,  0.00,  0.00,
        0.65,  0.70,  0.75,  0.80,  0.80,  0.75,  0.70,  0.65,
        0.30,  0.35,  0.40,  0.45,  0.45,  0.40,  0.35,  0.30,
        0.10,  0.15,  0.20,  0.25,  0.25,  0.20,  0.15,  0.10,
        0.00,  0.05,  0.10,  0.15,  0.15,  0.10,  0.05,  0.00,
       -0.05,  0.00,  0.05,  0.10,  0.10,  0.05,  0.00, -0.05,
       -0.10, -0.05,  0.00, -0.20, -0.20,  0.00,  0.00, -0.10,
        0.00,  0.00,  0.00,  0.00,  0.00,  0.00,  0.00,  0.00
    ],

    chess.KNIGHT: [
        0.00,  0.00,  0.00,  0.00,  0.00,  0.00,  0.00,  0.00,
        0.00,  0.00,  0.00,  0.00,  0.00,  0.00,  0.00,  0.00,
        0.00,  0.00,  0.00,  0.00,  0.00,  0.00,  0.00,  0.00,
        0.00,  0.00,  0.00,  0.00,  0.00,  0.00,  0.00,  0.00,
        0.00,  0.00,  0.00,  0.00,  0.00,  0.00,  0.00,  0.00,
        0.00,  0.00,  0.00,  0.00,  0.00,  0.00,  0.00,  0.00,
        0.00,  0.00,  0.00,  0.00,  0.00,  0.00,  0.00,  0.00,
       -0.10, -0.10, -0.10, -0.10, -0.10, -0.10, -0.10, -0.10,
    ],

    chess.BISHOP: [
        0.00,  0.00,  0.00,  0.00,  0.00,  0.00,  0.00,  0.00,
        0.00,  0.00,  0.00,  0.00,  0.00,  0.00,  0.00,  0.00,
        0.00,  0.00,  0.00,  0.00,  0.00,  0.00,  0.00,  0.00,
        0.00,  0.00,  0.00,  0.00,  0.00,  0.00,  0.00,  0.00,
        0.00,  0.00,  0.00,  0.00,  0.00,  0.00,  0.00,  0.00,
        0.00,  0.00,  0.00,  0.00,  0.00,  0.00,  0.00,  0.00,
        0.00,  0.00,  0.00,  0.00,  0.00,  0.00,  0.00,  0.00,
       -0.10, -0.10, -0.10, -0.10, -0.10, -0.10, -0.10, -0.10,
    ],

    chess.ROOK: [
        0.00,  0.00,  0.00,  0.00,  0.00,  0.00,  0.00,  0.00,
        0.20,  0.20,  0.20,  0.20,  0.20,  0.20,  0.20,  0.20,
        0.00,  0.00,  0.00,  0.00,  0.00,  0.00,  0.00,  0.00,
        0.00,  0.00,  0.00,  0.00,  0.00,  0.00,  0.00,  0.00,
        0.00,  0.00,  0.00,  0.00,  0.00,  0.00,  0.00,  0.00,
        0.00,  0.00,  0.00,  0.00,  0.00,  0.00,  0.00,  0.00,
        0.00,  0.00,  0.00,  0.00,  0.00,  0.00,  0.00,  0.00,
        0.05,  0.05,  0.05,  0.05,  0.05,  0.05,  0.05,  0.05,
    ],

    chess.QUEEN: [
        0.00,  0.00,  0.00,  0.00,  0.00,  0.00,  0.00,  0.00,
        0.00,  0.00,  0.00,  0.00,  0.00,  0.00,  0.00,  0.00,
        0.00,  0.00,  0.00,  0.00,  0.00,  0.00,  0.00,  0.00,
        0.00,  0.00,  0.00,  0.00,  0.00,  0.00,  0.00,  0.00,
        0.00,  0.00,  0.00,  0.00,  0.00,  0.00,  0.00,  0.00,
        0.05,  0.05,  0.05,  0.05,  0.05,  0.05,  0.05,  0.05,
        0.05,  0.05,  0.05,  0.05,  0.05,  0.05,  0.05,  0.05,
       -0.05, -0.05, -0.05, -0.05, -0.05, -0.05, -0.05, -0.05,
    ],

    chess.KING: [
        0.25,  0.25,  0.25,  0.25,  0.25,  0.25,  0.25,  0.25,
        0.25,  0.25,  0.25,  0.25,  0.25,  0.25,  0.25,  0.25,
        0.25,  0.25,  0.25,  0.25,  0.25,  0.25,  0.25,  0.25,
        0.25,  0.25,  0.25,  0.25,  0.25,  0.25,  0.25,  0.25,
        0.25,  0.25,  0.25,  0.25,  0.25,  0.25,  0.25,  0.25,
        0.20,  0.20,  0.20,  0.20,  0.20,  0.20,  0.20,  0.20,
        0.15,  0.15,  0.00,  0.00,  0.00,  0.00,  0.15,  0.15,
        0.10,  0.10,  0.05,  0.00,  0.05,  0.00,  0.10,  0.10,
    ]
}

# Define piece values and multipliers for controlling squares
control_multipliers = {
    chess.PAWN: 0,
    chess.KNIGHT: 0.03,
    chess.BISHOP: 0.03,
    chess.ROOK: 0.02,
    chess.QUEEN: 0.01,
    chess.KING: 0,
}

color = input("Choose your color (w for white, b for black): ")
if color.lower() == 'w':
    player_color = chess.WHITE
elif color.lower() == 'b':
    player_color = chess.BLACK
else:
    print("Invalid color choice. Defaulting to white.")
    player_color = chess.WHITE

computer_thinking_time = 0

def play_best_move():
    move_number = 1
    global computer_thinking_time

    while True:
        if board.is_checkmate():
            print("Checkmate!")
            break
        if board.is_stalemate():
            print("Stalemate!")
            break
        if board.is_insufficient_material():
            print("Insufficient material!")
            break
        if board.is_repetition(3):
            print("Draw by repetition!")
            break


        if board.turn == player_color:
            user_move = input("Enter your move: ")
            if user_move == "undo":
                if move_number > 1:
                    board.pop()
                    board.pop()
                    move_number -= 1
                    print("Move undone.")
                    print(board)
                else:
                    print("Cannot undo further.")
                continue
            try:
                move = board.parse_san(user_move)
                board.push(move)
            except ValueError:
                print("Invalid move. Please enter a valid move in SAN notation.")
                continue
        else:
            start_time = time.time()
            best_move = evaluate_moves()
            end_time = time.time()
            computer_thinking_time += (end_time - start_time)
            san_move = board.san(best_move)
            print(f"Move {move_number}: {san_move}")
            print(f"Computer thinking time: {computer_thinking_time:.2f} seconds")
            board.push(best_move)
            move_number += 1

        # Print the board
        print(board)
        print()  # New line for readability
    return player_color

def king_safety(color):
    king_sq = board.king(color)
    if king_sq is None:
        return 0.0

    rank = chess.square_rank(king_sq)
    file = chess.square_file(king_sq)

    direction = 1 if color == chess.WHITE else -1
    shield_rank = rank + direction

    safety = 0.0

    if not (0 <= shield_rank <= 7):
        return 0.0

    for df in (-1, 0, 1):
        f = file + df
        if 0 <= f <= 7:
            sq = chess.square(f, shield_rank)
            piece = board.piece_at(sq)

            # Only count ONE pawn per file directly in front
            if piece and piece.piece_type == chess.PAWN and piece.color == color:
                safety += 0.2

    return safety

def passed_pawn_bonus(square, color):
    file = chess.square_file(square)
    rank = chess.square_rank(square)

    for f in (file - 1, file, file + 1):
        if 0 <= f <= 7:
            for r in range(rank + 1, 8) if color == chess.WHITE else range(rank - 1, -1, -1):
                sq = chess.square(f, r)
                p = board.piece_at(sq)
                if p and p.piece_type == chess.PAWN and p.color != color:
                    return 0
    return 0.3 + 0.1 * (rank if color == chess.WHITE else 7 - rank)

def bishop_pair(color):
    return sum(
        1 for sq in chess.SQUARES
        if (p := board.piece_at(sq)) and p.color == color and p.piece_type == chess.BISHOP
    ) >= 2

def evaluate_position(player_color, depth):
    if board.is_check() and not board.is_checkmate():
        captures = [move for move in board.legal_moves]
    else:
        captures = [move for move in board.legal_moves if board.is_capture(move)]
    if len(captures) > 0 and depth > 0:
        capture_evaluations = []
        # Consider the current position without captures first
        if not board.is_check():
            capture_evaluations.append(evaluate_position(player_color, 0))
        for move in captures:
            captured_piece = board.piece_at(move.to_square)
            if board.is_check() or not captured_piece or captured_piece.piece_type != chess.PAWN:
                board.push(move)
                evaluation = evaluate_position(player_color, depth - 1)
                board.pop()
                capture_evaluations.append(evaluation)

        if board.turn == player_color:
            evaluation = min(capture_evaluations)
        else:
            evaluation = max(capture_evaluations)
        return evaluation

    else:
      # Initialize evaluation score
      if board.turn == player_color:
          evaluation = random.randint(-25, -15)/100
      else:
          evaluation = random.randint(15, 25)/100

      if board.is_checkmate():
          if board.turn == player_color:
              return 250
          else:
              return -250

      if board.is_stalemate():
          return 0

      if board.is_insufficient_material():
          return 0

      if board.is_repetition(3):
          return 0

      # King saftey
      evaluation += king_safety(not player_color)
      evaluation -= king_safety(player_color)

      # Doubled pawns penalty
      for color in [chess.WHITE, chess.BLACK]:
          for file in range(8):
              pawns_in_file = sum(1 for square in chess.SQUARES if chess.square_file(square) == file and board.piece_at(square) == chess.Piece(chess.PAWN, color))
              if pawns_in_file > 1:
                  penalty = (pawns_in_file - 1) * 0.5  # Adjust penalty value as needed
                  if color == player_color:
                      evaluation += penalty  # Add penalty for opponent's doubled pawns
                  else:
                      evaluation -= penalty  # Subtract penalty for own doubled pawns

      # Bishop pair
      if bishop_pair(not player_color):
          evaluation += 0.3
      if bishop_pair(player_color):
          evaluation -= 0.3

      if board.turn == player_color:
          attack_factor = 0
      else:
          attack_factor = 1

      for square in chess.SQUARES:
          piece = board.piece_at(square)
          if piece is None:
              continue  # Skip empty squares
          else:
              piece_value = piece_values[piece.piece_type]
              piece_type = piece.piece_type

              control_multiplier = control_multipliers[piece.piece_type]


              if piece.color == player_color:
                  # Player's piece, subtract value
                  evaluation -= piece_value
                  evaluation -= control_multiplier * len(board.attacks(square))



                  if piece.color == chess.WHITE:
                      evaluation -= piece_square_tables[piece_type][chess.square_mirror(square)]
                  else:
                      evaluation -= piece_square_tables[piece_type][square]


              else:
                  # Computer's piece, add value
                  evaluation += piece_value
                  evaluation += control_multiplier * len(board.attacks(square))


                  # Check if the computer's piece is under attack by the player


                  if piece.color == chess.WHITE:
                      evaluation += piece_square_tables[piece_type][chess.square_mirror(square)]
                  else:
                      evaluation += piece_square_tables[piece_type][square]

              if piece.piece_type == chess.PAWN:
                  bonus = passed_pawn_bonus(square, piece.color)
                  if piece.color == player_color:
                      evaluation -= bonus
                  else:
                      evaluation += bonus

      return round(evaluation, 2)


def evaluate_moves():
    lines = []

    #block 1
    for move in board.legal_moves:
        board.push(move)
        evaluation = evaluate_position(player_color, 5)
        lines.append([evaluation, move])
        board.pop()

    # Sort lines with reverse=True for the first level
    lines.sort(key=lambda x: x[0], reverse=True)
    num_lines = min(len(lines), 16)
    lines = lines[:num_lines]
    print(lines)


    #block 2
    for line1 in lines:
        board.push(line1[1])
        line1.append([])
        if board.is_checkmate() or board.is_stalemate() or board.is_insufficient_material() or board.is_repetition(3):
            evaluation = evaluate_position(player_color, 1)
            # Use a dummy move when the game is over
            line1[2].append([evaluation, chess.Move.null(), [[evaluation, chess.Move.null(), [[evaluation, chess.Move.null(), [[evaluation, chess.Move.null(), [[evaluation, chess.Move.null(), [[evaluation, chess.Move.null(), [[evaluation, chess.Move.null(), [[evaluation, chess.Move.null()]]]]]]]]]]]]]]])
            x=0
        else:
            for move in board.legal_moves:
                board.push(move)
                evaluation = evaluate_position(player_color, 4)
                line1[2].append([evaluation, move])
                board.pop()

        # Sort line1's nested moves with reverse=False
        line1[2].sort(key=lambda x: x[0], reverse=False)
        num_line1 = min(len(line1[2]), 5)
        line1[2] = line1[2][:num_line1]
        board.pop()
        line1[0] = line1[2][0][0]

    # Sort lines with reverse=True for the second level
    lines.sort(key=lambda x: x[0], reverse=True)
    num_lines = min(len(lines), 5)
    lines = lines[:num_lines]
    print(lines)

    #block 3
    for line1 in lines:
        board.push(line1[1])
        if board.is_checkmate() or board.is_stalemate() or board.is_insufficient_material():
            x=0
        else:
            for line2 in line1[2]:
                # Check if the move is a dummy move before pushing
                if line2[1] != chess.Move.null():
                    board.push(line2[1])
                line2.append([])
                if board.is_checkmate() or board.is_stalemate() or board.is_insufficient_material():
                    evaluation = evaluate_position(player_color, 1)
                    # Use a dummy move when the game is over
                    line2[2].append([evaluation, chess.Move.null(), [[evaluation, chess.Move.null(), [[evaluation, chess.Move.null()]]]]])
                    x=0
                else:
                    for move in board.legal_moves:
                        board.push(move)
                        evaluation = evaluate_position(player_color, 3)
                        line2[2].append([evaluation, move])
                        board.pop()

                # Sort line2 with reverse=True
                line2[2].sort(key=lambda x: x[0], reverse=True)
                num_line2 = min(len(line2[2]), 3)
                line2[2] = line2[2][:num_line2]
                # Pop the move only if it was pushed
                if line2[1] != chess.Move.null():
                    board.pop()
                line2[0] = line2[2][0][0]

        # Sort line1's nested moves with reverse=False
        line1[2].sort(key=lambda x: x[0], reverse=False)
        num_line1 = min(len(line1[2]), 3)
        line1[2] = line1[2][:num_line1]
        board.pop()
        line1[0] = line1[2][0][0]

    # Sort lines with reverse=True for the third level
    lines.sort(key=lambda x: x[0], reverse=True)
    num_lines = min(len(lines), 3)
    lines = lines[:num_lines]
    print(lines)

    #block 4
    for line1 in lines:
        board.push(line1[1])
        if board.is_checkmate() or board.is_stalemate() or board.is_insufficient_material():
            x=0
        else:
            for line2 in line1[2]:
                if line2[1] != chess.Move.null():
                    board.push(line2[1])
                if board.is_checkmate() or board.is_stalemate() or board.is_insufficient_material():
                    x=0
                else:
                    for line3 in line2[2]:
                        if line3[1] != chess.Move.null():
                            board.push(line3[1])
                        line3.append([])
                        if board.is_checkmate() or board.is_stalemate() or board.is_insufficient_material():
                            evaluation = evaluate_position(player_color, 1)
                            line3[2].append([evaluation, chess.Move.null(), [[evaluation, chess.Move.null()]]])
                            x=0
                        else:
                            for move in board.legal_moves:
                                board.push(move)
                                evaluation = evaluate_position(player_color, 3)
                                line3[2].append([evaluation, move])
                                board.pop()

                        # Sort line3 with reverse=False
                        line3[2].sort(key=lambda x: x[0], reverse=False)
                        num_line3 = min(len(line3[2]), 2)
                        line3[2] = line3[2][:num_line3]
                        if line3[1] != chess.Move.null():
                            board.pop()
                        line3[0] = line3[2][0][0]

                # Sort line2's nested moves with reverse=True
                line2[2].sort(key=lambda x: x[0], reverse=True)
                num_line2 = min(len(line2[2]), 2)
                line2[2] = line2[2][:num_line2]
                if line2[1] != chess.Move.null():
                    board.pop()
                line2[0] = line2[2][0][0]

        # Sort line1's nested moves with reverse=False
        line1[2].sort(key=lambda x: x[0], reverse=False)
        num_line1 = min(len(line1[2]), 2)
        line1[2] = line1[2][:num_line1]
        board.pop()
        line1[0] = line1[2][0][0]

    # Sort lines with reverse=True for the fourth level
    lines.sort(key=lambda x: x[0], reverse=True)
    num_lines = min(len(lines), 2)
    lines = lines[:num_lines]
    print(lines)

    #block 5
    for line1 in lines:
        board.push(line1[1])
        if board.is_checkmate() or board.is_stalemate() or board.is_insufficient_material():
            x=0
        else:
            for line2 in line1[2]:
                if line2[1] != chess.Move.null():
                    board.push(line2[1])
                if board.is_checkmate() or board.is_stalemate() or board.is_insufficient_material():
                    x=0
                else:
                    for line3 in line2[2]:
                        if line3[1] != chess.Move.null():
                            board.push(line3[1])
                        if board.is_checkmate() or board.is_stalemate() or board.is_insufficient_material():
                            x=0
                        else:
                            for line4 in line3[2]:
                                if line4[1] != chess.Move.null():
                                    board.push(line4[1])
                                line4.append([])
                                if board.is_checkmate() or board.is_stalemate() or board.is_insufficient_material():
                                    evaluation = evaluate_position(player_color, 1)
                                    line4[2].append([evaluation, chess.Move.null()])
                                    x=0
                                else:
                                    for move in board.legal_moves:
                                        board.push(move)
                                        evaluation = evaluate_position(player_color, 3)
                                        line4[2].append([evaluation, move])
                                        board.pop()

                                # Sort line4 with reverse=True
                                line4[2].sort(key=lambda x: x[0], reverse=True)
                                num_line4 = min(len(line4[2]), 1)
                                line4[2] = line4[2][:num_line4]
                                if line4[1] != chess.Move.null():
                                    board.pop()
                                line4[0] = line4[2][0][0]

                        # Sort line3's nested moves with reverse=False
                        line3[2].sort(key=lambda x: x[0], reverse=False)
                        num_line3 = min(len(line3[2]), 1)
                        line3[2] = line3[2][:num_line3]
                        if line3[1] != chess.Move.null():
                            board.pop()
                        line3[0] = line3[2][0][0]

                # Sort line2's nested moves with reverse=True
                line2[2].sort(key=lambda x: x[0], reverse=True)
                num_line2 = min(len(line2[2]), 1)
                line2[2] = line2[2][:num_line2]
                if line2[1] != chess.Move.null():
                    board.pop()
                line2[0] = line2[2][0][0]

        # Sort line1's nested moves with reverse=False
        line1[2].sort(key=lambda x: x[0], reverse=False)
        num_line1 = min(len(line1[2]), 1)
        line1[2] = line1[2][:num_line1]
        board.pop()
        line1[0] = line1[2][0][0]

    # Sort lines with reverse=True for the fifth level
    lines.sort(key=lambda x: x[0], reverse=True)
    num_lines = min(len(lines), 1)
    lines = lines[:num_lines]
    print(lines)

    best_move = lines[0][1]
    return best_move


# Call the function to start playing the best move]
play_best_move()

### Flask

from flask import Flask, request, jsonify
from flask_cors import CORS
import chess
import time

# import your engine code here
# from engine import evaluate_moves, board, player_color
# OR paste your engine code ABOVE this Flask section

app = Flask(__name__)
CORS(app)

board = chess.Board()
player_color = chess.WHITE   # default

@app.route("/new_game", methods=["POST"])
def new_game():
    global board, player_color
    board = chess.Board()

    data = request.json
    color = data.get("color", "w")
    player_color = chess.WHITE if color == "w" else chess.BLACK

    return jsonify({"fen": board.fen()})

@app.route("/player_move", methods=["POST"])
def player_move():
    global board

    data = request.json
    san = data["move"]

    try:
        move = board.parse_san(san)
        board.push(move)
    except:
        return jsonify({"error": "Invalid move"}), 400

    return jsonify({"fen": board.fen()})

@app.route("/engine_move", methods=["POST"])
def engine_move():
    global board

    start = time.time()
    best_move = evaluate_moves()
    think_time = time.time() - start

    san = board.san(best_move)
    board.push(best_move)

    return jsonify({
        "move": san,
        "fen": board.fen(),
        "think_time": round(think_time, 2)
    })

if __name__ == "__main__":
    app.run(debug=True)
