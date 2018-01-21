
import tkinter as tk

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import Union
    Container = Union[tk.Frame, tk.Tk]


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
