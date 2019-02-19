import sys
sys.path.append('./tools')
import tkinter as tk
import information as i
import network as nt
import graph as gr
from tkinter import ttk

class Application:
    def __init__(self, master):
        self.master = master
        self.general_info = ['hostname','community','version', 'port', 'protocol', 'status']
        self.createWidgets()

    def createWidgets(self):
        self.master.title("Network Administrator")
        self.createButtons()
        self.createTreeView()

    def createButtons(self):
        self.add_agent_btn = tk.Button(self.master, text='New Agent', command=self.addAgentPanel)
        self.delete_agent = tk.Button(self.master, text='Delete Agent', command=self.deleteAgentTreeview, state= "disabled")
        self.add_agent_btn.grid(row=1, column = 0)
        self.delete_agent.grid(row=1, column = 1)

    def createTreeView(self):
        self.treeview = ttk.Treeview(self.master)
        self.treeview['columns'] = self.general_info[1:]

        for i, elem in enumerate(self.general_info):
            self.treeview.heading("#" + str(i), text = elem, anchor='w')
            self.treeview.column("#" + str(i),  width = 170, anchor='w')

        self.treeview.bind('<Button-1>', self.enableDelete)
        self.treeview.bind("<Double-1>", lambda event: self.deviceInformationPanel(event))
        self.treeview.grid(row=0, column=0, columnspan=2)
        self.updateValuesIntoTreeView()

    def enableDelete(self, event):
        self.delete_agent['state'] = 'normal'

    def deviceInformationPanel(self, event):
        self.agent_information_window = tk.Toplevel(self.master)
        self.agent_information_window.title("Agent")
        self.agent_ntb = ttk.Notebook(self.agent_information_window)
        self.createTabsInformationPanel()
        self.fillInformationTab()
        self.fillGraphTab()
        self.agent_ntb.grid(row=0, column=0)

    def createTabsInformationPanel(self):
        self.information_frame = ttk.Frame(self.agent_ntb)
        self.agent_ntb.add(self.information_frame, text="Information")
        self.graphs_frame = ttk.Frame(self.agent_ntb)
        self.agent_ntb.add(self.graphs_frame, text="Graphs")
        self.agent_ntb.select(self.information_frame)
        self.agent_ntb.enable_traversal()

    def fillInformationTab(self):
        selected_item = self.treeview.selection()[0]
        ip = self.treeview.item(selected_item,"text")
        data = self.treeview.item(selected_item,"values")
        community, port = data[0], data[3]
        system = nt.getOS(community,ip,port)
        adress = nt.getLocation(community,ip,port)
        computer = nt.getName(community,ip,port)
        time = nt.getUpTime(community,ip,port)

        ttk.Label(self.information_frame,text="SO :" + system).grid(row=1)
        ttk.Label(self.information_frame,text="Adress :" + adress).grid(row=2)
        ttk.Label(self.information_frame,text="Computer :" + computer).grid(row=3)
        ttk.Label(self.information_frame,text="Time :" + time).grid(row=4)

    #TODO refacor this method
    def fillGraphTab(self):
        gr.hilotrafico(community,ip,port)
        photo = tk.PhotoImage(file ="./data/rd/tcp/trafico.png")
        lbTrafico = ttk.Label(self.graphs_frame,image=photo, text="Grafica1")
        lbTrafico.pack(pady=(10,10))
        lbTrafico.image = photo

    def updateValuesIntoTreeView(self):
        for old_value in self.treeview.get_children():
            self.treeview.delete(old_value)
        for info in i.get_agents():
            self.treeview.insert('', 'end', text=info[0], values=(info[1], info[2], info[3], info[4], 'up'))

    def addAgentPanel(self):
        entries = []
        self.new_agent_window = tk.Toplevel(self.master)
        self.new_agent_window.title("Agregar dispositivo")
        for i, elem in enumerate(self.general_info[:len(self.general_info) -2]):
            tk.Label(self.new_agent_window, text=elem).grid(row=i)
            entry = tk.Entry(self.new_agent_window, text='', width=40)
            entries.append(entry)
            entry.grid(row=i, column=1)
        tk.Button(self.new_agent_window, text="Add", width=10, command=lambda: self.getEntriesAgentPanel(entries)).grid(row=5, column=0)

    def getEntriesAgentPanel(self, entries):
        i.add_agent(" ".join(str(entry.get()) for entry in entries) + ' up')
        self.updateValuesIntoTreeView()
        self.new_agent_window.destroy()

    def deleteAgentTreeview(self):
        i.delete_agent(self.treeview.item(self.treeview.selection()[0], "text"))
        self.updateValuesIntoTreeView()


master = tk.Tk()
app = Application(master)
i.get_agents()
master.mainloop()