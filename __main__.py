import tkinter as tk
from snake_typer import *
import time


class Root(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Frame(self)


class App(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)


class Game(tk.Frame):
    headstart_count = 3
    snake_pos = [1, 0]
    line_no = 1
    _comparator = """The Woodward–Hoffmann rules are a set of rules devised by Robert
        Burns Woodward and Roald Hoffmann to rationalize or predict certain aspects of the stereochemistry and activation energy of pericyclic"""
    source_lines = _comparator.split("\n")
    lines = [[] for _ in range(len(_comparator))]

    def __init__(self, master=None):
        super().__init__(master)
        self.pack()

        self._canvas = tk.Canvas(self, width=600, height=500)
        self._canvas.pack(side='bottom')
        self._canvas.bind_all("<Key>", self.handle_keypress)

        self._view = tk.Text(self, background="white")
        self._view.insert(tk.INSERT, self._comparator)

        self.init()

    def init(self):
        # configure tags
        self._view.tag_configure("eaten", foreground="black", background="green")
        self._view.tag_configure("err", foreground="black", background="red")
        self._view.tag_configure("inactive", foreground="gray", background="white")
        self._view.tag_configure("active", foreground="black", background="white")
        self._view.tag_configure("cursor", underline=True, underlinefg="black")
        # tag hierarchy
        self._view.tag_raise("active", "inactive")
        self._view.tag_raise("err", "active")
        self._view.tag_raise("cursor", "active")
        self._view.tag_raise("eaten", "err")
        # deactivate all chars
        self._view.tag_add("inactive", format_pos(1, 0), tk.END)
        self._view.configure(state="disabled")
        # create canvas
        self._canvas.create_window(300, 300, window=self._view)
        # start snake loop
        self._view.after(1000, self.loop)

    def _line_ind(self):
        return self.line_no - 1

    line_ind = property(_line_ind)

    def _text(self):
        return self.lines[self.line_ind]

    text = property(_text)

    def _pos(self):
        return (self.line_no, len(self.lines[self.line_ind]))

    pos = property(_pos)

    def loop(self):
        if self.headstart_count:
            self.headstart_count -= 1
            self._view.after(1000, self.loop)
            return

        self.snake_pos[1] += 1
        if self.snake_pos[1] > len(self.source_lines[self.snake_pos[0] - 1]):
            self.snake_pos[0] += 1

        if self.snake_pos[1] > len(self.lines[self.snake_pos[0] - 1]):
            # TODO:
            print("CAUGHT UP")
            self._canvas.unbind_all("<Key>")
            return

        self.render_text()
        self._view.after(1000, self.loop)

    def render_text(self):
        print(self.pos)
        # flush...
        self._view.tag_add("inactive", format_pos(1, 0), tk.END)
        self._view.tag_remove("err", format_pos(1, 0), tk.END)
        self._view.tag_remove("cursor", format_pos(1,0), tk.END)
        self._view.tag_remove("active", format_pos(1, 0), tk.END)
        self._view.tag_remove(
            "inactive", format_pos(1, 0), format_pos(self.line_no, len(self.text))
        )
        # then paint
        self._view.tag_add(
            "active", format_pos(1, 0), format_pos(self.line_no, len(self.text))
        )
        self._view.tag_add(
            "cursor", format_pos(*self.pos), format_pos(*(self.pos[0], self.pos[1]+1))
        )
        self._view.tag_add("eaten", format_pos(1, 0), format_pos(*self.snake_pos))

        for i, val in enumerate(self.correct(self.text)):
            if val:
                continue
            self._view.tag_add("err", format_pos(self.line_no, i), format_pos(self.line_no, i + 1))

    def handle_keypress(self, ev: tk.Event):
        # TODO: handle XP ascii keycodes
        if KEYMAP.get(ev.keycode) is None:
            return

        ref = KEYMAP.get(ev.keycode)
        if isinstance(ref, SpecialKey):
            if ref == SpecialKey.BACKSPACE and len(self.text) > 0:
                del self.text[-1]
            if ref == SpecialKey.ENTER and len(self.text) >= len(self.source_lines[self.line_ind]):
                self.line_no += 1
                print("TODO")
            self.render_text()
            return

        if len(self.lines[self.line_ind]) < len(self.source_lines[self.line_ind]):
            self.text.append(KEYMAP.get(ev.keycode))
            self.render_text()

    def correct(self, value):
        for i, char in enumerate(value):
            print(self.source_lines[self.line_ind][i], char, i)
            yield self.source_lines[self.line_ind][i] == char


# class Test(tk.Frame):
#     def __init__(self, master = None):
#         super().__init__(master)
#         self.grid()
#         self.setup()

#     def setup(self):
#         but = tk.Button(text="Click me!", command=self.trigger, width=10)
#         but.pack()

#         a = tk.Label(self, text="Snake Typer")
#         a.pack()

#     @staticmethod
#     def trigger():
#         print("hai")

# class Bar(tk.Frame):
#     def __init__(self, master = None):
#         super().__init__(master)
#         self.grid()
#         self.setup()

#     def setup(self):
#         label = tk.Label(self, text="awdi")
#         label.pack()

# class MainScreen(tk.Frame):
#     def __init__(self, master = None):
#         super().__init__(master)
#         self.pack()

# class Game(tk.Frame):
#     def __init__(self, master = None):
#         pass

root = tk.Tk()
# app = App()
# app.pack(side='top', anchor='center', pady=100)
a = tk.Text(root, background="red", height=40, width=60)
a.insert(tk.INSERT, "hai")
a.pack(side='left')
game = Game(root)
game.pack(side="top", pady=100, expand=True)
# test = MainScreen(app)
# bar = Bar(test)
# a = Test(test)
# print(test.master)
root.title("Snake Typer")
root.geometry("800x600")
root.mainloop()
