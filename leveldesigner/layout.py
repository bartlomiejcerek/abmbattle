import logging
import tkinter as tk
from tkinter import messagebox
from tkinter.filedialog import askopenfilename, asksaveasfilename

import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from settings import Settings

settings = Settings()

colors = ['ro', 'bo', 'co', 'go', 'mo', 'yo']


def convert_to_data(field, units):
    obstacles = {'x': [], 'y': []}
    unit_cords = {}
    for i in range(len(field)):
        for j in range(len(field[i])):
            if field[i, j] < 0:
                obstacles['x'].append(i + 0.5)
                obstacles['y'].append(j + 0.5)
            if field[i, j] > 0:
                team = units[field[i, j]]['team']
                if team not in unit_cords.keys():
                    unit_cords[team] = {'x': [], 'y': []}
                unit_cords[team]['x'].append(i + 0.5)
                unit_cords[team]['y'].append(j + 0.5)
    return obstacles, unit_cords


class Page(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

    @staticmethod
    def error(mes):
        messagebox.showinfo("Error", mes)

    @staticmethod
    def info(mes):
        messagebox.showinfo("Result", mes)


class OpenCreateDialog(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        self.filename_var = tk.StringVar(self)
        open_file_panel = tk.LabelFrame(self, text='Load settings file:', padx=30, pady=20)
        open_file_panel.pack(side="top", fill="x", expand=False)
        open_file = tk.Entry(open_file_panel, textvariable=self.filename_var, width=50) \
            .pack(expand=1, fill=tk.X, side='left')
        open_file_button = tk.Button(open_file_panel, text="...", command=self.chose_file, width=2) \
            .pack(fill=tk.X, side='right')
        create_panel = tk.LabelFrame(self, text='OR create new:', padx=30, pady=20)
        create_panel.pack(side="top", fill="x", expand=False)
        tk.Label(create_panel, text="Heigh").grid(row=0)
        tk.Label(create_panel, text="Wight").grid(row=1)

        self.heigh_var = tk.StringVar(self)
        self.weight_var = tk.StringVar(self)
        heigh = tk.Entry(create_panel, textvariable=self.heigh_var).grid(row=0, column=1)
        weight = tk.Entry(create_panel, textvariable=self.weight_var).grid(row=1, column=1)
        b1 = tk.Button(create_panel, text="Create", command=self.create_field).grid(row=1, column=2)

    def create_field(self):
        try:
            h = int(self.heigh_var.get())
            w = int(self.weight_var.get())
            if h < 0 or w < 0:
                raise ValueError("Shape value should be positive")
            if h and w:
                settings.create_board(h, w)
                self.info("Board created")
        except Exception as e:
            logging.error(e)
            self.error("Error during creating board: " + str(e) + "\n See logs for detailed information")

    def chose_file(self):
        self.filename_var.set(askopenfilename(initialdir="/", title="Select file",
                                              filetypes=(("battle giles", "*.json"), ("all files", "*.*"))))
        try:
            file_name = self.filename_var.get()
            if file_name and file_name != "":
                settings.load_file(file_name)
            self.info("Settings loaded")

        except Exception as e:
            logging.error(e)
            self.error("Error during file loading: " + str(e) + "\n See logs for detailed information")

    def show(self):
        self.lift()


class TeamsDialog(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        self.team_var = tk.StringVar(self)
        teams_label = tk.Label(self, text="Teams:").grid(row=0)
        self.teams = tk.Listbox(self, selectmode='extended', height=20, width=30)
        self.teams.grid(row=1, padx=(70, 10), pady=(10, 30))
        delete_element = tk.Button(self, text="Delete", command=self.delete).grid(row=1, column=1)
        self.one_team = tk.Entry(self, textvariable=self.team_var).grid(row=2, column=0)
        add_element = tk.Button(self, text="Add", command=self.add).grid(row=2, column=1)

    def add(self):
        team_name = self.team_var.get()
        if team_name and team_name != "":
            try:
                settings.add_team(team_name)
                self.teams.insert(tk.END, team_name)
                self.team_var.set("")
            except Exception as e:
                logging.error(e)
                self.error("Error during adding team: " + str(e) + "\n See logs for detailed information")

    def delete(self):
        try:
            for el in self.teams.curselection():
                settings.delete_team(el)
                self.teams.delete(el)
        except Exception as e:
            logging.error(e)
            self.error("Error during deleting team: " + str(e) + "\n See logs for detailed information")

    def show(self):
        self.teams.delete(0, last=self.teams.size())
        for team in settings.get_teams():
            self.teams.insert(tk.END, team)
        self.lift()


class SetCoordinates(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        field = tk.LabelFrame(self, text='Field:')
        field.pack(fill="both", side="left", expand=True)
        self.fig = Figure(figsize=(7, 7), dpi=100, tight_layout=True)
        self.ax = self.fig.add_subplot(111)
        self.ax.plot([], [])

        self.canvas = FigureCanvasTkAgg(self.fig, master=field)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH)
        self.canvas.mpl_connect('button_press_event', self.on_press)
        self.canvas.mpl_connect('button_release_event', self.on_release)
        self.canvas.mpl_connect('motion_notify_event', self.on_move)

        parameters = tk.LabelFrame(self, text='Parameters:')
        parameters.pack(fill="y", side="right", expand=False)
        self.clear = tk.IntVar(self)
        self.obstacle = tk.IntVar(self)
        self.obstacle.set(1)
        self.unit = tk.IntVar(self)
        self.team = tk.StringVar(self)
        self.hp = tk.StringVar(self)
        self.attack = tk.StringVar(self)
        self.ran = tk.StringVar(self)
        self.strategy = tk.StringVar(self)
        self.strategy_list = ["KillTheClosest", "RandomStrategy"]
        self.team_list = ()
        tk.Checkbutton(parameters, text="empty", variable=self.clear,
                       onvalue=1, offvalue=0, command=self.set_empty).grid(row=0, sticky=tk.W)
        tk.Checkbutton(parameters, text="obstacle", variable=self.obstacle,
                       onvalue=1, offvalue=0, command=self.set_obstacle).grid(row=1, sticky=tk.W)
        tk.Checkbutton(parameters, text="unit", variable=self.unit,
                       onvalue=1, offvalue=0, command=self.set_unit).grid(row=2, sticky=tk.W)

        tk.Label(parameters, text="Team").grid(row=3, sticky=tk.W)
        self.teams = tk.OptionMenu(parameters, value="", variable=self.team, *self.team_list)
        self.teams.grid(row=4, sticky=tk.W)
        self.teams.config(width=30)
        tk.Label(parameters, text="HP").grid(row=5, sticky=tk.W)
        self.hp_el = tk.Entry(parameters, textvariable=self.hp)
        self.hp_el.grid(row=6)
        tk.Label(parameters, text="Attack").grid(row=7, sticky=tk.W)
        self.atack_el = tk.Entry(parameters, textvariable=self.attack)
        self.atack_el.grid(row=8)
        tk.Label(parameters, text="Range").grid(row=9, sticky=tk.W)
        self.strategy_element = tk.OptionMenu(parameters, self.ran, *(1,2))
        self.strategy_element.grid(row=10, sticky=tk.W)
        self.strategy_element.config(width=30)
        tk.Label(parameters, text="Strategy").grid(row=11, sticky=tk.W)
        self.strategy_element = tk.OptionMenu(parameters, self.strategy, *self.strategy_list)
        self.strategy_element.grid(row=12, sticky=tk.W)
        self.strategy_element.config(width=30)

        self.teams_map = {}

    def on_press(self, event):
        pass
        # MPL MouseEvent: xy=(434,314) xydata=(3.9454114766315347,7.76) button=1 dblclick=False inaxes=AxesSubplot(0.125,0.11;0.775x0.77)

    def on_release(self, event):
        if self.obstacle.get():
            settings.create_obstacle(int(event.xdata), int(event.ydata))
        if self.clear.get():
            settings.clear_position(int(event.xdata), int(event.ydata))
        if self.unit.get():
            try:
                if self.team.get() is None or self.team.get() == "":
                    raise ValueError("Pick team")
                    
                try: #Nested try to make sure casting happend
                    hp = int(self.hp.get())
                    attack = int(self.attack.get())
                except:
                    raise ValueError("Set HP and Attack")
             
                if hp <= 0 or attack <= 0:
                    raise ValueError("Hp and attack should be positive")
                
                if self.ran.get() is None or self.ran.get() == "":
                    raise ValueError("Choose range")

                if self.strategy.get() is None or self.strategy.get() == "":
                    raise ValueError("Choose strategy")
                
                settings.create_unit(int(event.xdata), int(event.ydata), self.team.get(), hp,
                                     attack, int(self.ran.get()), self.strategy.get())
            except Exception as e:
                logging.error(e)
                self.error("Error during placing unit: " + str(e) + "\n See logs for detailed information")

        self.refresh_board()

    def on_move(self, event):
        pass

    def set_empty(self):
        if self.clear.get() == 1:
            self.obstacle.set(0)
            self.unit.set(0)
            self.enable_disable()

    def set_obstacle(self):
        if self.obstacle.get() == 1:
            self.clear.set(0)
            self.unit.set(0)
            self.enable_disable()

    def set_unit(self):
        if self.unit.get() == 1:
            self.clear.set(0)
            self.obstacle.set(0)
            self.enable_disable()

    def enable_disable(self):
        if self.unit.get() == 1:
            self.hp_el.config(state='normal')
            self.teams.config(state='normal')
            self.atack_el.config(state='normal')
            self.strategy_element.config(state='normal')
        else:
            self.hp_el.config(state='disabled')
            self.teams.config(state='disabled')
            self.atack_el.config(state='disabled')
            self.strategy_element.config(state='disabled')

    def refresh_board(self):
        self.ax.cla()
        self.ax.set_yticklabels([])
        self.ax.set_xticklabels([])
        x, y = settings.get_field_shape()
        self.ax.set_xlim(0, x)
        self.ax.set_ylim(0, y)
        self.ax.set_xticks(np.array(range(1, x)))
        self.ax.set_yticks(np.array(range(1, y)))
        self.ax.grid(True, which='both', axis='both')

        if x > 0 and y > 0:
            obstacles, units = convert_to_data(settings.field, settings.units)
            self.ax.plot(obstacles['x'], obstacles['y'], 'ks', markersize=5)
            for i, team in enumerate(units.keys()):
                self.ax.plot(units[team]['x'], units[team]['y'], colors[i], markersize=5)
        self.canvas.draw()

    def show(self):
        self.refresh_board()

        self.enable_disable()
        self.teams['menu'].delete(0, 'end')
        self.teams_map = {}
        for i, team in enumerate(settings.get_teams()):
            self.teams['menu'].add_command(label=team, command=tk._setit(self.team, team))
            self.teams_map[team] = i

        self.lift()


class SaveToFile(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        self.filename_var = tk.StringVar(self)
        open_file_panel = tk.LabelFrame(self, text='Save settings file:', padx=30, pady=20)
        open_file_panel.pack(side="top", fill="x", expand=False)
        open_file = tk.Entry(open_file_panel, textvariable=self.filename_var, width=50) \
            .pack(expand=1, fill=tk.X, side='left')
        open_file_button = tk.Button(open_file_panel, text="...", command=self.chose_file, width=2) \
            .pack(fill=tk.X, side='right')

    def chose_file(self):
        self.filename_var.set(asksaveasfilename(initialdir="/", title="Select file",
                                                filetypes=(("battle files", "*.json"), ("all files", "*.*"))))
        try:
            file_name = self.filename_var.get()
            if file_name and file_name != "":
                settings.save_to_file(file_name)
            self.info("Settings saved")

        except Exception as e:
            logging.error(e)
            self.error("Error during saving to file : " + str(e) + "\n See logs for detailed information")

    def show(self):
        self.lift()


class MainView(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        tk.Frame.__init__(self, *args, **kwargs)
        p1 = OpenCreateDialog(self)
        p2 = TeamsDialog(self)
        p3 = SetCoordinates(self)
        p4 = SaveToFile(self)

        buttonframe = tk.Frame(self)
        container = tk.Frame(self)
        buttonframe.pack(side="top", fill="x", expand=False)
        container.pack(side="top", fill="both", expand=True)

        p1.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p2.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p3.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p4.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

        b1 = tk.Button(buttonframe, text="Open/Create field", command=p1.show)
        b2 = tk.Button(buttonframe, text="Teams", command=p2.show)
        b3 = tk.Button(buttonframe, text="Field visualization", command=p3.show)
        b4 = tk.Button(buttonframe, text="Save", command=p4.show)

        b1.pack(side="left")
        b2.pack(side="left")
        b3.pack(side="left")
        b4.pack(side="left")

        p1.show()
