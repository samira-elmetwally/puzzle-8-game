import tkinter as tk
from tkinter import messagebox
import random
from collections import deque


class CleanBFSPuzzle:
    def __init__(self, root):
        self.root = root
        self.root.title("BFS Puzzle Solver")
        self.root.geometry("350x450")
        self.root.configure(bg="#f0f0f0")

        self.goal = [1, 2, 3, 4, 5, 6, 7, 8, None]
        self.tiles = list(self.goal)
        self.buttons = []

        self.setup_ui()
        self.shuffle_puzzle()

    def setup_ui(self):

        self.main_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.main_frame.pack(expand=True)


        for i in range(9):
            btn = tk.Button(self.main_frame, text="", font=("Arial", 20, "bold"),
                            width=5, height=2, relief="groove")
            btn.grid(row=i // 3, column=i % 3, padx=2, pady=2)
            self.buttons.append(btn)


        control_frame = tk.Frame(self.root, bg="#f0f0f0")
        control_frame.pack(pady=20)

        tk.Button(control_frame, text="Shuffle", command=self.shuffle_puzzle,
                  width=10, bg="#bbb").pack(side=tk.LEFT, padx=5)

        tk.Button(control_frame, text="AI Solve", command=self.run_bfs,
                  width=10, bg="#4CAF50", fg="white").pack(side=tk.LEFT, padx=5)

    def redraw(self):
        for i, val in enumerate(self.tiles):
            if val is None:
                self.buttons[i].config(text="", bg="#d1d1d1", state="disabled")
            else:
                self.buttons[i].config(text=str(val), bg="white", state="normal")
        self.root.update()

    def get_moves(self, state):
        res = []
        empty = state.index(None)
        r, c = divmod(empty, 3)
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < 3 and 0 <= nc < 3:
                new_s = list(state)
                target = nr * 3 + nc
                new_s[empty], new_s[target] = new_s[target], new_s[empty]
                res.append(tuple(new_s))
        return res

    def run_bfs(self):
        start = tuple(self.tiles)
        target = tuple(self.goal)

        # BFS Logic
        queue = deque([(start, [])])
        visited = {start}

        while queue:
            curr, path = queue.popleft()
            if curr == target:
                self.show_path(path)
                return

            for next_s in self.get_moves(curr):
                if next_s not in visited:
                    visited.add(next_s)
                    queue.append((next_s, path + [next_s]))

    def show_path(self, path):
        for step in path:
            self.tiles = list(step)
            self.redraw()
            self.root.after(300)

    def shuffle_puzzle(self):

        for _ in range(12):
            self.tiles = list(random.choice(self.get_moves(tuple(self.tiles))))
        self.redraw()


if __name__ == "__main__":
    root = tk.Tk()
    app = CleanBFSPuzzle(root)
    root.mainloop()
