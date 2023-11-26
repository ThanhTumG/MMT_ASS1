import customtkinter as ctk
import tkinter as tk
from server import *
import threading
from tkinter import ttk 
from tkinter import messagebox
from CTkListbox import *

SERVER_IP = get_local_ip()
SERVER_PORT = 4869

class AppServer():
    listName = list()
    index=0
    clientListName = []
    so_far  = 30
    def __init__(self):
        # super().__init__()
        self.app = ctk.CTk()
        self.server = Server(SERVER_IP, SERVER_PORT)
        self.UIobject()
        self.tree = self.create_tree_widget()
        self.button = self.create_button()
       
        self.ButtonFrame = self.createButtonField()


    
    
    def setup(self):
        ctk.set_appearance_mode('dark')
        ctk.set_default_color_theme('blue')
        self.app.title("ServerUI")
        self.app.geometry("900x500")
        # self.runServer()
        server_thread = threading.Thread(target=self.runServer)
        server_thread.start()
    def runServer(self):
        self.server.start()
    def UIobject(self):

        self.mainFrame = ctk.CTkFrame(master=self.app,
                           width=800,
                           height=400,
                           fg_color="dark slate gray")
        self.mainFrame.pack(expand = True,  fill="both")
        
        self.mainFrame2 = ctk.CTkFrame(master=self.mainFrame, border_color="cadetblue4",border_width=10,
                           width=800,
                           height=400,
                           fg_color="light slate gray")
        self.mainFrame2.pack(padx=10, pady=10, expand =True, fill="both")

        self.tableFrame = ctk.CTkFrame(master=self.mainFrame2,corner_radius=0, fg_color="cadetblue4")
        self.tableFrame.place(relx=0.05, rely=0.1, relheight=0.8,relwidth=0.4, )

        self.updateFrame = ctk.CTkFrame(master=self.tableFrame,corner_radius=0, fg_color="honeydew1", border_color="cadetblue4",border_width=2)
        self.updateFrame.place(relx=0, rely=0.9, relheight=0.1,relwidth=1.1)
        
        
        self.repoFrame = ctk.CTkFrame(master=self.mainFrame2,corner_radius=0, fg_color="cadetblue",  border_color="cadetblue4",border_width=2)
        self.repoFrame.place(relwidth=0.28, relx=0.67,rely=0.1, relheight= 0.8)
        
        
        self.repoTitle = tk.Label(master= self.repoFrame,fg="White",bg="cadet blue", 
                          text="Status",font=("Arial",16,"bold"))
        self.repoTitle.place(relx = 0.5, rely = 0.01, anchor="n", relheight=0.1)
        self.font3 = ('Arial',10,'bold')
        self.repo_list = CTkListbox(master=self.repoFrame, font=self.font3, 
                                    fg_color='white',border_color="#37d3ff",border_width=3, text_color="black", hover_color="SkyBlue3", select_color= "SkyBlue",
                                    )    
        self.repo_list.place(relwidth= 0.9, relx=0.5,rely=0.11, relheight= 0.25, anchor="n")


        self.repoTitle2 = tk.Label(master= self.repoFrame,fg="White",bg="cadet blue", 
                          text="Repository",font=("Arial",16,"bold"))
        self.repoTitle2.place(relx = 0.5, rely = 0.4, anchor="n", relheight=0.1)
        self.font3 = ('Arial',10,'bold')
        self.repo_list2 = CTkListbox(master=self.repoFrame, font=self.font3, 
                                    fg_color='white',border_color="#37d3ff",border_width=3, text_color="black", hover_color="SkyBlue3", select_color= "SkyBlue",
                                    )    
        self.repo_list2.place(relwidth= 0.9, relx=0.5,rely=0.51, relheight= 0.4, anchor="n")

    def create_button(self):
        self.updateButton = ctk.CTkButton(master=self.updateFrame,width=100,corner_radius=8, text='Update table',bg_color='honeydew1', command=self.tableUpdate)
        self.updateButton.place(relx=0.1, rely=0.8,relheight=0.5,  anchor='sw')

    def createButtonField(self):
        self.buttons = ctk.CTkFrame(master =self.mainFrame2, width=100, fg_color="ghost white",border_color="cadetblue4",border_width=2, corner_radius=0)
        self.buttons.place(relx=0.45, rely=0.1, relwidth= 0.2, relheight= 0.8)
        title = tk.Label(master= self.buttons,fg="White",bg="cadet blue", highlightthickness=3, highlightbackground="cadetblue4",
                          text="OPTION",font=("Arial",16,"bold"))
        
        title.place(relx = 0, rely = 0, relwidth= 1)

    def create_tree_widget(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("mystyle.Treeview", rowheight=30,  bd=0, font=('Calibri', 13)) # Modify the font of the body
        style.configure("mystyle.Treeview.Heading",rowheight=30,background= 'cadet blue',
                        foreground="white",relief="flat", font=('Calibri', 16,'bold')) # Modify the font of the headings
        style.map("mystyle.Treeview.Heading", background=[('active','cadet blue')])
        style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})])   
        columns = ('Client Name', 'Client IP')
        tree = ttk.Treeview(self.tableFrame, style="mystyle.Treeview", columns=columns,  show='headings')
        # define headings
        tree.column("# 1",anchor=ctk.CENTER)
        tree.heading("# 1", text="Client Name")
        tree.column("# 2", anchor=ctk.CENTER)
        tree.heading("# 2", text="Client IP")


        tree.tag_configure('odd', background='#E8E8E8')
        tree.tag_configure('even', background='#DFDFDF')
        tree.place(x=0, y=0, relheight=0.9,relwidth=1)

        return tree

    def tableUpdate(self):
        self.repo_list.delete("all")
        self.repo_list2.delete("all")



        for name in self.server.connectedClient:
            self.createButton(name)

    
    def createButton(self,name):
        if name not in self.clientListName:
            # self.listName.append(name)
            self.clientListName.append(name)
            self.tree.insert('', tk.END, text="1", values=(name, self.server.connectedClient[name]))
            button1 = ctk.CTkButton(self.buttons,corner_radius=2, fg_color="brown2",hover_color="brown3", text = "Ping", height=23, 
                                        command= lambda: self.ping_hostname(name))
            button2 = ctk.CTkButton(self.buttons,corner_radius=2, text = "Discover", height=23, 
                                        command= lambda: self.discover_hostname(name))
            button1.place(in_=self.ButtonFrame, relx=0.06, y=self.so_far, relwidth=0.42)
            button2.place(in_=self.ButtonFrame, relx= 0.52, y=self.so_far, relwidth=0.42)
            self.so_far += 24
    def ping_hostname(self, name):
        # self.repo_list2.delete("all")
        self.repo_list.insert("END",name+ ": "+ self.server.ping(name))
        
    
    def discover_hostname(self, name):
       
        self.server.discover(name)
        self.display_repo(name)

    def display_repo(self, hostname=''):
        self.repo_list2.delete("all")
        if hostname in self.server.connectedClient:
            for filename in self.server.clientFileList[self.server.connectedClient[hostname]]:
                self.repo_list2.insert("END",filename)

if __name__ == '__main__':
    app = AppServer()
    app.setup()
    app.app.mainloop()