import time
import random
import pyglet
from pyglet import shapes


BLACK = 1
WHITE = 0


class Board:
    def __init__(self, window):
        self.window = window                       # Pyglet window used for rendering
        self.window_size = self.window.get_size()  # Width and height of game window in pixels
        self.files = "abcdefgh"
        self.board = []
        self.click_pos = None         # X and Y position of last click
        self.last_square_selected = None
        self.color_to_move = WHITE
        self.game_over = False

        # Width and height of board squares in pixels
        self.square_width = self.window_size[0] / 8
        self.square_height = self.window_size[1] / 8

        self.init_board()

    # Prints board state to terminal
    def print_board(self):
        print('-----------------------------------------------------------')
        for rank in self.board:
            for square in rank:
                if not square.get_piece():
                    print(' ', end=' ')
                else:
                    print(square.get_piece().get_piece_type(), end=' ')
            print('')
        print('-----------------------------------------------------------')

    # Sets up the board by assigning squares with pieces
    # Also sets world position of each square for rendering
    def init_board(self):
        # Create a 2D Array of Square objects, setting their proper color
        color = WHITE
        for rank in reversed(range(1, 9)):
            row = []
            self.board.append(row)
            for file in range(1, 9):
                # Assigns colors to make checkerboard appearance
                if file > 1:
                    if color == WHITE:
                        color = BLACK
                    else:
                        color = WHITE
                else:
                    if color == WHITE:
                        color = WHITE
                    else:
                        color = BLACK
                position = self.files[file - 1] + str(rank)  # Assigns board's positional notation
                row.append(Square(position, color, self.window))

        # Iterate over board array and initialize world positions and pieces
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                square = self.board[i][j]

                # Initialize world position of each square for rendering
                square.set_world_position(j * self.square_width,
                                          self.window_size[1] - ((i+1) * self.square_height))
                square.set_area()  # Initialize area variable of square

                # Initialize starting game position of pieces
                if square.position == 'a8' or square.position == 'h8':
                    square.set_piece(Piece('R', BLACK))
                elif square.position == 'b8' or square.position == 'g8':
                    square.set_piece(Piece('N', BLACK))
                elif square.position == 'c8' or square.position == 'f8':
                    square.set_piece(Piece('B', BLACK))
                elif square.position == 'd8':
                    square.set_piece(Piece('Q', BLACK))
                elif square.position == 'e8':
                    square.set_piece(Piece('K', BLACK))
                elif square.position[1] == '7':
                    square.set_piece(Piece('P', BLACK))
                elif square.position == 'a1' or square.position == 'h1':
                    square.set_piece(Piece('R', WHITE))
                elif square.position == 'b1' or square.position == 'g1':
                    square.set_piece(Piece('N', WHITE))
                elif square.position == 'c1' or square.position == 'f1':
                    square.set_piece(Piece('B', WHITE))
                elif square.position == 'd1':
                    square.set_piece(Piece('Q', WHITE))
                elif square.position == 'e1':
                    square.set_piece(Piece('K', WHITE))
                elif square.position[1] == '2':
                    square.set_piece(Piece('P', WHITE))
        self.update_move_lists()

    # Moves game piece from one square to another
    def move_piece(self, start_square, end_square):
        # if end square isn't in possible move list, move is not possible
        if end_square not in start_square.possible_moves:
            print("NOT POSSIBLE")
            return -1
        piece = start_square.piece
        if piece is not None:
            if piece.piece_type == 'P':
                piece.has_moved = True
        start_square.set_piece(None)
        end_square.set_piece(piece)
        self.update_move_lists()

        # Change turns
        if self.color_to_move == WHITE:
            self.color_to_move = BLACK
            self.black_controller()
        else:
            self.color_to_move = WHITE

    def render(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                current_square = self.board[i][j]
                current_square.render()

    def get_file(self, num):
        return [row[num] for row in self.board]

    def update_move_lists(self):
        print("UPDATING MOVE LISTS")
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j].piece is not None:
                    current_square = self.board[i][j]
                    # --- Update possible move lists of each square with a piece based on piece type

                    # Calculate move list for a king
                    if current_square.piece.piece_type == 'K':
                        current_square.possible_moves = []  # Clears move list
                        # Iterate over each square in area around king
                        for y in range((i-1), (i+2)):
                            if y < 0 or y >= 8:
                                continue    # Skips squares out of index
                            for x in range((j-1), (j+2)):
                                if x < 0 or y >= 8:
                                    continue    # Skip squares out of index
                                if x == j and y == i:
                                    continue    # Can't move to it's own square
                                if self.board[y][x].piece is not None:
                                    if self.board[y][x].piece.color == current_square.piece.color:
                                        continue    # Can't move to square with same color piece

                                current_square.possible_moves.append(self.board[y][x])

                    # Calculate move list for queen
                    if current_square.piece.piece_type == 'Q':
                        current_square.possible_moves = []

                        # Iterate over each square in its rank
                        for x in reversed(range(j)):
                            if self.board[i][x].piece is not None:
                                if self.board[i][x].piece.color != current_square.piece.color:
                                    current_square.possible_moves.append(self.board[i][x])
                                    break   # Prevents jumping over of pieces
                                elif self.board[i][x].piece.color == current_square.piece.color:
                                    break
                            current_square.possible_moves.append(self.board[i][x])
                        for x in range(j+1, 8):
                            if self.board[i][x].piece is not None:
                                if self.board[i][x].piece.color != current_square.piece.color:
                                    current_square.possible_moves.append(self.board[i][x])
                                    break   # Prevents jumping over of pieces
                                elif self.board[i][x].piece.color == current_square.piece.color:
                                    break
                            current_square.possible_moves.append(self.board[i][x])

                        # Iterate over each square in file
                        for y in reversed(range(i)):
                            if self.board[y][j].piece is not None:
                                if self.board[y][j].piece.color != current_square.piece.color:
                                    current_square.possible_moves.append(self.board[y][j])
                                    break
                                elif self.board[y][j].piece.color == current_square.piece.color:
                                    break
                            current_square.possible_moves.append(self.board[y][j])
                        for y in range(i+1, 8):
                            if self.board[y][j].piece is not None:
                                if self.board[y][j].piece.color != current_square.piece.color:
                                    current_square.possible_moves.append(self.board[y][j])
                                    break   # Prevents jumping over of pieces
                                elif self.board[y][j].piece.color == current_square.piece.color:
                                    break
                            current_square.possible_moves.append(self.board[y][j])

                        # Iterate over diagonals
                        for w in range(1, 8):
                            if i-w >= 0 and j-w >= 0:
                                if self.board[i-w][j-w].piece is not None:
                                    if self.board[i-w][j-w].piece.color != current_square.piece.color:
                                        current_square.possible_moves.append(self.board[i-w][j-w])
                                        break  # Prevents jumping over of pieces
                                    elif self.board[i-w][j-w].piece.color == current_square.piece.color:
                                        break
                                current_square.possible_moves.append(self.board[i-w][j-w])
                        for w in range(1, 8):
                            if i+w < 8 and j+w < 8:
                                if self.board[i+w][j+w].piece is not None:
                                    if self.board[i+w][j+w].piece.color != current_square.piece.color:
                                        current_square.possible_moves.append(self.board[i+w][j+w])
                                        break  # Prevents jumping over of pieces
                                    elif self.board[i+w][j+w].piece.color == current_square.piece.color:
                                        break
                                current_square.possible_moves.append(self.board[i+w][j+w])
                        for w in range(1, 8):
                            if i+w < 8 and j-w >= 0:
                                if self.board[i+w][j-w].piece is not None:
                                    if self.board[i+w][j-w].piece.color != current_square.piece.color:
                                        current_square.possible_moves.append(self.board[i+w][j-w])
                                        break  # Prevents jumping over of pieces
                                    elif self.board[i+w][j-w].piece.color == current_square.piece.color:
                                        break
                                current_square.possible_moves.append(self.board[i+w][j-w])
                        for w in range(1, 8):
                            if i-w >= 0 and j+w < 8:
                                if self.board[i-w][j+w].piece is not None:
                                    if self.board[i-w][j+w].piece.color != current_square.piece.color:
                                        current_square.possible_moves.append(self.board[i-w][j+w])
                                        break  # Prevents jumping over of pieces
                                    elif self.board[i-w][j+w].piece.color == current_square.piece.color:
                                        break
                                current_square.possible_moves.append(self.board[i-w][j+w])

                    # Calculate move list for Bishop
                    if current_square.piece.piece_type == 'B':
                        current_square.possible_moves = []
                        # Iterate over diagonals
                        for w in range(1, 8):
                            if i-w >= 0 and j-w >= 0:
                                if self.board[i-w][j-w].piece is not None:
                                    if self.board[i-w][j-w].piece.color != current_square.piece.color:
                                        current_square.possible_moves.append(self.board[i-w][j-w])
                                        break  # Prevents jumping over of pieces
                                    elif self.board[i-w][j-w].piece.color == current_square.piece.color:
                                        break
                                current_square.possible_moves.append(self.board[i-w][j-w])
                        for w in range(1, 8):
                            if i+w < 8 and j+w < 8:
                                if self.board[i+w][j+w].piece is not None:
                                    if self.board[i+w][j+w].piece.color != current_square.piece.color:
                                        current_square.possible_moves.append(self.board[i+w][j+w])
                                        break  # Prevents jumping over of pieces
                                    elif self.board[i+w][j+w].piece.color == current_square.piece.color:
                                        break
                                current_square.possible_moves.append(self.board[i+w][j+w])
                        for w in range(1, 8):
                            if i+w < 8 and j-w >= 0:
                                if self.board[i+w][j-w].piece is not None:
                                    if self.board[i+w][j-w].piece.color != current_square.piece.color:
                                        current_square.possible_moves.append(self.board[i+w][j-w])
                                        break  # Prevents jumping over of pieces
                                    elif self.board[i+w][j-w].piece.color == current_square.piece.color:
                                        break
                                current_square.possible_moves.append(self.board[i+w][j-w])
                        for w in range(1, 8):
                            if i-w >= 0 and j+w < 8:
                                if self.board[i-w][j+w].piece is not None:
                                    if self.board[i-w][j+w].piece.color != current_square.piece.color:
                                        current_square.possible_moves.append(self.board[i-w][j+w])
                                        break  # Prevents jumping over of pieces
                                    elif self.board[i-w][j+w].piece.color == current_square.piece.color:
                                        break
                                current_square.possible_moves.append(self.board[i-w][j+w])

                    # Calculate move list for knight
                    if current_square.piece.piece_type == 'N':
                        current_square.possible_moves = []
                        if i-1 >= 0 and j-2 >= 0:
                            if self.board[i-1][j-2].piece is not None:
                                if self.board[i-1][j-2].piece.color != current_square.piece.color:
                                    current_square.possible_moves.append(self.board[i-1][j-2])
                            else:
                                current_square.possible_moves.append(self.board[i - 1][j - 2])
                        if i-2 >= 0 and j-1 >= 0:
                            if self.board[i-2][j-1].piece is not None:
                                if self.board[i-2][j-1].piece.color != current_square.piece.color:
                                    current_square.possible_moves.append(self.board[i-2][j-1])
                            else:
                                current_square.possible_moves.append(self.board[i - 2][j - 1])
                        if i-2 >= 0 and j+1 < 8:
                            if self.board[i-2][j+1].piece is not None:
                                if self.board[i-2][j+1].piece.color != current_square.piece.color:
                                    current_square.possible_moves.append(self.board[i-2][j+1])
                            else:
                                current_square.possible_moves.append(self.board[i - 2][j + 1])
                        if i-1 >= 0 and j+2 < 8:
                            if self.board[i-1][j+2].piece is not None:
                                if self.board[i-1][j+2].piece.color != current_square.piece.color:
                                    current_square.possible_moves.append(self.board[i-1][j+2])
                            else:
                                current_square.possible_moves.append(self.board[i - 1][j + 2])
                        if i+1 < 8 and j+2 < 8:
                            if self.board[i+1][j+2].piece is not None:
                                if self.board[i+1][j+2].piece.color != current_square.piece.color:
                                    current_square.possible_moves.append(self.board[i+1][j+2])
                            else:
                                current_square.possible_moves.append(self.board[i + 1][j + 2])
                        if i+2 < 8 and j+1 < 8:
                            if self.board[i+2][j+1].piece is not None:
                                if self.board[i+2][j+1].piece.color != current_square.piece.color:
                                    current_square.possible_moves.append(self.board[i+2][j+1])
                            else:
                                current_square.possible_moves.append(self.board[i + 2][j + 1])
                        if i+2 < 8 and j-1 >= 0:
                            if self.board[i+2][j-1].piece is not None:
                                if self.board[i+2][j-1].piece.color != current_square.piece.color:
                                    current_square.possible_moves.append(self.board[i+2][j-1])
                            else:
                                current_square.possible_moves.append(self.board[i + 2][j - 1])
                        if i+1 < 8 and j-2 >= 0:
                            if self.board[i+1][j-2].piece is not None:
                                if self.board[i+1][j-2].piece.color != current_square.piece.color:
                                    current_square.possible_moves.append(self.board[i+1][j-2])
                            else:
                                current_square.possible_moves.append(self.board[i + 1][j - 2])

                    # Calculate move list for pawn
                    if current_square.piece.piece_type == 'P':
                        current_square.possible_moves = []
                        # White pawns
                        if current_square.piece.color == WHITE:
                            # If pawn hasn't moved, can move two space forward
                            if not current_square.piece.has_moved:
                                for y in range(1, 3):
                                    if i-y >= 0:
                                        if self.board[i-y][j].piece is None:
                                            current_square.possible_moves.append(self.board[i-y][j])
                            else:
                                if i-1 >= 0:
                                    if self.board[i-1][j].piece is None:
                                        current_square.possible_moves.append(self.board[i-1][j])
                            if i-1 >= 0 and j-1 >= 0:
                                if self.board[i-1][j-1].piece is not None and self.board[i-1][j-1].piece.color != WHITE:
                                    current_square.possible_moves.append(self.board[i-1][j-1])
                            if i-1 >= 0 and j+1 < 8:
                                if self.board[i - 1][j + 1].piece is not None and self.board[i - 1][j + 1].piece.color != WHITE:
                                    current_square.possible_moves.append(self.board[i - 1][j + 1])
                        # Black pawns
                        else:
                            if not current_square.piece.has_moved:
                                for y in range(1, 3):
                                    if i + y < 8:
                                        if self.board[i + y][j].piece is None:
                                            current_square.possible_moves.append(self.board[i + y][j])
                            else:
                                if i+1 < 8:
                                    if self.board[i+1][j].piece is None:
                                        current_square.possible_moves.append(self.board[i+1][j])
                            if i+1 < 8 and j+1 < 8:
                                if self.board[i+1][j+1].piece is not None and self.board[i+1][j+1].piece.color != BLACK:
                                    current_square.possible_moves.append(self.board[i+1][j+1])
                            if i+1 < 8 and j-1 >= 0:
                                if self.board[i+1][j-1].piece is not None and self.board[i+1][j-1].piece.color != BLACK:
                                    current_square.possible_moves.append(self.board[i+1][j-1])

                    # Calculate move list for rook
                    if current_square.piece.piece_type == 'R':
                        current_square.possible_moves = []
                        for y in reversed(range(i)):
                            if self.board[y][j].piece is not None:
                                if self.board[y][j].piece.color != current_square.piece.color:
                                    current_square.possible_moves.append(self.board[y][j])
                                    break
                                elif self.board[y][j].piece.color == current_square.piece.color:
                                    break
                            current_square.possible_moves.append(self.board[y][j])
                        for y in range(i+1, 8):
                            if self.board[y][j].piece is not None:
                                if self.board[y][j].piece.color != current_square.piece.color:
                                    current_square.possible_moves.append(self.board[y][j])
                                    break   # Prevents jumping over of pieces
                                elif self.board[y][j].piece.color == current_square.piece.color:
                                    break
                            current_square.possible_moves.append(self.board[y][j])
                        # Iterate over each square in its rank
                        for x in reversed(range(j)):
                            if self.board[i][x].piece is not None:
                                if self.board[i][x].piece.color != current_square.piece.color:
                                    current_square.possible_moves.append(self.board[i][x])
                                    break   # Prevents jumping over of pieces
                                elif self.board[i][x].piece.color == current_square.piece.color:
                                    break
                            current_square.possible_moves.append(self.board[i][x])
                        for x in range(j+1, 8):
                            if self.board[i][x].piece is not None:
                                if self.board[i][x].piece.color != current_square.piece.color:
                                    current_square.possible_moves.append(self.board[i][x])
                                    break   # Prevents jumping over of pieces
                                elif self.board[i][x].piece.color == current_square.piece.color:
                                    break
                            current_square.possible_moves.append(self.board[i][x])

    def click(self, x, y):
        self.click_pos = (x, y)
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                current_square = self.board[i][j]
                if current_square.is_clicked(self.click_pos):

                    # First click onto square with piece
                    if current_square.piece and self.last_square_selected is None and current_square.piece.color == self.color_to_move:
                        current_square.is_selected = True
                        if current_square.possible_moves is not None:
                            for square in current_square.possible_moves:
                                square.is_selected = True
                            self.last_square_selected = current_square

                    # Second click if a square with piece is already selected
                    elif self.last_square_selected is not None:
                        # Move piece to new square
                        self.move_piece(self.last_square_selected, current_square)

                        # De-select squares
                        # self.last_square_selected.is_selected = False
                        # current_square.is_selected = False
                        for rank in self.board:
                            for square in rank:
                                square.is_selected = False

                        self.last_square_selected = None

    def random_move(self):
        square_list = []
        found_square = False
        for rank in self.board:
            for square in rank:
                if square.piece:
                    if square.piece.color == BLACK and square.possible_moves is not None:
                        if len(square.possible_moves) > 0:
                            found_square = True
                            square_list.append(square)

        if not found_square:
            self.end_game()

        random_square = random.choice(square_list)
        random_move = random.choice(random_square.possible_moves)

        self.move_piece(random_square, random_move)

    def black_controller(self):
        self.random_move()

    def end_game(self):
        print("Game over")
        self.game_over = True
        time.sleep(999)


