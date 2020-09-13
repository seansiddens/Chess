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
        self.square_clicked = None
        self.square_moved = None

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
                square.set_world_position(j * self.square_width, self.window_size[1] -
                                                    ((i+1) * self.square_height))
                square.set_area() # Initialize area variable of square

                # Initialize starting game position of pieces
                if square.get_position() == 'a8' or square.get_position() == 'h8':
                    square.set_piece(Piece('R', BLACK))
                elif square.get_position() == 'b8' or square.get_position() == 'g8':
                    square.set_piece(Piece('N', BLACK))
                elif square.get_position() == 'c8' or square.get_position() == 'f8':
                    square.set_piece(Piece('B', BLACK))
                elif square.get_position() == 'd8':
                    square.set_piece(Piece('Q', BLACK))
                elif square.get_position() == 'e8':
                    square.set_piece(Piece('K', BLACK))
                elif square.get_position()[1] == '7':
                    square.set_piece(Piece('P', BLACK))
                elif square.get_position() == 'a1' or square.get_position() == 'h1':
                    square.set_piece(Piece('R', WHITE))
                elif square.get_position() == 'b1' or square.get_position() == 'g1':
                    square.set_piece(Piece('N', WHITE))
                elif square.get_position() == 'c1' or square.get_position() == 'f1':
                    square.set_piece(Piece('B', WHITE))
                elif square.get_position() == 'd1':
                    square.set_piece(Piece('Q', WHITE))
                elif square.get_position() == 'e1':
                    square.set_piece(Piece('K', WHITE))
                elif square.get_position()[1] == '2':
                    square.set_piece(Piece('P', WHITE))
        self.update_move_lists()

    def move_piece(self, position, move):
        position_rank_index = 8 - int(position[1])
        position_file_index = self.files.index(position[0])
        move_rank_index = 8 - int(move[1])
        move_file_index = self.files.index(move[0])
        piece = self.board[position_rank_index][position_file_index].get_piece()
        self.board[position_rank_index][position_file_index].set_piece(None)
        self.board[move_rank_index][move_file_index].set_piece(piece)
        self.print_board()

    def render(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                current_square = self.board[i][j]

                current_square.render()



                #
                # if self.click_pos is not None:
                #     if (new_square_area[0] < self.click_pos[0] < new_square_area[2] and
                #             new_square_area[1] < self.click_pos[1] < new_square_area[3]):
                #         self.square_clicked = self.board[i][j].get_position()
                #         print(self.square_clicked)
                #
                #         new_bounding_box = shapes.Rectangle(x=new_square_area[0],
                #                                             y=new_square_area[1],
                #                                             width=square_width, height=square_height,
                #                                             color=(255, 0, 0))
                #         new_bounding_box.opacity = 255
                #         new_bounding_box.draw()
                #
                # if self.move_pos is not None:
                #     if (new_square_area[0] < self.move_pos[0] < new_square_area[2] and
                #             new_square_area[1] < self.move_pos[1] < new_square_area[3]):
                #         self.square_moved = self.board[i][j].get_position()
                #         print(self.square_moved)
                #
                #         self.move_piece(self.square_clicked, self.board[i][j].get_position())
                #
                #         new_bounding_box = shapes.Rectangle(x=new_square_area[0],
                #                                             y=new_square_area[1],
                #                                             width=square_width, height=square_height,
                #                                             color=(255, 0, 0))
                #         new_bounding_box.opacity = 255
                #         new_bounding_box.draw()

    def get_file(self, num):
        return [row[num] for row in self.board]

    def update_move_lists(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j].get_piece() is not None:
                    if self.board[i][j].get_piece_type() == 'R':
                        possible_moves = self.get_file(j)
                        for square in possible_moves:
                            if self.board[i][j].get_position() == square.get_position():
                                possible_moves.remove(square)
                        self.board[i][j].set_possible_moves(possible_moves)

    def set_move_pos(self, x, y):
        self.move_pos = (x, y)
        print("Move pos:", self.move_pos)

    def click(self, x, y):
        self.click_pos = (x, y)
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                current_square = self.board[i][j]
                if current_square.is_clicked(self.click_pos):
                    print(current_square.get_position(), "clicked")


class Square:
    def __init__(self, position, color, window):
        self.position = position        # Position on board
        self.world_position = None      # Coordinates for rendering to screen
        self.area = None
        self.piece = None               # Piece object on square
        self.color = color              # Color of square
        self.possible_moves = []        # List of squares which could be moved to from a given square based on piece

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

    def get_color(self):
        return self.color

    def get_position(self):
        return self.position

    def get_piece(self):
        return self.piece

    def set_piece(self, piece):
        self.piece = piece

    def set_possible_moves(self, move_list):
        self.possible_moves = move_list

    def get_piece_type(self):
        return self.piece.piece_type

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

        # --- Piece rendering ---
        if self.piece is not None:
            piece_sprite = pyglet.sprite.Sprite(self.piece.get_sprite(),
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
            self.sprite = pyglet.image.load('pieces/white-pawn.png')
        elif self.piece_type == 'P' and self.color == BLACK:
            self.sprite = pyglet.image.load('pieces/black-pawn.png')

    def get_piece_type(self):
        return self.piece_type

    def get_color(self):
        return self.color

    def get_sprite(self):
        return self.sprite
