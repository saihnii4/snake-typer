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
    lines = []
    headstart_count = 3
    snake_pos = [1, 0]
    line_no = 1

    def __init__(self, master=None):
        super().__init__(master)

        self._comparator = """The Woodward–Hoffmann rules are a set of rules devised by Robert
        Burns Woodward and Roald Hoffmann to rationalize or predict certain aspects of the stereochemistry and activation energy of pericyclic"""

        self.source_lines = self._comparator.split("\n")

        self.canvas = tk.Canvas(self, width=600, height=500)
        self.canvas.pack()
        self.canvas.bind_all("<Key>", self.handle_keypress)

        self.view = tk.Text(self, background="orange")
        self.view.insert(tk.INSERT, self.comparator)

        self.view.after(1000, self.loop)

        self.view.tag_configure("eaten", foreground="black", background="green")
        self.view.tag_configure("err", foreground="blue", background="red")
        self.view.tag_configure("inactive", foreground="gray", background="orange")
        self.view.tag_configure("active", foreground="black", background="orange")

        self.view.tag_raise("active", "inactive")
        self.view.tag_raise("err", "active")
        self.view.tag_raise("eaten", "err")

        self.view.tag_add("inactive", format_pos(1, 0), tk.END)
        self.view.configure(state="disabled")
        self.canvas.create_window(300, 300, window=self.view)

        self.pack()

    def _line_ind(self):
        return self.line_no - 1

    line_ind = property(_line_ind)

    def loop(self):
        if self.headstart_count:
            self.headstart_count -= 1
            self.view.after(1000, self.test)
            return

        self.snake_pos[1] += 1
        if self.snake_pos[1] > len(self.lines[self.snake_pos[0]]):
            self.snake_pos[0] += 1

        self.render_text()
        self.view.after(1000, self.loop)

    def render_text(self):
        self.view.tag_add("inactive", format_pos(1, 0), tk.END)
        self.view.tag_remove("err", format_pos(1, 0), tk.END)
        self.view.tag_remove(
            "inactive", format_pos(1, 0), format_pos(self.line_no, len(self.text))
        )
        self.view.tag_add("eaten", format_pos(1, 0), format_pos(*self.snake_pos))

        for i, val in enumerate(self.correct(self.lines[self.line_no])):
            if val:
                continue
            self.view.tag_add("err", format_pos(1, i), format_pos(self.line_no, i + 1))

    def handle_keypress(self, ev: tk.Event):
        if KEYMAP.get(ev.keycode) is None:
            return

        ref = KEYMAP.get(ev.keycode)
        if isinstance(ref, SpecialKey):
            if ref == SpecialKey.BACKSPACE and len(self.text) > 0:
                del self.text[-1]
            if ref == SpecialKey.ENTER:
                self.line_no += 1
                print("TODO")
            self.render_text()
            return

        if len(self.lines[self.line_no]) < len(self.source_lines[self.line_no]):
            self.text.append(KEYMAP.get(ev.keycode))
        self.render_text()

    def correct(self, value):
        for i, char in enumerate(value):
            print(self.source_lines[self.line_no][i], char, i)
            yield self.comparator[self.line_no][i] == char


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
game = Game()
game.pack(side="top", anchor="center", pady=100)
# test = MainScreen(app)
# bar = Bar(test)
# a = Test(test)
# print(test.master)
root.title("Snake Typer")
root.geometry("800x600")
root.mainloop()
