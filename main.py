import pyglet
import chess

SCR_WIDTH = 900
SCR_HEIGHT = 900

if __name__ == "__main__":
    window = pyglet.window.Window(SCR_WIDTH, SCR_HEIGHT)

    board = chess.Board(window)

    @window.event
    def on_draw():
        window.clear()
        board.render()


    @window.event
    def on_mouse_press(x, y, button, modifiers):
        if button == 1:
            board.click(x, y)

    pyglet.app.run()


