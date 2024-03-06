from flask import Flask, request, jsonify
from flask_cors import CORS
from game_class.herustic import HeuristicValueFunctionsSizeN
from game_class.minimax_policy import MinMaxPolicySizeN
from game_class.TicTacToeSizeN import TicTacToeSizeN
from game_class.board import BoardCorrect
from game_class.board import BoardNew
import numpy as np

app = Flask(__name__)
cors = CORS(app)

minimax_policy = MinMaxPolicySizeN(TicTacToeSizeN, BoardNew, None)


@app.route('/api/make_move', methods=['POST'])
def make_move():
    data = request.get_json()
    print(data)
    board = np.array(data.get('board')).flatten()
    current_player_str = data.get('currentPlayer')
    player_mapping = {'black': 1, 'white': -1}
    current_player = player_mapping[current_player_str]
    if current_player is None:
        return jsonify({'error': 'Invalid player'}), 400

    game = TicTacToeSizeN.from_state(board_class=BoardNew, state=tuple(board), player=current_player)
    actions = game.get_actions()
    # action_scores = minimax_policy.get_all_Qs(game.get_state(), current_player, actions)
    # best_action = max(action_scores, key=action_scores.get)
    best_action = minimax_policy(game.get_state(), current_player, actions)
    row, col = divmod(best_action, 15)
    print(row, col)
    return jsonify({'row': row, 'col': col})


if __name__ == '__main__':
    app.run(debug=True, port=5001)
