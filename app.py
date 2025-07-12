from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

player = 1
canPlay = True
player_1_small_moves = {"1": [],
                        "2": [],
                        "3": [],
                        "4": [],
                        "5": [],
                        "6": [],
                        "7": [],
                        "8": [],
                        "9": [],}
player_2_small_moves = {"1": [],
                        "2": [],
                        "3": [],
                        "4": [],
                        "5": [],
                        "6": [],
                        "7": [],
                        "8": [],
                        "9": [],}
player_1_big_moves = []
player_2_big_moves = []
winning_spots = [
    ['1','2','3'],
    ['4','5','6'],
    ['7','8','9'],
    ['1','4','7'],
    ['2','5','8'],
    ['3','6','9'],
    ['1','5','9'],
    ['3','5','7'],
]

def check_small_winner(big, player):
    global player_1_small_moves, player_2_small_moves
    player_moves = []
    big_spot = str(big)

    if player == "1":
        player_moves = player_1_small_moves[big_spot]
    else:
        player_moves = player_2_small_moves[big_spot]

    for spot in winning_spots: 
        if all(item in player_moves for item in spot):
            if player == "1":
                player_1_big_moves.append(big_spot)
            else:
                player_2_big_moves.append(big_spot)

            return True
    
    return False

def check_big_winner(player):
    global player_1_big_moves, player_2_big_moves
    player_moves = []
    
    if player == "1":
        player_moves = player_1_big_moves
    else:
        player_moves = player_2_big_moves

    for spot in winning_spots:
        if all(item in player_moves for item in spot):
            return True

    return False

@app.route("/")
def home():
    return render_template("game.html")

@app.route("/check", methods=["POST"])
def check():
    global player, player_1_big_moves, player_1_small_moves, player_2_big_moves, player_2_small_moves, canPlay
    data = request.get_json()

    canPlay = True
    
    small_win = False
    big_win = False

    if data["small"] in player_1_small_moves[str(data["big"])] or data["small"] in player_2_small_moves[str(data["big"])]:
            canPlay = False
            return jsonify({
                "canPlay": canPlay
            })

    if player % 2 == 1:
        current_player = "1"
        player_1_small_moves[str(data["big"])].append(data["small"])
    else:
        current_player = "2"
        player_2_small_moves[str(data["big"])].append(data["small"])

    small_win = check_small_winner(data["big"], current_player)
    big_win = check_big_winner(current_player)

    if big_win:
        canPlay = False
        return jsonify({
            "winner": current_player,
            "canPlay": canPlay,
            })

    player += 1 

    return jsonify({
        "canPlay": canPlay,
        "currentPlayer": current_player,
        "nextBig": data["small"]
    })

@app.route("/reset", methods=["GET"])
def reset():
    global player, player_1_big_moves, player_1_small_moves, player_2_big_moves, player_2_small_moves, canPlay
    player = 1

    for key in player_1_small_moves:
        player_1_small_moves[key].clear()
    for key in player_2_small_moves:
        player_2_small_moves[key].clear()

    player_1_big_moves.clear()
    player_2_big_moves.clear()

    canPlay = True

    return jsonify({"message": "Game reset!"})

if __name__ == "__main__":
    app.run(port="0.0.0.0", debug=True)
