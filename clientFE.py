import tkinter as tk
import customtkinter as ctk
from client import *
import threading
import time
from tkinter import END, filedialog,messagebox
import os
from CTkListbox import *


class App:
    def __init__(self):
        self.app = ctk.CTk()
        self.client =  Client('',0,'') 
        # self.Client_UI()
        self.Connect()

    def setup(self):
        ctk.set_appearance_mode('dark')
        ctk.set_default_color_theme("green")
        self.app.title('FileSharing_UI')
        self.app.geometry('800x400')

    def Connect(self):
        #Create a Frame
        self.Connect_Frame = ctk.CTkFrame(master=self.app,
                           width=800,
                           height=200,
                           fg_color='dark slate gray')
        self.Connect_Frame.place(relwidth=0.95, relheight=0.95, relx= 0.5,rely=0.5, anchor = "center")

        # Add title
        self.App_Title = ctk.CTkLabel(master=self.Connect_Frame,text="FILE-SHARING APPLICATION",font=("Arial",20,"bold"),text_color='white')
        self.App_Title.place(relx = 0.5, rely = 0.1, anchor = "center")

        # Add Server_IP
        self.Server_IP = ctk.CTkLabel(master=self.Connect_Frame,text="SERVER_IP",font=("Arial",15,"bold"),text_color='white')
        self.Server_IP.place(relx = 0.3, rely = 0.3)
        self.Server_IP_Entry = ctk.CTkEntry(master=self.Connect_Frame,
                              placeholder_text='Enter serverIP',
                              placeholder_text_color= "gray69",
                              
                              width=200,
                              height=30,
                              fg_color="light slate gray",
                              text_color='white',
                              corner_radius=10)
        self.Server_IP_Entry.configure(state='normal')
        self.Server_IP_Entry.place(relx = 0.45, rely = 0.3)

        #Add HostName
        self.HostName = ctk.CTkLabel(master=self.Connect_Frame,text="HOSTNAME",font=("Arial",15,"bold"),text_color='white')
        self.HostName.place(relx = 0.3, rely = 0.4)
        self.Hostname_Entry = ctk.CTkEntry(master=self.Connect_Frame,
                              placeholder_text='Enter your hostname',
                              placeholder_text_color="gray69",
                              width=200,
                              height=30,
                              text_color='white',
                              fg_color="light slate gray",
                              corner_radius=10)
        self.Hostname_Entry.configure(state='normal')
        self.Hostname_Entry.place(relx = 0.45, rely = 0.4)

        #Add Button
        self.Connect_Button = ctk.CTkButton(master=self.app,
                                            hover_color="slate gray",
                                             fg_color="light slate gray", font=("Aria",15,"bold"),bg_color='dark slate gray',
                                                text='Connect', command=self.Connect_To_Server,text_color="white")
        self.Connect_Button.place(relx=0.5, rely=0.7, anchor=tk.CENTER)

        self.client = Client('',0,'')
    def Connect_To_Server(self):
        SERVER_IP = self.Server_IP_Entry.get()
        SERVER_PORT = 4004
        hostname = self.Hostname_Entry.get()
        if not SERVER_IP or not hostname:
            # Handle empty fields
            print("Please enter both Server IP and Hostname.")
            return
        self.client = Client(SERVER_IP, SERVER_PORT, hostname)
        if(self.client.start() == False):
            return
        time.sleep(0.5)
        
        # Hide the Connect frame
        self.Connect_Frame.pack_forget()

        self.Client_UI()
    def Client_UI(self):
        # Build a frame
        self.Client_UI_Frame = ctk.CTkFrame(master=self.app, width=800, height=500, fg_color='darkslategray4')
        self.Client_UI_Frame.place(relwidth=0.95, relheight=0.95, relx= 0.5,rely=0.5, anchor = "center")

        # Add title 
        self.App_Title = ctk.CTkLabel(master=self.Client_UI_Frame,text="FILE-SHARING APPLICATION",font=("Arial",20,"bold"),text_color='white')
        self.App_Title.place(relx = 0.5, rely = 0.1, anchor = "s")

        # Build Sub frame

        self.Left_Sub_Frame = ctk.CTkFrame(master=self.Client_UI_Frame, fg_color='deepskyblue4')
        self.Left_Sub_Frame.place(relx= 0.1,rely=0.13, relwidth=0.45, relheight=0.8)

        self.Right_Sub_Frame = ctk.CTkFrame(master=self.Client_UI_Frame,  fg_color='deepskyblue4')
        self.Right_Sub_Frame.place(relx= 0.6,rely=0.13, relwidth=0.3, relheight=0.8)

        # Add suggest
        self.commandLabel = ctk.CTkLabel(master=self.Right_Sub_Frame,text="COMMAND",font=("Arial",17,"bold"),text_color='white')
        self.commandLabel.place(relx = 0.5, rely = 0.01, anchor='n')

        # Add option
        self.publishLabel = ctk.CTkLabel(master=self.Right_Sub_Frame,text="Upload a file to repository",font=("Arial",14,),text_color='white')
        self.publishLabel.place(relx = 0.5, rely = 0.25, anchor='s')
        self.Publish_Button = ctk.CTkButton(master=self.Right_Sub_Frame,
                                            hover_color="slate gray",
                                             fg_color="light slate gray", font=("Aria",15,"bold"),
                                                text='PUBLISH', command=self.Add_Local_File,text_color="white")
        self.Publish_Button.place(relx=0.5, rely=0.35, anchor='s')

        self.fetchLabel = ctk.CTkLabel(master=self.Right_Sub_Frame,text="Request file from other client",font=("Arial",14,),text_color='white')
        self.fetchLabel.place(relx = 0.5, rely = 0.5, anchor='s')
        self.Fetch_Button = ctk.CTkButton(master=self.Right_Sub_Frame,
                                            hover_color="slate gray",
                                             fg_color="light slate gray", font=("Aria",15,"bold"),
                                                text='FETCH', command=self.Fetch_Input,text_color="white")
        self.Fetch_Button.pack()
        self.Fetch_Button.place(relx=0.5, rely=0.6, anchor='s')
        
        self.fetchLabel = ctk.CTkLabel(master=self.Right_Sub_Frame,text="Disconnect from current server",font=("Arial",14,),text_color='white')
        self.fetchLabel.place(relx = 0.5, rely = 0.75, anchor='s')
        self.Quit_Button = ctk.CTkButton(master=self.Right_Sub_Frame,
                                            hover_color="slate gray",
                                             fg_color="light slate gray", font=("Aria",15,"bold"),
                                                text='QUIT', command=self.Disconnect_From_Server,text_color="white")
        self.Quit_Button.place(relx=0.5, rely=0.85, anchor='s')

        #data from repository
        self.font3 = ('Arial',10,'bold')
        self.repoTitle = tk.Label(master= self.Left_Sub_Frame,fg="White",bg="deepskyblue4", 
                                text="Repository",font=("Arial",16,"bold"))
        self.repoTitle.place(relx = 0.5, rely = 0.01, anchor="n", relheight=0.1)
        self.repo_list = CTkListbox(master=self.Left_Sub_Frame, font=self.font3, fg_color='white',border_color="#37d3ff",border_width=3, 
                                    text_color="black", hover_color="SkyBlue3", select_color= "SkyBlue" )    
        self.repo_list.place(relwidth= 0.8, relx=0.5,rely=0.15, relheight= 0.6, anchor="n")
        
        path = os.getcwd()
        newpath = path + '/repository'
        repo_filename = os.listdir(newpath)
        
        for filename in repo_filename:
            self.repo_list.insert("END",filename)
        # var1 = tk.StringVar()    
        self.delete_Button = ctk.CTkButton(master=self.Left_Sub_Frame,
                                            hover_color="slate gray",
                                             fg_color="light slate gray", font=("Aria",15,"bold"),
                                                text='Delete selected file', command=self.deleteFile,text_color="white")
        self.delete_Button.place(relx=0.5, rely=0.8, anchor='n')

    def deleteFile(self):
        fname = self.repo_list.get()
        if fname == None:
            messagebox.showinfo(title='Information', message="Please select a file to delete!")
            return

        self.client.deleteFile(self.repo_list.get())
        self.repo_list.delete(self.repo_list.curselection())
        messagebox.showinfo(title='Information', message=fname + " deleted successfully!")

        # print(s)



    def Fetch_Input(self):
        # self.Right_Sub_Frame.destroy()
        time.sleep(0.5)
        self.Fetch_Frame()
        
    def Fetch_Frame(self):
        # Fetch frame

        self.Fetch_Input_Frame = ctk.CTkFrame(master=self.Client_UI_Frame,  fg_color='deepskyblue4')
        self.Fetch_Input_Frame.place(relx= 0.6,rely=0.13, relwidth=0.3, relheight=0.8)
        # Fetch suggest
        self.Fetch_Suggest = ctk.CTkLabel(master=self.Fetch_Input_Frame,text="PLEASE TYPE THE " + '\n' +  "NAME OF FILE THAT YOU" + '\n' + "WANT TO FETCH!",font=("Arial",13,"bold"),text_color='white')
        self.Fetch_Suggest.place(relx = 0.5, rely = 0.1, anchor='c')
        # Fetch input
        self.Fetch_File_Entry = ctk.CTkEntry(master=self.Fetch_Input_Frame,
                              placeholder_text='Assignment_1_HK231.pdf',
                              placeholder_text_color="white",
                              width=200,
                              height=30,
                              text_color='white',
                              fg_color="light slate gray",
                              corner_radius=10)
        self.Fetch_File_Entry.configure(state='normal')
        self.Fetch_File_Entry.place(relx = 0.5, rely = 0.3, anchor='c')
        # Fetch button
        self.Fetch_Button = ctk.CTkButton(master=self.Fetch_Input_Frame,
                                            hover_color="slate gray",
                                             fg_color="light slate gray", font=("Aria",13,"bold"),
                                                text='FETCH', command=self.Fetch_File,text_color="white")
        self.Fetch_Button.place(relx=0.5, rely=0.7, anchor=tk.CENTER)

        self.returnButton = ctk.CTkButton(master=self.Fetch_Input_Frame,
                                            hover_color="slate gray",
                                             fg_color="light slate gray", font=("Aria",13,"bold"),
                                                text='Return', command=self.returnToCommand,text_color="white")
        self.returnButton.place(relx=0.5, rely=0.9, anchor=tk.CENTER)
    def returnToCommand(self):
        self.Fetch_Input_Frame.destroy()
        time.sleep(0.5)
        # self.Right_Sub_Frame.pack()
        
    # Handle Publish
    def Add_Local_File(self):
        filepath = filedialog.askopenfilename()
        directory, filename = os.path.split(filepath)

        self.client.publish(directory,filename)
        
        self.repo_list.delete(0,END)
        path = os.getcwd()
        newpath = path + '/repository'
        repo_filename = os.listdir(newpath)
        for fname in repo_filename:
            self.repo_list.insert("END",fname)
        messagebox.showinfo(title='Information', message=filename + " uploaded successfully!")
        
    # Handle Fetch
    def Fetch_File(self):
        if self.Fetch_File_Entry.get() == '':
            messagebox.showinfo("Error", "Please enter file name!")
        else:
            msg = self.client.fetch(self.Fetch_File_Entry.get())
            if msg == 'These are clients having the file:':
                self.repo_list.insert("END",self.Fetch_File_Entry.get())
                messagebox.showinfo("Success", "Done fetch file!")
            else:
                messagebox.showerror("Error",msg)
    # Hanlde Quit
    def Disconnect_From_Server(self):
        # self.app.withdraw()
        self.client.quitCli()
        self.Connect()
if __name__ == '__main__':
    app = App()
    app.setup()
    app.app.mainloop()