import tkinter as tk

# window = tk.Tk()
# window.title("Temperature Converter")
# window.resizable(width=False, height=False)

# frame_a = tk.Frame()
# label_a = tk.Label(master=frame_a, text="I'm in Frame A")
# label_a.pack()

# frame_b = tk.Frame(master=window, width=200, height=100, bg="red")
# label_b = tk.Label(master=frame_b, text="I'm in Frame B")
# label_b.pack()

# # Swap the order of `frame_a` and `frame_b`
# frame_b.pack(fill=tk.X)
# frame_a.pack()

# tk.Label(text="Hello, Tkinter").pack()


# def handle_click(event):
#     print("The button was clicked!")


# button = tk.Button(text="Click me!")

# button.bind("<Button-1>", handle_click)
# button.pack()


# # def increase():
# #     value = int(lbl_value["text"])
# #     lbl_value["text"] = f"{value + 1}"


# # def decrease():
# #     value = int(lbl_value["text"])
# #     lbl_value["text"] = f"{value - 1}"


# # btn_decrease = tk.Button(master=window, text="-", command=decrease)
# # btn_decrease.grid(row=0, column=0, sticky="nsew")

# # lbl_value = tk.Label(master=window, text="0")
# # lbl_value.grid(row=0, column=1)

# # btn_increase = tk.Button(master=window, text="+", command=increase)
# # btn_increase.grid(row=0, column=2, sticky="nsew")

# window.mainloop()

# # .pack()
# # .place()
# # label2.place(x=75, y=75)
# # .grid()


class Gui:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Temperature Converter")
        self.window.resizable(width=False, height=False)
        self.cbk = handle_click

    def start(self):
        self.window.mainloop()

    def add_lbl(self, txt):
        lbl = tk.Label(master=self.window, text=txt)
        lbl.pack()

    def add_btn(self, txt, cbk):
        btn = tk.Button(text=txt)
        btn.bind(func=self.cbk)
        btn.pack()


def handle_click(event):
    # print(event)
    print("The button was clicked!")


gui = Gui()
gui.add_lbl("raz")
gui.add_lbl("dwa")

gui.add_btn("raz", handle_click)
gui.add_btn("dwa", handle_click)
gui.start()