class Square:
    def __init__(self, position, color, window):
        self.position = position        # Position on board
        self.world_position = None      # Coordinates for rendering to screen
        self.area = None
        self.piece = None               # Piece object on square
        self.color = color              # Color of square
        self.possible_moves = None        # List of squares which could be moved to from a given square based on piece
        self.is_selected = False

        self.window = window
        self.window_size = self.window.get_size()
        self.square_width = self.window_size[0] / 8
        self.square_height = self.window_size[1] / 8

    def set_world_position(self, x, y):
        self.world_position = (x, y)

    def set_area(self):
        # Four world-coordinates representing area of square
        self.area = [self.world_position[0],                       # x1
                     self.world_position[1],                       # y1
                     self.world_position[0] + self.square_width,   # x2
                     self.world_position[1] + self.square_height]  # y2

    def set_piece(self, piece):
        self.piece = piece

    def set_possible_moves(self, move_list):
        self.possible_moves = move_list

    # Draws square to screen using world position, also renders piece sprite if applicable
    def render(self):
        # --- Square rendering ---
        if self.color == WHITE:
            square_color = (255, 255, 255)  # Display color for white squares
        else:
            square_color = (51, 204, 255)  # Display color for black squares

        rendered_square = shapes.Rectangle(self.world_position[0], self.world_position[1],
                                           width=self.square_width, height=self.square_height,
                                           color=square_color)
        rendered_square.draw()

        if self.is_selected:
            highlight_square = shapes.Rectangle(x=self.world_position[0],
                                                y=self.world_position[1],
                                                width=self.square_width, height=self.square_height,
                                                color=(255, 0, 0))
            highlight_square.opacity = 100
            highlight_square.draw()

        # --- Piece rendering ---
        if self.piece is not None:
            piece_sprite = pyglet.sprite.Sprite(self.piece.sprite,
                                                x=self.world_position[0],
                                                y=self.world_position[1])
            scale_factor = self.square_width / piece_sprite.width
            piece_sprite.scale = scale_factor

            piece_sprite.draw()

    def is_clicked(self, click_pos):
        if (self.area[0] < click_pos[0] < self.area[2] and
                self.area[1] < click_pos[1] < self.area[3]):
            return True
        else:
            return False


