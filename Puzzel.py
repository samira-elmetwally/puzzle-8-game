import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk  
import random


class SimpleImagePuzzle:
    def __init__(self, root):
        self.root = root
        self.root.title("Duck Puzzel Game")


        self.image_path = "Puzzel.jpg"
        # --------------------------

        self.size = 3
        self.tiles = []
        self.buttons = []

        try:
            self.load_and_slice_image()
            self.create_widgets()
            self.shuffle_puzzle()
        except Exception as e:
            messagebox.showerror("error", f"we couldn`t load photo: {e}")
            self.root.destroy()

    def load_and_slice_image(self):
        img = Image.open(self.image_path)
        img = img.resize((450, 450))
        self.tile_w = 150  # 450 / 3
        self.tile_h = 150

        for i in range(self.size):
            for j in range(self.size):
                left = j * self.tile_w
                upper = i * self.tile_h
                right = (j + 1) * self.tile_w
                lower = (i + 1) * self.tile_h

                tile_img = img.crop((left, upper, right, lower))
                tile_photo = ImageTk.PhotoImage(tile_img)

                if i == self.size - 1 and j == self.size - 1:
                    self.tiles.append(None)
                else:
                    self.tiles.append(tile_photo)

        self.correct_order = list(self.tiles)

    def create_widgets(self):
        self.frame = tk.Frame(self.root, bg="black")
        self.frame.pack(pady=20, padx=20)

        for i in range(self.size * self.size):
            btn = tk.Button(self.frame, bd=1, relief="solid",
                            command=lambda idx=i: self.click_tile(idx))
            btn.grid(row=i // self.size, column=i % self.size)
            self.buttons.append(btn)

    def update_board(self):
        for i, tile in enumerate(self.tiles):
            if tile:
                self.buttons[i].config(image=tile, state="normal", width=150, height=150)
            else:
                self.buttons[i].config(image="", bg="#2c3e50", state="disabled", width=20, height=9)

    def click_tile(self, idx):
        empty_idx = self.tiles.index(None)
        r, c = divmod(idx, self.size)
        er, ec = divmod(empty_idx, self.size)

        if abs(r - er) + abs(c - ec) == 1:
            self.tiles[idx], self.tiles[empty_idx] = self.tiles[empty_idx], self.tiles[idx]
            self.update_board()
            if self.tiles == self.correct_order:
                messagebox.showinfo("Winnnnnnn", "Excellent , You Win")

    def shuffle_puzzle(self):
        random.shuffle(self.tiles)
        self.update_board()


if __name__ == "__main__":
    root = tk.Tk()
    game = SimpleImagePuzzle(root)
    root.mainloop()
