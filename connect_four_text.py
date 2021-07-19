'''---imported libraries---'''
import string
'''--- test/debug variables ---'''
board = [0, 0, 0, 0, 0, 0, 0]
test_spaces = [[1,1],[1,4],[1,2],[1,3],[1,5],[1,6]]
test_spaces_2 = [[1,1],[4,4],[2,2],[3,3],[5,5],[6,6]]
test_spaces_3 = [[1,0],[2,0]]
test_spaces_4 = [[1,1],[3,4],[4,2],[2,3],[3,2],[7,3],[4,1],[7,2]]
test_spaces_5 = [[1,1],[3,4],[4,2],[2,3],[3,2],[7,3],[4,1],[7,2],[2,2],[5,2]]
test_spaces_6 = [[1,1],[3,4],[4,2],[2,3],[3,2],[7,3],[4,1],[7,2],[4,4],[5,4]]

'''---Misc. Functions---'''

def num_to_letter(y):
    reference = []
    letter = ''
    print(letter)
    for i in range(y):
        counter = i%26
        char = string.ascii_uppercase[counter]
        if counter == 0:
            letter = char*(int(i/26)+1)
        else:
            letter = letter[:-1]+char
        reference.append(letter)
    return reference

'''---Board---'''

class Board(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.x_ref = num_to_letter(self.x)
        self.board_ref = {self.x_ref[i]+str(j+1):[[i+1,j+1],'O'] for i in range(self.x) for j in range(self.y)}
        self.board_count = {i:0 for i in self.x_ref}  
                
    def update_board(self, play, symbol):
        self.play = play
        self.symbol = symbol
        self.board_ref[self.play][1] = self.symbol
        
    def plays_to_coords(self, plays):
        self.plays = plays
        return [self.board_ref[i][0] for i in self.plays]

    '''def coord_to_play(coord):
    x_ref = num_to_letter(coord[0])
    play = x_ref[-1]+str(coord[1])
    return play'''

    def print_board(self):
        board = [[self.board_ref[i+str(j+1)][1] for i in self.x_ref] for j in range(self.y)]
        flip_board = board[::-1]
        row_ref = self.y
        col_ref = self.x
        y_offset = ' '*(len(str(self.y))-len(str(row_ref)))
        x_offset = ' '*(len(str(self.x)))
        row = y_offset+str(row_ref)
        col = [i+' '*(len(str(self.x))-len(i)) for i in num_to_letter(self.x)]
        for i in flip_board:
            print(str(row)+' '+(x_offset.join(i)))
            row_ref -= 1
            y_offset = ' '*(len(str(self.y))-len(str(row_ref))) 
            row = y_offset+str(row_ref)
        col_offset = ' '*(len(str(self.y))+1)
        print(col_offset+' '.join(col))

'''---Players---'''

class Player(object):
    def __init__(self, name, symbol, plays, won):
        self.name = name
        self.symbol = symbol
        self.plays = plays
        self.won = won

    def update_player(self):
        count = 1
        forbidden_names = []
        forbidden_symbols = ['O','o','0','']
        new_name = input(self.name+'- Select a name: ')
        while new_name in forbidden_names:
            new_name = input('Sorry, that name has already been taken. \nPlease select another name: ')
        else:
            if new_name == '' or new_name.isspace():
                self.name = self.name
            else:
                self.name = new_name
                forbidden_names.append(new_name)
        new_symbol = input(self.name+', select your symbol: ')
        while new_symbol in forbidden_symbols or new_symbol.isspace() or len(new_symbol) > 1:
            new_symbol = input('You can\'t use that. \nSelect another symbol: ')
        else:
            self.symbol = new_symbol
            forbidden_symbols.append(new_symbol)
            print(self.name+' selected \''+self.symbol+'\'.')
    
'''---Game---'''

class Game(object):
    
    def __init__(self, board_x, board_y, player_count, win_count):
        self.board_x = board_x
        self.board_y = board_y
        self.player_count = player_count
        self.win_count = win_count
        self.board = Board(board_x, board_y)
        self.player_data = {'p'+str(i+1):Player('Player'+str(i+1),'O',[],False) for i in range(self.player_count)}

    '''getting player input'''
    def get_player_data(self):
        for p in self.player_data:
            self.player_data[p].update_player()
    
    def get_play(self, player):
        self.player = player
        play = input(player.name+'- Select a space: ')
        play = play.upper()
        while play not in self.board.x_ref or self.board.board_count[play]>=self.board_y:
            if play not in self.board.x_ref:
                play = input('That is not a valid input. \nPlease select another space: ')
                play = play.upper()
            elif self.board.board_count[play]>=self.board_y:
                play = input('That space has been filled. \nPlease select another space: ')
                play = play.upper()
        else:
            self.board.board_count[play] += 1
            play = play+str(self.board.board_count[play])
            self.player.plays.append(play)
            self.board.update_board(play, self.player.symbol)
            p_coords = self.board.plays_to_coords(player.plays)
        return p_coords

    '''Counting Plays/deciding winner Funcion''' 
    def check_win(self, spaces):
        self.spaces = spaces
        ref = self.spaces[-1]
        pile = self.spaces[:-1]
        streak = 0
        instructions = [[1,0],[0,1],[1,1],[-1,1]]
        for i in instructions:
            adjacent_plays = 1
            count = 1
            tester1 = [x[0]+(x[1]*count) for x in zip(ref,i)]
            tester2 = [x[0]+(x[1]*-count) for x in zip(ref,i)]
            while tester1 in pile or tester2 in pile:
                if tester1 in pile:
                    pile.remove(tester1)
                    adjacent_plays += 1
                else:
                    tester1 = None
                if tester2 in pile:
                    pile.remove(tester2)
                    adjacent_plays += 1
                else:
                    tester2 = None
                count += 1
                tester1 = [x[0]+(x[1]*count) for x in zip(ref,i)] if tester1!=None else None
                tester2 = [x[0]+(x[1]*-count) for x in zip(ref,i)] if tester2!=None else None
            streak = adjacent_plays if adjacent_plays > streak else streak
            if streak >= self.win_count:
                break
        return True if streak >= self.win_count else False
    
    '''where the game happens'''
    def play(self):
        turns = self.board_x * self.board_y
        winner = 'Stalemate.'
        self.get_player_data()
        for i in range(turns):
            round_count = i%len(self.player_data)
            p = self.player_data['p'+str(round_count+1)]
            self.board.print_board()
            play = self.get_play(p)
            p.won = self.check_win(play)
            if p.won:
                self.board.print_board()
                winner = (p.name+' is the winner!')
                break
        print(winner)    

'''---Selecting a Game---'''
def make_custom_game():
    g = {'x':['board\'s x',7],'y':['board\s y',6],'p':['number of players',2],'w':['win count',4]}
    for i in g:
        x = input('Select the '+g[i][0]+': ')
        while x != '' and (not x.isdigit()) and (not x.isspace()):
            x = input('Sorry, invalid input.\nSelect the '+g[i][0]+': ')
        else:
            if x == '' or x.isspace():
                g[i][1] = g[i][1]
            else:
                g[i][1]= int(x)
    custom_game = Game(g['x'][1],g['y'][1],g['p'][1],g['w'][1])
    return custom_game

def select_game(games):
    game_titles = [i for i in games if i != 'Debug']
    game_titles.append('Exit')
    games_display = '"'+'", "'.join(game_titles[:-2])+'", and "'+game_titles[-2]+'". If you\'re done, type "exit".'
    game = input('We have '+games_display+': ')
    game = ' '.join([i.capitalize() for i in game.split()])
    while game not in game_titles:
        game = input('Sorry, we don\'t have that. Please try something else: ')
    else:
        if game == 'Custom':
            games[game] = make_custom_game()
    return game

'''---Main---'''
games = {'Classic':Game(7,6,2,4), 'Gravity Tic Tac Toe': Game(3,3,2,3),'Debug':Game(9,8,1,4), 'Custom':Game(7,6,2,4)}
print('Welcome to Connect 4!\n\nPlease select a game.')
game = select_game(games)
while game != 'Exit':
    games[game].play()
    print('Welcome back!\nPlease select a game.')
    game = select_game(games)
else:
    print('thanks for playing!')
          
'''--- debug area ---'''