class Piece:
    def __init__(self, piece_type, color):
        self.piece_type = piece_type
        self.color = color
        self.has_moved = None

        # Load sprites
        if self.piece_type == 'K' and self.color == WHITE:
            self.sprite = pyglet.image.load('pieces/white-king.png')
        elif self.piece_type == 'K' and self.color == BLACK:
            self.sprite = pyglet.image.load('pieces/black-king.png')
        elif self.piece_type == 'Q' and self.color == WHITE:
            self.sprite = pyglet.image.load('pieces/white-queen.png')
        elif self.piece_type == 'Q' and self.color == BLACK:
            self.sprite = pyglet.image.load('pieces/black-queen.png')
        elif self.piece_type == 'R' and self.color == WHITE:
            self.sprite = pyglet.image.load('pieces/white-rook.png')
        elif self.piece_type == 'R' and self.color == BLACK:
            self.sprite = pyglet.image.load('pieces/black-rook.png')
        elif self.piece_type == 'B' and self.color == WHITE:
            self.sprite = pyglet.image.load('pieces/white-bishop.png')
        elif self.piece_type == 'B' and self.color == BLACK:
            self.sprite = pyglet.image.load('pieces/black-bishop.png')
        elif self.piece_type == 'N' and self.color == WHITE:
            self.sprite = pyglet.image.load('pieces/white-knight.png')
        elif self.piece_type == 'N' and self.color == BLACK:
            self.sprite = pyglet.image.load('pieces/black-knight.png')
        elif self.piece_type == 'P' and self.color == WHITE:
            self.has_moved = False
            self.sprite = pyglet.image.load('pieces/white-pawn.png')
        elif self.piece_type == 'P' and self.color == BLACK:
            self.has_moved = False
            self.sprite = pyglet.image.load('pieces/black-pawn.png')

