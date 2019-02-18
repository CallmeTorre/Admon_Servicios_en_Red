import tkinter as tk
from tkinter import ttk

class Application:
    def __init__(self, master):
        self.master = master
        self.general_info = ['hostname','community','version', 'port', 'protocol', 'status']
        self.createWidgets()

    def createWidgets(self):
        self.master.title("Network Administrator")
        #self.createNotebook()
        self.createTreeView()
        self.createButtons()

    def createNotebook(self):
        self.agent_ntb = ttk.Notebook(self.master)
        self.agent_ntb.pack(fill="both", expand='yes')

    def createTreeView(self):
        self.treeview = ttk.Treeview(self.master)
        self.treeview['columns'] = self.general_info[1:]

        for i, elem in enumerate(self.general_info):
            self.treeview.heading("#" + str(i), text = elem, anchor='w')
            self.treeview.column("#" + str(i),  width = 100, anchor='w')

        self.treeview.grid(row=0, column=0, columnspan=2)

    def createButtons(self):
        self.add_agent_btn = tk.Button(self.master, text='New Agent', command=self.add_agent_panel)
        self.delete_agent = tk.Button(self.master, text='Delete Agent', command=None, state= "disabled")
        self.add_agent_btn.grid(row=1, column = 0)
        self.delete_agent.grid(row=1, column = 1)

    def add_agent_panel(self):
        ents = {}
        new_agent_window = tk.Toplevel(self.master)
        new_agent_window.title("Agregar dispositivo")
        for i, elem in enumerate(self.general_info[:len(self.general_info) -2]):
            tk.Label(new_agent_window, text=elem).grid(row=i)
            entry = tk.Entry(new_agent_window, text='', width=40).grid(row=i, column=1)
        tk.Button(new_agent_window, text="Add", width=10, command=lambda: self.add_agent()).grid(row=5, column=0)

    def add_agent(self):
        print("Hi there")

master = tk.Tk()
app = Application(master)
master.mainloop()