# Connect4
Standard game of connect 4 plus "Gravity Tic Tac Toe" and even build your own board and game.
--------------------------------------------------------------------------------------------------
Classes/Objects: Board, Player, Game
  Board
    Class Attritbutes: x, y
    Class Variables: board_ref, board_count
    Class Functions: update_board(self, play, symbol), plays_to_coords(self, plays), print_board(self)
  Player
    Class Attritbutes: name, symbol, plays, won
    Class Functions: update_player(self)
  Game
    Class Attritbutes: board_x, board_y, player_count, win_count
    Class Variables: board, player_data
    Class Functions: get_player_data(self), get_play(self, player), check_win(self, spaces), play(self)

Game Functions: make_custom_game(), select_game(games)

Misc. Functions: num_to_letter(y)

Game Variables: games, game
