
import tkinter as tk
import tkinter.filedialog as filedialog
import tkinter.ttk as ttk

import dnd.io as _io

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import Union
    Container = Union[tk.Frame, tk.Tk]


class ItemEditWindow(tk.Tk):
    def __init__(self) -> None:
        tk.Tk.__init__(self)

        self.minsize(640,480)

        menubar = tk.Menu(self)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Open", command=self._load_file)
        file_menu.add_command(label="Save", command=self._save_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)
        menubar.add_cascade(label="File", menu=file_menu)

        lbl_tree = tk.Label(self, text="Category Selection", anchor='w', justify='left')
        lbl_list = tk.Label(self, text="Item Selection", anchor='w', justify='left')
        lbl_edit = tk.Label(self, text="Item Edit", anchor='w', justify='left')
        self._tree_categories = ttk.Treeview(self)
        self._lst_items = tk.Listbox(self)
        self._frm_edit = ItemEditFrame(self, relief='sunken')

        lbl_tree.grid(row=0, column=0, sticky='we')
        lbl_list.grid(row=0, column=1, sticky='we')
        lbl_edit.grid(row=0, column=2, sticky='we')
        self._tree_categories.grid(row=1, column=0, sticky='nsew')
        self._lst_items.grid(row=1, column=1, sticky='nsew')
        self._frm_edit.grid(row=1, column=2, sticky='nsew')

        self.config(menu=menubar)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=6, pad=4)
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)

        self._item_collection = None

    def _load_file(self) -> None:
        filename = filedialog.askopenfilename()
        if filename is not None and filename != "":
            fd = _io.FileData()
            fd.load_filename(filename)
            self._item_collection = fd._items

    def _save_file(self) -> None:
        print("Save File")


class ItemEditFrame(tk.Frame):
    def __init__(self, root: 'Container', **kwargs) -> None:
        tk.Frame.__init__(self, root, kwargs)


class MainFrame(tk.Frame):
    def __init__(self, root: 'Container', **kwargs) -> None:
        tk.Frame.__init__(self, root, kwargs)


class ReplTextArea(tk.Text):
    def __init__(self, root: 'Container', **kwargs) -> None:
        width = kwargs.pop("width", None)
        height = kwargs.pop("height", 1)
        tk.Text.__init__(self, root, kwargs)
        if width is not None:
            self.configure(width=width)
        self.configure(height=height)


class ActorFrame(tk.Frame):
    def __init__(self, root: 'Container', **kwargs) -> None:
        tk.Frame.__init__(self, root, kwargs)

        self._var_initiative = tk.Label(self, width=4, text="23", anchor='e', justify='right')
        self._var_name = tk.Label(self, text="Lyra Al'Thor", anchor='w', justify='left')
        self._lbl_hp = tk.Label(self, text="hp:", anchor='e', justify='right')
        self._var_hp = tk.Label(self, text="800/999", fg='green', anchor='e', justify='left')
        self._lbl_mp = tk.Label(self, text="mp:", anchor='e', justify='right')
        self._var_mp = tk.Label(self, text="100/200", fg='yellow', anchor='e', justify='left')

        self._var_initiative.grid(row=0, column=0)
        self._var_name.grid(row=0, column=1, columnspan=4, sticky='ew')
        self._lbl_hp.grid(row=1, column=1)
        self._var_hp.grid(row=1, column=2)
        self._lbl_mp.grid(row=1, column=3)
        self._var_mp.grid(row=1, column=4)


class GroupFrame(tk.Frame):
    def __init__(self, root: 'Container', **kwargs) -> None:
        tk.Frame.__init__(self, root, kwargs)

        self._lbl_title = tk.Label(self, "Actors:", font=("Times", 14, "bold"))
        self._frm_actors = tk.Frame(self, borderwidth=1, padx=2, pady=4, relief='groove')
