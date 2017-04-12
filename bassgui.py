import pint
import numpy as np
import pandas as pd
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, font
from tkinter.filedialog import askopenfilename
from encap import *

__all__ = ['Entry', 'StartPage', 'BassApp']
LARGE_FONT = ("Avenir Next", 12)
entries = {}  # global variable because I'm a pleb


class Entry:
    '''
    The object that is actually holding the data with the entries
    '''

    def __init__(self, boat_number=-1, school=None,
                 names=None, fishes=np.zeros(5)):
        self.boat_number = boat_number
        self.school = school
        self.names = names
        self.fishes = 0  # np.array(fishes) # Five 'weights'
        self.total_weight = 0  # sum(fishes)
        self.num_fish = 0  # np.count_nonzero(self.fishes)
        self.biggest_fish = 0  # max(self.fishes)

    def updateTotalWeight(self):
        self.total_weight = sum(self.fishes)

    def updateNumFish(self):
        self.num_fish = len(self.fishes)

    def updateFish(self, total_weight, num_fish, big_bass):
        ureg = pint.UnitRegistry()
        self.num_fish = num_fish
        self.total_weight = (int(total_weight[0]) * ureg.pound
                             + int(total_weight[1]) * ureg.ounce)

        if (big_bass[0] == ''):  # big_bass[0] Because split returned a list
            self.biggest_fish = np.nan
        else:
            self.biggest_fish = (int(big_bass[0]) * ureg.pound
                                 + int(big_bass[1]) * ureg.ounce)


class BassApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        '''
        *args and **kwargs wil be passed into Tk's init() function.
        '''
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, "b a s s")

        container = tk.Frame(self)
        container.pack(side='top', fill='both', expand=True)  # Use container.grid() for more control
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}  # multiple windows = multiple values in self.frames

        for F in (StartPage,):  # , PageEntries, PageScores, PageAddEntries, PageAddCatch): # We can just add pages here—we can also do this not in a for-loop if we need more control
            frame = F(container, self)
            self.frames[F] = frame
            # nsew stretches in all 4 directions to frame
            frame.grid(row=0, column=0, sticky='nsew')

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class StartPage(tk.Frame):
    '''
    Shows all the entries and buttons for manipulation
    '''

    def __init__(self, parent, controller):
        frame = tk.Frame.__init__(self, parent)
        # bg for tk background color, background for ttk
        label = tk.Label(self, text='Entries Page',
                         font=LARGE_FONT, bg='#39c4d3')
        label.grid(row=0)

        self.configure(background='#39c4d3')
        # default_font = font.nametofont("TkDefaultFont")
        # default_font.configure(size=48)

        avenir12 = font.Font(family='Avenir Next', size=12, weight='bold')
        s = ttk.Style()  # Needed to stylize ttk buttons.
        s.configure('my.TButton', font=('Avenir Next', 12))

        self.tree = ttk.Treeview(self, show='headings')
        self.tree.grid(row=1, column=0)

        col_names = ["Boat Number", 'School', "Anglers",
                     "Number of Fish", "Total Weight", "Big Bass"]

        self.tree["columns"] = (col_names)

        for col in col_names:
            self.tree.column(col, width=200)
            self.tree.heading(
                col, text=col,
                command=lambda _col=col: self.treeviewSortColumn(_col, True))

        for i, (boat_number, entry) in enumerate(entries.items()):
            self.tree.insert("", i, iid=(i + 1),
                             text=str(boat_number),
                             values=self.getValue(entry))

        # Groups by school but that might not be the best interface
        # for i, (school, entry_list) in enumerate(entries_by_school.items()):
        #     temp_id = self.tree.insert("", i, school, text=school) #Top level
        #
        #     for entry in entry_list:
        #         self.tree.insert(temp_id, 'end', '',
        #                          text='',
        #                          values=self.getValues(entry))

        self.addEntryInterface()
        self.addCatchInterface()
        self.deleteEntryInterface()
        self.openFileInterface()

    def addEntryInterface(self):
        # for ttk, use style parameter instead of font
        self.instruction = tk.Label(self, text='Enter Boat Number',
                                    font=LARGE_FONT, bg='#39c4d3')
        # Forcing it to be s because of weird formatting otherwise
        self.instruction.grid(row=3, column=1, sticky='sw')
        self.entry_boat_number = ttk.Entry(self)
        self.entry_boat_number.grid(row=4, column=1, sticky='w')

        self.instruction = tk.Label(self, text='Enter School',
                                    font=LARGE_FONT, bg='#39c4d3')
        self.instruction.grid(row=5, column=1, sticky='w')
        self.entry_school = ttk.Entry(self)
        self.entry_school.grid(row=6, column=1, sticky='w')

        self.instruction = tk.Label(self, text='Enter Angler 1',
                                    font=LARGE_FONT, bg='#39c4d3')
        self.instruction.grid(row=7, column=1, sticky='w')
        self.entry_fisher1 = ttk.Entry(self)
        self.entry_fisher1.grid(row=8, column=1, sticky='w')

        self.instruction = tk.Label(self, text='Enter Angler 2',
                                    font=LARGE_FONT, bg='#39c4d3')
        self.instruction.grid(row=9, column=1, sticky='w')
        self.entry_fisher2 = ttk.Entry(self)
        self.entry_fisher2.grid(row=10, column=1, sticky='w')
        # you need to catch the keyboard event as a parameter, see below
        self.entry_fisher2.bind('<Return>', self.addEntry)

        self.add_entry_button = ttk.Button(self, text='Add Entry',
                                           command=self.addEntry,
                                           style='my.TButton')
        self.add_entry_button.grid(row=11, column=1, sticky='w')

    def addCatchInterface(self):
        self.instruction = tk.Label(self, text='Boat Number',
                                    font=LARGE_FONT, bg='#39c4d3')
        self.instruction.grid(row=3, column=0, sticky='w')
        self.catch_boat_number = ttk.Entry(self)
        self.catch_boat_number.grid(row=4, column=0, sticky='w')

        self.instruction = tk.Label(self,
                                    text='Enter total fish weight in the form (lb, oz). Example: (1, 9) is 1lb 9oz',
                                    font=LARGE_FONT, bg='#39c4d3')
        self.instruction.grid(row=5, column=0, sticky='w')
        self.catch_fish_weight = ttk.Entry(self)
        self.catch_fish_weight.grid(row=6, column=0, sticky='w')

        self.instruction = tk.Label(self, text='Enter number of fish caught',
                                    font=LARGE_FONT, bg='#39c4d3')
        self.instruction.grid(row=7, column=0, sticky='w')
        self.catch_num_fish = ttk.Entry(self)
        self.catch_num_fish.grid(row=8, column=0, sticky='w')

        self.instruction = tk.Label(self, text='Enter big bass (if applicable)',
                                    font=LARGE_FONT, bg='#39c4d3')
        self.instruction.grid(row=9, column=0, sticky='w')
        self.catch_big_bass = ttk.Entry(self)
        self.catch_big_bass.grid(row=10, column=0, sticky='w')
        self.catch_big_bass.bind('<Return>', self.addCatch)

        self.add_catch_button = ttk.Button(self, text='Add Catches',
                                           command=self.addCatch,
                                           style='my.TButton')
        self.add_catch_button.grid(row=11, column=0, sticky='w')

    def deleteEntryInterface(self):
        self.instruction = tk.Label(self, text='Boat Number to Delete',
                                    font=LARGE_FONT, bg='#39c4d3')
        self.instruction.grid(row=12, column=0, pady=20, sticky='w')
        self.delete_entry = ttk.Entry(self)
        self.delete_entry.grid(row=13, column=0, sticky='w')
        self.delete_entry_button = ttk.Button(self, text='Delete Entry',
                                              command=self.deleteEntry,
                                              style='my.TButton')
        self.delete_entry_button.grid(row=14, column=0, sticky='w')
        self.delete_entry.bind('<Return>', self.deleteEntry)

    def openFileInterface(self):
        self.open_file_button = ttk.Button(self, text='Open File',
                                           command=self.addEntryFromExcel,
                                           style='my.TButton')
        self.open_file_button.grid(row=15, column=0, pady=20, sticky='sw')

    def editEntry(self, event=None):
        boat_number = int(self.edit_entry.get())
        entry = entries[boat_number]
        toplevel = tk.Toplevel()

        toplevel.boat_number = ttk.Entry(toplevel)
        toplevel.boat_number.insert('end', entry.boat_number)
        toplevel.boat_number.grid(row=1, column=0)

        toplevel.school = ttk.Entry(toplevel)
        toplevel.school.insert('end', entry.school)
        toplevel.school.grid(row=2, column=0)

        toplevel.fisher1 = ttk.Entry(toplevel)
        toplevel.fisher1.insert('end', entry.names[0])
        toplevel.fisher1.grid(row=3, column=0)

        toplevel.fisher2 = ttk.Entry(toplevel)
        toplevel.fisher2.insert('end', entry.names[1])
        toplevel.fisher2.grid(row=4, column=0)

        toplevel.num_fish = ttk.Entry(toplevel)
        toplevel.num_fish.insert('end', entry.num_fish)
        toplevel.num_fish.grid(row=5, column=0)

        toplevel.total_weight = ttk.Entry(toplevel)
        toplevel.total_weight.insert('end', entry.total_weight)
        toplevel.total_weight.grid(row=6, column=0)

        toplevel.biggest_fish = ttk.Entry(toplevel)
        toplevel.biggest_fish.insert('end', entry.biggest_fish)
        toplevel.biggest_fish.grid(row=7, column=0)

        toplevel.update_button = ttk.Button(
            toplevel, text='Update', command=self.updateEntry(toplevel, entry))
        toplevel.update_button.grid(row=8, column=0)

        self.tree.delete(entry.boat_number)
        self.tree.insert('', entry.boat_number, iid=entry.boat_number,
                         text=str(entry.boat_number),
                         values=(self.getValues(entry)))

    def updateEntry(self, toplevel, entry, event=None):
        entry.boat_number = int(toplevel.boat_number.get())
        entry.school = toplevel.school.get()
        entry.fisher1 = toplevel.fisher1.get()
        entry.fisher2 = toplevel.fisher2.get()
        entry.num_fish = toplevel.num_fish.get()
        entry.total_weight = toplevel.total_weight.get()
        entry.biggest_fish = toplevel.biggest_fish.get()

    def addEntry(self, event=None):
        '''
        Adds an entry.

        Note: self.e.bind('<Key>', self.meth) calls self.meth(event), meaning
        that it will pass both itself AND the event.

        Therefore, event=None catches that.
        '''
        boat_number = int(self.entry_boat_number.get())

        # Display error message if key already exists
        # TODO: Handle this more elegantly
        if boat_number in entries.keys():
            messagebox.showerror(
                "ERROR",
                "Boat number already exists. \n\nPlease enter a different boat number or delete the old boat number."
            )
            return

        school = self.entry_school.get()
        fisher1 = self.entry_fisher1.get()
        fisher2 = self.entry_fisher2.get()

        entry = Entry(boat_number=boat_number, school=school, names=[fisher1, fisher2])
        entries[boat_number] = entry
        self.entry_boat_number.delete(0, 'end')  # clears entrybox after submit
        self.entry_school.delete(0, 'end')
        self.entry_fisher1.delete(0, 'end')
        self.entry_fisher2.delete(0, 'end')

        # Update the table
        self.tree.insert("", entry.boat_number, iid=entry.boat_number,
                         text=str(entry.boat_number),
                         values=self.getValues(entry))

    def addEntryFromExcel(self, event=None):
        filename = askopenfilename()
        data = pd.read_excel(filename)
        boat_numbers = data['Boat No.']
        schools = data['School Name']
        names = data['Angler Names']

        for boat_number, school, team in zip(boat_numbers, schools, names):
            entry = Entry(boat_number=int(boat_number), school=school, names=team.split(', '))
            entries[boat_number] = entry
            self.tree.insert('', entry.boat_number, iid=entry.boat_number,
                             text=str(entry.boat_number),
                             values=self.getValues(entry))

    def treeviewSortColumn(self, col, reverse):
        l = [(self.tree.set(k, col), k) for k in self.tree.get_children('')]
        try:
            # we need to convert the treeview object into an int
            l.sort(key=lambda t: int(t[0]), reverse=not reverse)
        except ValueError:
            # This will sort the strings. Oddly, nothing at all happens for
            # string columns w/o this block—no error is shown. Maybe ttk
            # internally ignores it.
            l.sort(reverse=reverse)

        for index, (val, k) in enumerate(l):
            self.tree.move(k, '', index)

        self.tree.heading(col, command=lambda: self.treeviewSortColumn(col, not reverse))

    def addCatch(self, event=None):
        try:
            boat_number = int(self.catch_boat_number.get())
        except ValueError:
            self.displayBoatDoesNotExistError()
            return

        try:
            total_weight = self.catch_fish_weight.get().split(', ')
            big_bass = self.catch_big_bass.get().split(', ')
        except ValueError:
            self.displayInvalidIntEntry()
            return

        try:
            entry = entries[boat_number]
        except KeyError:
            self.displayBoatDoesNotExistError()
            return

        try:
            num_fish = int(self.catch_num_fish.get())
        except ValueError:
            self.displayInvalidIntEntry()
            return

        entry.updateFish(total_weight, num_fish, big_bass)

        # delete entry from textbox
        self.catch_boat_number.delete(0, 'end')
        self.catch_fish_weight.delete(0, 'end')
        self.catch_num_fish.delete(0, 'end')
        self.catch_big_bass.delete(0, 'end')

        self.tree.delete(entry.boat_number)
        self.tree.insert('', entry.boat_number, iid=entry.boat_number,
                         text=str(entry.boat_number),
                         values=self.getValues(entry))

    def deleteEntry(self, event=None):
        boat_number = int(self.delete_entry.get())

        try:
            entry = entries[boat_number]
        except KeyError:
            self.displayBoatDoesNotExistError()
            return

        self.delete_entry.delete(0, 'end')
        self.tree.delete(entry.boat_number)
        entries.pop(boat_number)
        del entry

    def getValues(self, entry):
        return (entry.boat_number, entry.school, entry.names, entry.num_fish,
                entry.total_weight, entry.biggest_fish)

    def displayBoatDoesNotExistError(self):
        '''
        Shows messagebox saying boat does not exist.
        '''
        messagebox.showerror(
            "ERROR",
            "Boat number does not exist. \n\nPlease enter a valid boat number"
        )

    def displayInvalidIntEntry(self):
        messagebox.showerror(
            'ERROR',
            'Please enter an integer value'
        )


if __name__ == '__main__':
    app = BassApp()
    app.mainloop()
