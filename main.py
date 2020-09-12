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
            board.set_click_pos(x, y)

    @window.event
    def on_mouse_release(x, y, button, modifiers):
        if button == 1:
            board.set_move_pos(x, y)


    pyglet.app.run()


