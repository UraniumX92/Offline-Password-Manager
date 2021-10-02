from tkinter import *
import commands
import tkinter.messagebox as msgbox
import utils
from utils import dump_json,load_json


class Application_GUI(Tk):
    default_padding = 10
    buttons_padding = 5
    standard_font_size = 10
    bold_font_tuple = ("arial",standard_font_size,'bold')
    default_font_tuple = ("arial",standard_font_size)
    default_font_color = "#faede3"


    def __init__(self,title:str,geometry:str,icon=None,background="#1c1c1c",fixed_geometry=True):
        super().__init__()
        self.width = int(geometry.split('x')[0])
        self.height = int(geometry.split('x')[1].split("+")[0])
        try:
            self.x_pos = geometry.split('+')[1]
            self.y_pos = geometry.split('+')[2]
        except IndexError:
            pass
        self.geometry = geometry
        self._background_color = background
        self._title = title
        self._icon = icon
        self.background_color = self._background_color
        self.window_title = self._title
        self.icon = self._icon
        if fixed_geometry:
            self.minsize(width=self.width,height=self.height)
            self.maxsize(width=self.width,height=self.height)

    # ------------------------------------------- Properties and setters ------------------------------------------- # 
    @property
    def geometry(self):
        return f"{self.width}x{self.height}+{self.x_pos}+{self.y_pos}"

    @geometry.setter
    def geometry(self,geometry:str):
        super().geometry(geometry)
        self.width = geometry.split("x")[0]
        self.height = geometry.split("x")[1].split("+")[0]
        try:
            self.x_pos = geometry.split('+')[1]
            self.y_pos = geometry.split('+')[2]
        except IndexError:
            pass


    @property
    def background_color(self):
        return self._background_color

    @background_color.setter
    def background_color(self,background):
        self._background_color = background
        self.configure(background=self._background_color)

    
    @property
    def icon(self):
        return self._icon

    @icon.setter
    def icon(self,icon):
        self._icon = icon
        self.wm_iconbitmap(self._icon)


    @property
    def window_title(self):
        return self._title
    
    @window_title.setter
    def window_title(self,title):
        self._title = title
        self.title(self._title)
    # -------------------------------------------------------------------------------------------------------------- #

    # ----------------------------------------------- Object Methodds ----------------------------------------------- #
    def init_setup(self):
        name_value = StringVar()
        password_value = StringVar()

        login_label = Label(master=self,background=self.background_color,foreground=self.default_font_color,text="Setup Your Password Manager",font=self.bold_font_tuple,
                            relief=RIDGE,borderwidth=3)
        login_label.pack(side='top',padx=self.default_padding,pady=self.default_padding)

        login_frame = Frame(master=self,background=self.background_color,borderwidth=2,relief=RIDGE)
        login_frame.pack(side='top',padx=self.default_padding,pady=self.default_padding,ipadx=5,ipady=5)

        name_label = Label(master=login_frame,background=self.background_color,foreground=self.default_font_color,text="Username :",font=self.default_font_tuple)
        name_label.grid(row=0,column=0,padx=self.default_padding,pady=self.default_padding)
        name_entry = Entry(master=login_frame,background=self.background_color,foreground=self.default_font_color,width=50,textvariable=name_value)
        name_entry.grid(row=0,column=1,padx=self.default_padding,pady=self.default_padding)

        password_label = Label(master=login_frame,background=self.background_color,foreground=self.default_font_color,text="Master Password :",font=self.default_font_tuple)
        password_label.grid(row=1,column=0,padx=self.default_padding,pady=self.default_padding)
        password_entry = Entry(master=login_frame,background=self.background_color,foreground=self.default_font_color,show=utils.bullet_char,width=50,textvariable=password_value)
        password_entry.grid(row=1,column=1,padx=self.default_padding,pady=self.default_padding)
        show_button = Button(master=login_frame,background=self.background_color,foreground=self.default_font_color,text="Show",borderwidth=3,relief=RAISED,
                             command=lambda:commands.show_hide(password_entry,show_button))
        show_button.grid(row=1,column=2)

        submit_button = Button(master=login_frame,background=self.background_color,foreground=self.default_font_color,text="Submit",font=self.bold_font_tuple,borderwidth=3,relief=RAISED,
                               command=lambda:commands.init_submit(name_var=name_value,password_var=password_value,window=self,pos_x=self.winfo_x(),pos_y=self.winfo_y()))
        submit_button.grid(row=2,column=1,padx=self.buttons_padding,pady=self.buttons_padding)


    def login_window(self):
        name_value = StringVar()
        password_value = StringVar()

        login_label = Label(master=self,background=self.background_color,foreground=self.default_font_color,text="Login to Password Manager",font=self.bold_font_tuple,
                            relief=RIDGE,borderwidth=3)
        login_label.pack(side='top',padx=self.default_padding,pady=self.default_padding)

        login_frame = Frame(master=self,background=self.background_color,borderwidth=2,relief=RIDGE)
        login_frame.pack(side='top',padx=self.default_padding,pady=self.default_padding,ipadx=5,ipady=5)

        name_label = Label(master=login_frame,background=self.background_color,foreground=self.default_font_color,text="Username :",font=self.default_font_tuple)
        name_label.grid(row=0,column=0,padx=self.default_padding,pady=self.default_padding)
        name_entry = Entry(master=login_frame,background=self.background_color,foreground=self.default_font_color,width=50,textvariable=name_value)
        name_entry.grid(row=0,column=1,padx=self.default_padding,pady=self.default_padding)
        
        user_dict = load_json(utils.user_data_file)
        name_value.set(user_dict['username'])
        name_entry.config(state="disable",disabledbackground=self.background_color,disabledforeground=self.default_font_color)

        password_label = Label(master=login_frame,background=self.background_color,foreground=self.default_font_color,text="Master Password :",font=self.default_font_tuple)
        password_label.grid(row=1,column=0,padx=self.default_padding,pady=self.default_padding)
        password_entry = Entry(master=login_frame,background=self.background_color,foreground=self.default_font_color,show=utils.bullet_char,width=50,textvariable=password_value)
        password_entry.grid(row=1,column=1,padx=self.default_padding,pady=self.default_padding)
        show_button = Button(master=login_frame,background=self.background_color,foreground=self.default_font_color,text="Show",borderwidth=3,relief=RAISED,
                             command=lambda:commands.show_hide(password_entry,show_button))
        show_button.grid(row=1,column=2)

        submit_button = Button(master=login_frame,background=self.background_color,foreground=self.default_font_color,text="Submit",font=self.bold_font_tuple,borderwidth=3,relief=RAISED,
                               command=lambda:commands.login_submit(name_var=name_value,password_var=password_value,window=self,pos_x=self.winfo_x(),pos_y=self.winfo_y()))
        submit_button.grid(row=2,column=2,padx=self.buttons_padding,pady=self.buttons_padding)

        change_mpass_button = Button(master=login_frame,background=self.background_color,foreground=self.default_font_color,text="Change Master Password",font=self.bold_font_tuple,
                                     borderwidth=3,relief=RAISED,command=lambda:commands.change_mpass(pos_x=self.winfo_x(),pos_y=self.winfo_y()))
        change_mpass_button.grid(row=2,column=1,padx=self.default_padding,pady=self.default_padding)



    def error_box(self,title:str,message:str):
        errbox = msgbox.showerror(title=title,message=message)
        return errbox


    def info_box(self,title:str,message:str):
        infobox = msgbox.showinfo(title=title,message=message)
        return infobox


    def askyesno(self,title:str,message:str):
        askbox = msgbox.askyesno(title=title,message=message)
        return askbox


    def exit_window(self):
        exit_box = msgbox.askyesno(title="Confirm Exit",message="Are you sure you want exit?")
        if exit_box:
            self.destroy()
        else:
            return


    def run(self):
        self.mainloop()
