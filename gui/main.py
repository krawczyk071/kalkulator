from typing import Literal
import os
from PIL import ImageTk
import PIL.Image
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter.filedialog import askopenfilename, askopenfilenames, askdirectory


class Gui(tk.Tk):
    def __init__(self, title, width=300, height=200):
        super().__init__()
        self.title(title)
        # self.resizable(width=False, height=False)
        x = self.winfo_screenwidth() // 2
        y = int(self.winfo_screenheight() // 2)
        self.geometry(
            f"{width}x{height}+" + str(x - (width // 2)) + "+" + str(y - (height // 2))
        )


class Frame(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, width=100, height=100)
        self.pack()

    def clear_widgets(self):
        # select all frame widgets and delete them
        for widget in self.winfo_children():
            widget.destroy()


class Label(ttk.Label):
    def __init__(self, master, txt):
        super().__init__(master, text=txt)
        self.pack()


class TextOutput(tk.Text):
    def __init__(self, master, txt, height=5, width=20):
        super().__init__(master, height=height, width=width, padx=15, pady=15)
        self.insert("1.0", txt)
        self.pack()


class Image(ttk.Label):
    def __init__(self, master, img_path, width=None, height=None, ratio=None):
        img = self._prepare_img(img_path, width, height, ratio)
        super().__init__(master, image=img)
        self.image = img
        self.pack()

    def _prepare_img(self, img_path, width, height, ratio):
        if bool(width) & bool(height):
            i = PIL.Image.open(img_path)
            i = i.resize((width, height))
            # i.thumbnail((width,height), Image.ANTIALIAS)
            return ImageTk.PhotoImage(i)
        if ratio:
            i = PIL.Image.open(img_path)
            width, height = i.size
            i = i.resize((int(width * ratio), int(height * ratio)))
            return ImageTk.PhotoImage(i)
        return ImageTk.PhotoImage(file=img_path)


class Button(ttk.Button):
    def __init__(self, master, txt, cbk):
        super().__init__(master, text=txt, command=cbk)
        self.pack()


class Input(ttk.Entry):
    def __init__(self, master):
        txt_var = tk.StringVar()
        super().__init__(master, textvariable=txt_var)

        self.pack(pady=20)


class FileDialog(ttk.Button):
    def __init__(
        self,
        master,
        txt,
        mode: Literal["folder", "file", "files"],
        title=None,
        dir_init=None,
        filetypes=None,
    ):
        self.dir_path = os.path.dirname(os.path.realpath(__file__))
        self.path = None
        self.mode = mode
        self.title = title
        self.dir_init = dir_init if dir_init else self.dir_path
        self.filetypes = (
            filetypes if filetypes else [("text files", "*.txt"), ("All files", "*.*")]
        )
        super().__init__(master, text=txt, command=lambda: self._save_path())
        self.pack()
        # self.bind("<Button-1>", lambda event: self._save_path())

    def get(self):
        return self.path

    def _save_path(self):
        self.path = self._select_func()
        print(self.path)

    def _select_func(self):
        match self.mode:
            case "folder":
                return askdirectory(
                    initialdir=self.dir_init,
                    title=self.title if self.title else "Select directory",
                )
            case "file":
                return askopenfilename(
                    initialdir=self.dir_init,
                    title=self.title if self.title else "Select file",
                    filetypes=self.filetypes,
                )
            case "files":
                return askopenfilenames(
                    initialdir=self.dir_init,
                    title=self.title if self.title else "Select files",
                    filetypes=self.filetypes,
                )
            # filedialog.asksaveasfilename()
            # filedialog.asksaveasfile()
            # filedialog.askopenfile()
            # filedialog.askopenfiles()


class MessageBox:
    def __init__(self):
        self.response = None

    def get(self):
        return self.response

    @staticmethod
    def showinfo(title=None, message=None, **options):
        "Show an info message"
        return messagebox.showinfo(title, message, **options)

    @staticmethod
    def showwarning(title=None, message=None, **options):
        "Show a warning message"
        return messagebox.showwarning(title, message, **options)

    @staticmethod
    def showerror(title=None, message=None, **options):
        "Show an error message"
        return messagebox.showerror(title, message, **options)

    def askquestion(self, title=None, message=None, **options):
        "Ask a question"
        # return messagebox.askquestion(title, message, **options)
        s = messagebox.askquestion(title, message, **options)
        self.response = s

    def askokcancel(self, title=None, message=None, **options):
        "Ask if operation should proceed; return true if the answer is ok"
        s = messagebox.askokcancel(title, message, **options)
        self.response = s

    def askyesno(self, title=None, message=None, **options):
        "Ask a question; return true if the answer is yes"
        s = messagebox.askyesno(title, message, **options)
        self.response = s

    def askyesnocancel(self, title=None, message=None, **options):
        "Ask a question; return true if the answer is yes, None if cancelled."
        s = messagebox.askyesnocancel(title, message, **options)
        # s might be a Tcl index object, so convert it to a string
        self.response = s

    def askretrycancel(self, title=None, message=None, **options):
        "Ask if operation should be retried; return true if the answer is yes"
        s = messagebox.askretrycancel(title, message, **options)
        self.response = s


#     def __init__(self, master, txt):
#         super().__init__(master, text=txt)
#         self.pack()


def testprint(x):
    print(x)


gui = Gui("tytul", 300, 400)
frm1 = Frame(gui)
lbl1 = Label(frm1, "test1")
btn1 = Button(frm1, "test1x", testprint)
btn2 = Button(frm1, "test1y", lambda: testprint("yy"))
# img1 = Image(frm1, "wykres1.png", width=100, height=100)
ipt1 = Input(frm1)
btn1 = Button(frm1, "print ipt", lambda: print(ipt1.get()))
txt1 = TextOutput(frm1, "test1")
fd1 = FileDialog(frm1, "open", "files")
btn2 = Button(frm1, "destroy", lambda: frm1.clear_widgets())
# messagebox.showinfo("showinfo", "Information")
msg1 = MessageBox()
msg1.askquestion("q1", "ask me")

btn3 = Button(frm1, "print ipt", lambda: print(msg1.get()))

gui.mainloop()
