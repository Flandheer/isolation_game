from flask import Flask
from backend.new_game import GameState

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    new_game = GameState(6, 8, "Frank", "Hugo")
    print_statement = f"This is an isolation game, where {new_game._player_1} plays against {new_game._player_2} " \

    return 'Hello World!' + print_statement



if __name__ == '__main__':
    app.run()
