import pyglet
from pyglet import shapes

black = 1
white = 0


class Board:
    def __init__(self, window):
        self.window = window
        self.window_size = self.window.get_size()
        self.files = "abcdefgh"
        self.board = []
        self.click_pos = None
        self.move_pos = None
        self.square_clicked = None

        color = white
        for rank in reversed(range(1, 9)):
            row = []
            self.board.append(row)
            for file in range(1, 9):
                if file > 1:
                    if color == white:
                        color = black
                    else:
                        color = white
                else:
                    if color == white:
                        color = white
                    else:
                        color = black
                position = self.files[file - 1] + str(rank)
                row.append(Square(position, color))

        self.init_board()

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

    def init_board(self):
        for rank in self.board:
            for square in rank:
                if square.get_position() == 'a8' or square.get_position() == 'h8':
                    square.set_piece(Piece('R', black))
                elif square.get_position() == 'b8' or square.get_position() == 'g8':
                    square.set_piece(Piece('N', black))
                elif square.get_position() == 'c8' or square.get_position() == 'f8':
                    square.set_piece(Piece('B', black))
                elif square.get_position() == 'd8':
                    square.set_piece(Piece('Q', black))
                elif square.get_position() == 'e8':
                    square.set_piece(Piece('K', black))
                elif square.get_position()[1] == '7':
                    square.set_piece(Piece('P', black))
                elif square.get_position() == 'a1' or square.get_position() == 'h1':
                    square.set_piece(Piece('R', black))
                elif square.get_position() == 'b1' or square.get_position() == 'g1':
                    square.set_piece(Piece('N', black))
                elif square.get_position() == 'c1' or square.get_position() == 'f1':
                    square.set_piece(Piece('B', black))
                elif square.get_position() == 'd1':
                    square.set_piece(Piece('Q', black))
                elif square.get_position() == 'e1':
                    square.set_piece(Piece('K', black))
                elif square.get_position()[1] == '2':
                    square.set_piece(Piece('P', black))
        self.print_board()
        self.update_move_lists()

    def move_piece(self, position, move):
        position_rank = int(position[1])
        position_file = self.files.index(position[0])
        move_rank = int(move[1])
        move_file = self.files.index(move[0])
        piece = self.board[position_rank][position_file].get_piece()
        self.board[position_rank][position_file].set_piece(None)
        self.board[move_rank][move_file].set_piece(piece)
        self.print_board()

    def render(self):
        square_width = self.window_size[0] / 8
        square_height = self.window_size[1] / 8
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                if self.board[i][j].get_color() == white:
                    square_color = (255, 255, 255)
                else:
                    square_color = (51, 204, 255)

                new_square_area = [j * square_width,
                                   self.window_size[1] - (i * square_height) - square_height,
                                   (j * square_width) + square_width,
                                   self.window_size[1] - (i * square_height) - square_height + square_height]


                new_square = shapes.Rectangle(x=new_square_area[0],
                                              y=new_square_area[1],
                                              width=square_width, height=square_height,
                                              color=square_color)
                new_square.draw()

                if self.click_pos is not None:
                    if (new_square_area[0] < self.click_pos[0] < new_square_area[2] and
                            new_square_area[1] < self.click_pos[1] < new_square_area[3]):
                        print(self.board[i][j].get_position())
                        self.square_clicked = self.board[i][j].get_position()

                        new_bounding_box = shapes.Rectangle(x=new_square_area[0],
                                                            y=new_square_area[1],
                                                            width=square_width, height=square_height,
                                                            color=(255, 0, 0))
                        new_bounding_box.opacity = 255
                        new_bounding_box.draw()

                if self.move_pos is not None:
                    if (new_square_area[0] < self.move_pos[0] < new_square_area[2] and
                            new_square_area[1] < self.move_pos[1] < new_square_area[3]):
                        print(self.board[i][j].get_position())

                        self.move_piece(self.square_clicked, self.board[i][j].get_position())

                        new_bounding_box = shapes.Rectangle(x=new_square_area[0],
                                                            y=new_square_area[1],
                                                            width=square_width, height=square_height,
                                                            color=(255, 0, 0))
                        new_bounding_box.opacity = 255
                        new_bounding_box.draw()

                if self.board[i][j].piece is None:
                    continue
                else:
                    if self.board[i][j].piece.sprite is None:
                        continue
                    else:
                        square_piece = self.board[i][j].get_piece()
                        new_sprite = pyglet.sprite.Sprite(square_piece.get_sprite(),
                                                          x=j * square_width,
                                                          y=self.window_size[1] - (i * square_height) - square_height)
                        scale_factor = square_width / new_sprite.width
                        new_sprite.scale = scale_factor

                        new_sprite.draw()

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

    def set_click_pos(self, x, y):
        self.click_pos = (x, y)

    def set_move_pos(self, x, y):
        self.move_pos = (x, y)


class Square:
    def __init__(self, position, color):
        self.position = position
        self.piece = None
        self.color = color
        self.possible_moves = []

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


class Piece:
    def __init__(self, piece_type, color):
        self.piece_type = piece_type
        self.color = color

        # Load sprites
        if self.piece_type == 'K' and self.color == white:
            self.sprite = pyglet.image.load('pieces/white-king.png')
        elif self.piece_type == 'K' and self.color == black:
            self.sprite = pyglet.image.load('pieces/black-king.png')
        elif self.piece_type == 'Q' and self.color == white:
            self.sprite = pyglet.image.load('pieces/white-queen.png')
        elif self.piece_type == 'Q' and self.color == black:
            self.sprite = pyglet.image.load('pieces/black-queen.png')
        elif self.piece_type == 'R' and self.color == white:
            self.sprite = pyglet.image.load('pieces/white-rook.png')
        elif self.piece_type == 'R' and self.color == black:
            self.sprite = pyglet.image.load('pieces/black-rook.png')
        elif self.piece_type == 'B' and self.color == white:
            self.sprite = pyglet.image.load('pieces/white-bishop.png')
        elif self.piece_type == 'B' and self.color == black:
            self.sprite = pyglet.image.load('pieces/black-bishop.png')
        elif self.piece_type == 'N' and self.color == white:
            self.sprite = pyglet.image.load('pieces/white-knight.png')
        elif self.piece_type == 'N' and self.color == black:
            self.sprite = pyglet.image.load('pieces/black-knight.png')
        elif self.piece_type == 'P' and self.color == white:
            self.sprite = pyglet.image.load('pieces/white-pawn.png')
        elif self.piece_type == 'P' and self.color == black:
            self.sprite = pyglet.image.load('pieces/black-pawn.png')

    def get_piece_type(self):
        return self.piece_type

    def get_color(self):
        return self.color

    def get_sprite(self):
        return self.sprite
