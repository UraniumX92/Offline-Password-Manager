from tkinter import *
import tkinter.messagebox as msgbox
import utils


min_password_length = 8
default_padding = 10
buttons_padding = 5
standard_font_size = 10
scrollbar_width = 15
scrollbar_padding = 1
bold_font_tuple = ("arial",standard_font_size,'bold')
default_font_tuple = ("arial",standard_font_size)
default_font_color = "#faede3"
background_color = "#1c1c1c"


def copy_text(text_var:StringVar,button:Button,window:Tk):
    """
    Takes the text from the given entry and copies the text in the clipboard.
    """
    text = text_var.get()
    window.clipboard_clear()
    window.clipboard_append(text)
    window.update()
    button['text'] = "Copied"
    return


def show_hide(entry:Entry,button:Button):
    """
    Show / Hide button command for password entries... Shows the password text if the button text is "Show",
    Shows the bullet character if the button text is "Hide"
    """
    if button['text'] == "Show":
        entry.config(show="")
        entry.update()
        button['text'] = "Hide"
    else:
        entry.config(show=utils.bullet_char)
        entry.update()
        button['text'] = "Show"


def destroy_children(frame:Frame): 
    """
    Destroys all children widgets from the window and clears the entire window
    """
    all_children = frame.winfo_children()

    for widget in all_children:
        all_children.extend(widget.winfo_children())
    
    for widget in all_children:
        widget.destroy()


def command_handler(radio_var:IntVar,pos_x:int,pos_y:int):
    value = radio_var.get()
    command_dict = {
        0 : show_password,
        1 : add_password,
        2 : change_password,
        3 : remove_password
    }
    func = command_dict[value]
    func(pos_x=pos_x,pos_y=pos_y)


def change_mpass(pos_x,pos_y):
    width = 600
    height = 250
    cur_pass_val = StringVar()
    new_pass_val = StringVar()

    mpass_window = Toplevel(background=background_color)
    mpass_window.wm_iconbitmap("passman.ico")
    mpass_window.geometry(f"{width}x{height}+{pos_x+10}+{pos_y+10}")
    mpass_window.minsize(width,height)
    mpass_window.maxsize(width,height)
    mpass_window.grab_set()

    header_frame = Frame(master=mpass_window,background=background_color)
    header_frame.pack(padx=default_padding,pady=default_padding)
    title_label = Label(master=header_frame,background=background_color,foreground=default_font_color,text="Change Master Password",borderwidth=3,relief=RIDGE)
    title_label.pack(ipadx=5,ipady=5,padx=default_padding,pady=default_padding)

    main_frame = Frame(master=mpass_window,background=background_color,borderwidth=3,relief=RIDGE)
    main_frame.pack(padx=default_padding,pady=default_padding)
    current_mpass_label = Label(master=main_frame,background=background_color,foreground=default_font_color,text="Current Master Password :",font=default_font_tuple)
    current_mpass_label.grid(row=0,column=0,padx=default_padding,pady=default_padding)
    current_mpass_entry = Entry(master=main_frame,background=background_color,foreground=default_font_color,textvariable=cur_pass_val,show=utils.bullet_char,width=50)
    current_mpass_entry.grid(row=0,column=1,padx=default_padding,pady=default_padding)
    curr_show_button = Button(master=main_frame,background=background_color,foreground=default_font_color,text="Show",borderwidth=3,relief=RAISED,font=default_font_tuple,
                         command=lambda:show_hide(current_mpass_entry,curr_show_button))
    curr_show_button.grid(row=0,column=2,padx=default_padding,pady=default_padding)

    new_mpass_label = Label(master=main_frame,background=background_color,foreground=default_font_color,text="New Master Password :",font=default_font_tuple)
    new_mpass_label.grid(row=1,column=0,padx=default_padding,pady=default_padding)
    new_mpass_entry = Entry(master=main_frame,background=background_color,foreground=default_font_color,textvariable=new_pass_val,show=utils.bullet_char,width=50)
    new_mpass_entry.grid(row=1,column=1,padx=default_padding,pady=default_padding)
    new_show_button = Button(master=main_frame,background=background_color,foreground=default_font_color,text="Show",borderwidth=3,relief=RAISED,font=default_font_tuple,
                         command=lambda:show_hide(new_mpass_entry,new_show_button))
    new_show_button.grid(row=1,column=2,padx=default_padding,pady=default_padding)

    def change_master():
        inp_mpass = cur_pass_val.get()
        inp_newmpass = new_pass_val.get()
        
        user_data = utils.load_json(utils.user_data_file)
        mpass = utils.deciph(user_data['password'])

        if inp_mpass == '' or inp_newmpass == '':
            return msgbox.showinfo(title="Field Required!",message="Fields cannot be empty!\nEnter all the information required to continue.")
        elif inp_mpass != mpass:
            return msgbox.showinfo(title="Wrong Password",message="You've entered wrong Master Password\nPlease check and try again.")
        elif len(inp_newmpass) < min_password_length:
            return msgbox.showinfo(title="Password too small!",message=f"Master password must have atleast {min_password_length} characters.")
        else:
            confirm_masterpass = msgbox.askyesno(title="Warning!",message="Are you sure you want to continue with this master password?\n"
                                                                      "If you forget your master password then there is no way to recover it using this App\n"
                                                                      "Do you want to continue with this master password?")
        if confirm_masterpass:
            user_data = utils.load_json(utils.user_data_file)
            user_data['password'] = utils.ciph(inp_newmpass)
            utils.dump_json(user_data,utils.user_data_file)
            msgbox.showinfo(title="Success",message="Successfully changed the Master Password.")
            mpass_window.destroy()
    
    confirm_button = Button(master=main_frame,background=background_color,foreground=default_font_color,text="Confirm",font=bold_font_tuple,borderwidth=3,relief=RAISED,
                            command=lambda:change_master())
    confirm_button.grid(row=2,column=1,padx=default_padding,pady=default_padding)


def init_submit(name_var:StringVar,password_var:StringVar,window:Tk,pos_x:int,pos_y:int):
    username = name_var.get()
    password = password_var.get()

    if username == '' or password == '':
        return msgbox.showinfo(title="Field Required!",message="Fields cannot be empty!\nEnter all the information required to continue.")
    elif len(password) < min_password_length:
        return msgbox.showinfo(title="Password too small!",message=f"Master password must have atleast {min_password_length} characters.")
    else:
        confirm_masterpass = msgbox.askyesno(title="Warning!",message="Are you sure you want to continue with this master password?\n"
                                                                      "If you forget your master password then there is no way to recover it using this App\n"
                                                                      "Do you want to continue with this master password?")
        if confirm_masterpass:
            window.withdraw()
            index = utils.rng()
            full_key = utils.random_KeyGen()
            key = utils.key_mod(key=full_key,index=index,username=username)
            encrypted_pass = utils.ciph(password,key)

            user_data = {
                'username' : username,
                'password' : encrypted_pass,
                'key'      : full_key,
                'index'    : index
            }
            utils.dump_json(object=user_data,filename=utils.user_data_file)
            password_var.set("")
            add_password(pos_x=pos_x,pos_y=pos_y,window=window,label_title="To Complete the Initialzation process, Add a Password :",init_login=True)
        else:
            pass                                                                    
    

def login_submit(name_var:StringVar,password_var:StringVar,window:Tk,pos_x:int,pos_y:int):
    user_dict = utils.load_json(utils.user_data_file)
    password = utils.deciph(user_dict['password'])
    inp_password = password_var.get()
    if inp_password == '':
        return msgbox.showinfo(title="Field Required!",message="Fields cannot be empty!\nEnter all the information required to continue.")
    elif inp_password == password:
        password_var.set("")
        menu_screen(window=window,pos_x=pos_x,pos_y=pos_y)
    else:
        msgbox.showinfo(title="Incorrect Password",message="The password you entered is incorrect,please check the password and try again.")
        return


def menu_screen(window:Tk,pos_x:int,pos_y:int,init_login=False):
    window.withdraw()
    width = 350
    height = 370

    menu_window = Toplevel(background=background_color)
    menu_window.wm_iconbitmap("passman.ico")
    menu_window.geometry(f"{width}x{height}+{pos_x+10}+{pos_y+10}")
    menu_window.minsize(width,height)
    menu_window.maxsize(width,height)
    menu_window.grab_set()
    menu_window.protocol("WM_DELETE_WINDOW",lambda:window.destroy())

    header_frame = Frame(master=menu_window,background=background_color)
    header_frame.pack(padx=default_padding,pady=default_padding)
    title_label = Label(master=header_frame,background=background_color,foreground=default_font_color,text="Main Menu",font=bold_font_tuple,borderwidth=3,relief=RIDGE)
    title_label.pack(padx=default_padding,pady=default_padding,ipadx=default_padding,ipady=default_padding)

    radio_var = IntVar()
    main_frame = Frame(master=menu_window,background=background_color,borderwidth=5,relief=RIDGE)
    main_frame.pack(padx=default_padding,pady=default_padding)

    show_pass = Radiobutton(master=main_frame,background=background_color,foreground=default_font_color,text="Show Passwords",
                            activebackground=background_color,activeforeground=default_font_color,selectcolor=background_color,variable=radio_var,value=0)
    show_pass.pack(anchor=W,padx=default_padding,pady=default_padding)
    add_pass = Radiobutton(master=main_frame,background=background_color,foreground=default_font_color,text="Add a new password",
                           activebackground=background_color,activeforeground=default_font_color,selectcolor=background_color,variable=radio_var,value=1)
    add_pass.pack(anchor=W,padx=default_padding,pady=default_padding)
    change_pass = Radiobutton(master=main_frame,background=background_color,foreground=default_font_color,text="Change  existing passwords",
                              activebackground=background_color,activeforeground=default_font_color,selectcolor=background_color,variable=radio_var,value=2)
    change_pass.pack(anchor=W,padx=default_padding,pady=default_padding)
    remove_pass = Radiobutton(master=main_frame,background=background_color,foreground=default_font_color,text="Remove existing platform with passoword",
                              activebackground=background_color,activeforeground=default_font_color,selectcolor=background_color,variable=radio_var,value=3)
    remove_pass.pack(anchor=W,padx=default_padding,pady=default_padding)

    buttons_frame = Frame(master=main_frame,background=background_color)
    buttons_frame.pack(side=BOTTOM,anchor=S,padx=default_padding,pady=default_padding)

    proceed_button = Button(master=buttons_frame,background=background_color,foreground=default_font_color,text="Proceed",font=bold_font_tuple,
                            borderwidth=3,relief=RAISED,command=lambda:command_handler(radio_var=radio_var,pos_x=menu_window.winfo_x(),pos_y=menu_window.winfo_y()))
    proceed_button.grid(row=0,column=1,padx=default_padding,pady=default_padding)
    if init_login:
        exit_button = Button(master=buttons_frame,background=background_color,foreground=default_font_color,text="Exit",font=bold_font_tuple,
                                borderwidth=3,relief=RAISED,command=lambda:window.destroy())
        exit_button.grid(row=0,column=0,padx=default_padding,pady=default_padding)
    else:
        back_button = Button(master=buttons_frame,background=background_color,foreground=default_font_color,text="Back",font=bold_font_tuple,
                                borderwidth=3,relief=RAISED,command=lambda:back_to_login())
        back_button.grid(row=0,column=0,padx=default_padding,pady=default_padding)

    def back_to_login():
        menu_window.destroy()
        window.wm_deiconify()


def add_password(pos_x:int,pos_y:int,window:Tk=None,label_title:str="Add a Password :",init_login:bool=False):
    width = 600
    height = 250

    add_pass_window = Toplevel(background=background_color)
    add_pass_window.wm_iconbitmap("passman.ico")
    add_pass_window.geometry(f"{width}x{height}+{pos_x+10}+{pos_y+10}")
    add_pass_window.minsize(width,height)
    add_pass_window.maxsize(width,height)
    if init_login:
        add_pass_window.protocol("WM_DELETE_WINDOW",lambda:window.destroy())
    add_pass_window.grab_set()

    header_frame = Frame(master=add_pass_window,background=background_color)
    header_frame.pack(padx=default_padding,pady=default_padding)
    title_label = Label(master=header_frame,background=background_color,foreground=default_font_color,text=label_title,font=bold_font_tuple,borderwidth=3)
    title_label.pack(padx=default_padding,pady=default_padding)

    platform_value = StringVar()
    password_value = StringVar()

    main_frame = Frame(master=add_pass_window,background=background_color,borderwidth=5,relief=RIDGE)
    main_frame.pack(padx=default_padding,pady=default_padding)

    platform_label = Label(master=main_frame,background=background_color,foreground=default_font_color,justify=RIGHT,text="Platform Name :",font=default_font_tuple)
    platform_label.grid(row=0,column=0,padx=default_padding,pady=default_padding)
    platform_entry = Entry(master=main_frame,background=background_color,textvariable=platform_value,foreground=default_font_color,width=40)
    platform_entry.grid(row=0,column=1,padx=default_padding,pady=default_padding)

    password_label = Label(master=main_frame,background=background_color,foreground=default_font_color,justify=RIGHT,text="Password :",font=default_font_tuple)
    password_label.grid(row=1,column=0,padx=default_padding,pady=default_padding)
    password_entry = Entry(master=main_frame,background=background_color,textvariable=password_value,foreground=default_font_color,width=40,show=utils.bullet_char)
    password_entry.grid(row=1,column=1,padx=default_padding,pady=default_padding)
    show_button = Button(master=main_frame,background=background_color,foreground=default_font_color,text="Show",font=default_font_tuple,borderwidth=3,relief=RAISED,
                         command=lambda:show_hide(password_entry,show_button))
    show_button.grid(row=1,column=2,padx=default_padding,pady=default_padding)                        

    def add_new_password():
        platform = platform_value.get()
        password = password_value.get()
        if platform == '' or password == '':
            msgbox.showinfo(title="Missing Required Field!",message="Please fill the required fields to proceed")
            return
        else:
            encrypted_pass = utils.ciph(password)
            if init_login:
                user_passwords = {
                    platform : encrypted_pass
                }
                utils.dump_json(user_passwords,utils.passwords_file)
            else:
                user_passwords = utils.load_json(utils.passwords_file)
                if platform in user_passwords.keys():
                    return msgbox.showinfo(title="Platform Already Exists",message=f"You've already added the '{platform}' platform.\n"
                                                                             "Enter a different platform name or use 'Change an existing password' option from Main Menu.")                                                                      
                user_passwords.update({platform : encrypted_pass})
                utils.dump_json(user_passwords,utils.passwords_file)

            msgbox.showinfo(title="Success",message=f"Successfully Added password for platform : {platform}.")
            if init_login:
                menu_screen(window=window,pos_x=add_pass_window.winfo_x(),pos_y=add_pass_window.winfo_y(),init_login=init_login)
            add_pass_window.destroy()

    add_button = Button(master=main_frame,background=background_color,foreground=default_font_color,text="Add New Password",font=default_font_tuple,borderwidth=3,relief=RAISED,command=lambda:add_new_password())
    add_button.grid(row=2,column=1,padx=buttons_padding,pady=buttons_padding)
    
    exit_button = Button(master=main_frame,background=background_color,foreground=default_font_color,text="Exit",borderwidth=3,relief=RAISED,
                  command=lambda:add_pass_window.destroy())
    exit_button.grid(row=2,column=0,padx=default_padding,pady=default_padding)


def show_password(pos_x:int,pos_y:int):
    width = 850
    height = 550

    show_window = Toplevel(background=background_color)
    show_window.wm_iconbitmap("passman.ico")
    show_window.grab_set()
    show_window.geometry(f"{width}x{height}+{pos_x+10}+{pos_y+10}")
    show_window.minsize(width,height)
    show_window.maxsize(width,height)

    header_label = Label(master=show_window,background=background_color,foreground=default_font_color,text="Showing Passwords",font=bold_font_tuple,borderwidth=3,relief=RIDGE)
    header_label.pack(side=TOP,anchor=N,padx=default_padding,pady=default_padding,ipadx=default_padding,ipady=default_padding)

    options_frame = Frame(master=show_window,background=background_color,borderwidth=5,relief=RIDGE)
    options_frame.pack(side=LEFT,anchor=NW,padx=default_padding,pady=default_padding,fill=X)

    user_passwords = utils.load_json(utils.passwords_file)
    radio_var = StringVar()
    radio_var.set("Initial_value")

    display_frame = Frame(master=show_window,background=background_color,borderwidth=5,relief=RIDGE)
    display_frame.pack(side=RIGHT,anchor=NE,padx=default_padding,pady=default_padding,fill=X)
    dtitle_label = Label(master=display_frame,background=background_color,foreground=default_font_color,
                         text="Displaying Passwords here :",font=bold_font_tuple)
    dtitle_label.pack(anchor=N,padx=default_padding,pady=default_padding,ipadx=default_padding,ipady=default_padding)

    list_scrollbar = Scrollbar(master=options_frame,background=background_color,width=scrollbar_width,troughcolor=default_font_color)
    list_scrollbar.pack(side=RIGHT,anchor=E,fill=Y,padx=scrollbar_padding)

    plat_label = Label(master=options_frame,background=background_color,foreground=default_font_color,text="Platforms",font=bold_font_tuple,
                       borderwidth=3,relief=RIDGE)
    plat_label.pack(side=TOP,padx=default_padding,pady=default_padding,ipadx=5,ipady=5)

    platform_listbox = Listbox(master=options_frame,background=background_color,foreground=default_font_color,activestyle='dotbox',borderwidth=1,relief=RIDGE,
                               height=20,width=40,selectmode=SINGLE,yscrollcommand=list_scrollbar.set)

    platform_listbox.pack(anchor=W,padx=default_padding,pady=default_padding,fill=X)
    list_scrollbar.config(command=platform_listbox.yview)

    exit_button = Button(master=options_frame,background=background_color,foreground=default_font_color,text="Exit",borderwidth=3,relief=RAISED,
                  command=lambda:show_window.destroy())
    exit_button.pack(padx=default_padding,pady=default_padding)

    for platform in user_passwords.keys():
        platform_listbox.insert(END,platform)

    def display_pass(event):
        try:
            requested_platform = platform_listbox.get(platform_listbox.curselection())
        except TclError:
            return
        destroy_children(frame=display_frame)
        dtitle_label = Label(master=display_frame,background=background_color,foreground=default_font_color,
                             text=f"Platform : {requested_platform}",font=bold_font_tuple)
        dtitle_label.pack(anchor=N,padx=default_padding,pady=default_padding,ipadx=5,ipady=5)
        user_passwords = utils.load_json(utils.passwords_file)
        enc_password = user_passwords[requested_platform]
        requested_password = utils.deciph(enc_password)
        pass_value = StringVar()
        pass_value.set(requested_password)
        display_entry = Entry(master=display_frame,textvariable=pass_value,background=background_color,foreground=default_font_color,width=50,font=default_font_tuple,
                              disabledbackground=background_color,disabledforeground=default_font_color,state="disable",show=utils.bullet_char)
        display_entry.pack(side=LEFT,padx=default_padding,pady=default_padding)
        show_button = Button(master=display_frame,text="Show",background=background_color,foreground=default_font_color,font=default_font_tuple,
                             borderwidth=3,relief=RAISED,command=lambda:show_hide(entry=display_entry,button=show_button))
        copy_button = Button(master=display_frame,text="Copy",background=background_color,foreground=default_font_color,font=default_font_tuple,
                             borderwidth=3,relief=RAISED,command=lambda:copy_text(text_var=pass_value,button=copy_button,window=show_window))
        copy_button.pack(side=RIGHT,anchor=E,padx=buttons_padding,pady=buttons_padding)
        show_button.pack(side=RIGHT,anchor=E,padx=buttons_padding,pady=buttons_padding)

    platform_listbox.bind("<<ListboxSelect>>",display_pass)


def change_password(pos_x:int,pos_y:int):
    width = 850
    height = 550

    change_window = Toplevel(background=background_color)
    change_window.wm_iconbitmap("passman.ico")
    change_window.grab_set()
    change_window.geometry(f"{width}x{height}+{pos_x+10}+{pos_y+10}")
    change_window.minsize(width,height)
    change_window.maxsize(width,height)

    header_label = Label(master=change_window,background=background_color,foreground=default_font_color,text="Change Passwords",font=bold_font_tuple,borderwidth=3,relief=RIDGE)
    header_label.pack(side=TOP,anchor=N,padx=default_padding,pady=default_padding,ipadx=default_padding,ipady=default_padding)

    options_frame = Frame(master=change_window,background=background_color,borderwidth=5,relief=RIDGE)
    options_frame.pack(side=LEFT,anchor=NW,padx=default_padding,pady=default_padding,fill=X)

    user_passwords = utils.load_json(utils.passwords_file)
    radio_var = StringVar()
    radio_var.set("Initial_value")

    display_frame = Frame(master=change_window,background=background_color,borderwidth=5,relief=RIDGE)
    display_frame.pack(side=RIGHT,anchor=NE,padx=default_padding,pady=default_padding,fill=X)
    dtitle_label = Label(master=display_frame,background=background_color,foreground=default_font_color,
                         text="Displaying Passwords here :",font=bold_font_tuple)
    dtitle_label.grid(row=0,column=0,padx=default_padding,pady=default_padding,ipadx=default_padding,ipady=default_padding)

    list_scrollbar = Scrollbar(master=options_frame,background=background_color,width=scrollbar_width)
    list_scrollbar.pack(side=RIGHT,anchor=E,fill=Y,padx=scrollbar_padding)

    plat_label = Label(master=options_frame,background=background_color,foreground=default_font_color,text="Platforms",font=bold_font_tuple,
                       borderwidth=3,relief=RIDGE)
    plat_label.pack(side=TOP,padx=default_padding,pady=default_padding,ipadx=5,ipady=5)

    platform_listbox = Listbox(master=options_frame,background=background_color,foreground=default_font_color,activestyle='dotbox',borderwidth=1,relief=RIDGE,
                               height=20,width=40,selectmode=SINGLE,yscrollcommand=list_scrollbar.set)

    platform_listbox.pack(anchor=W,padx=default_padding,pady=default_padding,fill=X)
    list_scrollbar.config(command=platform_listbox.yview)

    exit_button = Button(master=options_frame,background=background_color,foreground=default_font_color,text="Exit",borderwidth=3,relief=RAISED,
                  command=lambda:change_window.destroy())
    exit_button.pack(padx=default_padding,pady=default_padding)

    for platform in user_passwords.keys():
        platform_listbox.insert(END,platform)

    def display_pass(event):
        try:
            requested_platform = platform_listbox.get(platform_listbox.curselection())
        except TclError:
            return

        destroy_children(frame=display_frame)
        dtitle_label = Label(master=display_frame,background=background_color,foreground=default_font_color,
                             text=f"Platfrom : {requested_platform}",font=bold_font_tuple)
        dtitle_label.grid(row=0,column=0,padx=default_padding,pady=default_padding,ipadx=5,ipady=5)
        user_passwords = utils.load_json(utils.passwords_file)
        enc_password = user_passwords[requested_platform]
        requested_password = utils.deciph(enc_password)
        pass_value = StringVar()
        pass_value.set(requested_password)
        display_entry = Entry(master=display_frame,textvariable=pass_value,background=background_color,foreground=default_font_color,width=50,font=default_font_tuple,
                              disabledbackground=background_color,disabledforeground=default_font_color,state="normal",show=utils.bullet_char)
        display_entry.grid(row=1,column=0,padx=default_padding,pady=default_padding)
        show_button = Button(master=display_frame,text="Show",background=background_color,foreground=default_font_color,font=default_font_tuple,
                             borderwidth=3,relief=RAISED,command=lambda:show_hide(entry=display_entry,button=show_button))
        show_button.grid(row=1,column=1,padx=buttons_padding,pady=buttons_padding)
        copy_button = Button(master=display_frame,text="Copy",background=background_color,foreground=default_font_color,font=default_font_tuple,
                             borderwidth=3,relief=RAISED,command=lambda:copy_text(text_var=pass_value,button=copy_button,window=change_window))
        copy_button.grid(row=1,column=2,padx=buttons_padding,pady=buttons_padding)
        def change_pass():
            confirm_change = msgbox.askyesno(title="Confirmation",message=f"Are you sure you want to change password for platform : {requested_platform}")
            if not confirm_change:
                return
            else:
                user_passwords = utils.load_json(utils.passwords_file)
                user_passwords[requested_platform] = utils.ciph(pass_value.get())
                utils.dump_json(user_passwords,utils.passwords_file)
                msgbox.showinfo(title="Success",message=f"Successfully changed the password for platform : {requested_platform}")

        change_button = Button(master=display_frame,background=background_color,foreground=default_font_color,text="Change Selected Password",font=bold_font_tuple,
                               borderwidth=3,relief=RAISED,command=lambda:change_pass())
        change_button.grid(row=2,column=0,padx=buttons_padding,pady=buttons_padding)

    platform_listbox.bind("<<ListboxSelect>>",display_pass)



def remove_password(pos_x:int,pos_y:int):
    width = 850
    height = 550

    remove_window = Toplevel(background=background_color)
    remove_window.wm_iconbitmap("passman.ico")
    remove_window.grab_set()
    remove_window.geometry(f"{width}x{height}+{pos_x+10}+{pos_y+10}")
    remove_window.minsize(width,height)
    remove_window.maxsize(width,height)

    header_label = Label(master=remove_window,background=background_color,foreground=default_font_color,text="Remove Platforms & Passwords",font=bold_font_tuple,borderwidth=3,relief=RIDGE)
    header_label.pack(side=TOP,anchor=N,padx=default_padding,pady=default_padding,ipadx=default_padding,ipady=default_padding)

    options_frame = Frame(master=remove_window,background=background_color,borderwidth=5,relief=RIDGE)
    options_frame.pack(side=LEFT,anchor=NW,padx=default_padding,pady=default_padding,fill=X)

    user_passwords = utils.load_json(utils.passwords_file)
    radio_var = StringVar()
    radio_var.set("Initial_value")

    display_frame = Frame(master=remove_window,background=background_color,borderwidth=5,relief=RIDGE)
    display_frame.pack(side=RIGHT,anchor=NE,padx=default_padding,pady=default_padding,fill=X)
    dtitle_label = Label(master=display_frame,background=background_color,foreground=default_font_color,
                         text="Displaying Passwords here :",font=bold_font_tuple)
    dtitle_label.grid(row=0,column=0,padx=default_padding,pady=default_padding,ipadx=default_padding,ipady=default_padding)

    list_scrollbar = Scrollbar(master=options_frame,background=background_color,width=scrollbar_width)
    list_scrollbar.pack(side=RIGHT,anchor=E,fill=Y,padx=scrollbar_padding)

    plat_label = Label(master=options_frame,background=background_color,foreground=default_font_color,text="Platforms",font=bold_font_tuple,
                       borderwidth=3,relief=RIDGE)
    plat_label.pack(side=TOP,padx=default_padding,pady=default_padding,ipadx=5,ipady=5)

    platform_listbox = Listbox(master=options_frame,background=background_color,foreground=default_font_color,activestyle='dotbox',borderwidth=1,relief=RIDGE,
                               height=20,width=40,selectmode=SINGLE,yscrollcommand=list_scrollbar.set)

    platform_listbox.pack(anchor=W,padx=default_padding,pady=default_padding,fill=X)
    list_scrollbar.config(command=platform_listbox.yview)

    exit_button = Button(master=options_frame,background=background_color,foreground=default_font_color,text="Exit",borderwidth=3,relief=RAISED,
                  command=lambda:remove_window.destroy())
    exit_button.pack(padx=default_padding,pady=default_padding)

    for platform in user_passwords.keys():
        platform_listbox.insert(END,platform)

    def display_pass(event):
        try:
            requested_platform = platform_listbox.get(platform_listbox.curselection())
        except TclError:
            return

        destroy_children(frame=display_frame)
        dtitle_label = Label(master=display_frame,background=background_color,foreground=default_font_color,
                             text=f"Platfrom : {requested_platform}",font=bold_font_tuple)
        dtitle_label.grid(row=0,column=0,padx=default_padding,pady=default_padding,ipadx=5,ipady=5)
        user_passwords = utils.load_json(utils.passwords_file)
        enc_password = user_passwords[requested_platform]
        requested_password = utils.deciph(enc_password)
        pass_value = StringVar()
        pass_value.set(requested_password)
        display_entry = Entry(master=display_frame,textvariable=pass_value,background=background_color,foreground=default_font_color,width=50,font=default_font_tuple,
                              disabledbackground=background_color,disabledforeground=default_font_color,state="disable",show=utils.bullet_char)
        display_entry.grid(row=1,column=0,padx=default_padding,pady=default_padding)
        show_button = Button(master=display_frame,text="Show",background=background_color,foreground=default_font_color,font=default_font_tuple,
                             borderwidth=3,relief=RAISED,command=lambda:show_hide(entry=display_entry,button=show_button))
        show_button.grid(row=1,column=1,padx=buttons_padding,pady=buttons_padding)
        copy_button = Button(master=display_frame,text="Copy",background=background_color,foreground=default_font_color,font=default_font_tuple,
                             borderwidth=3,relief=RAISED,command=lambda:copy_text(text_var=pass_value,button=copy_button,window=remove_window))
        copy_button.grid(row=1,column=2,padx=buttons_padding,pady=buttons_padding)


        remove_button = Button(master=display_frame,background=background_color,foreground=default_font_color,text="Remove Selected Platform",font=bold_font_tuple,
                               borderwidth=3,relief=RAISED,command=lambda:remove_pass())
        remove_button.grid(row=2,column=0,padx=buttons_padding,pady=buttons_padding)
        def remove_pass():
            confirm_remove = msgbox.askyesno(title="Confirmation",message=f"Are you sure you want to remove this platform : {requested_platform}")
            if not confirm_remove:
                return
            else:
                user_passwords:dict = utils.load_json(utils.passwords_file)
                user_passwords.pop(requested_platform)
                utils.dump_json(user_passwords,utils.passwords_file)
                platform_listbox.delete(platform_listbox.curselection())
                msgbox.showinfo(title="Success",message=f"Successfully removed the platform : {requested_platform}")
                remove_button.destroy()
                dtitle_label['text'] = f"Platform (Removed) : {requested_platform}"
                # dtitle_label.update()

    platform_listbox.bind("<<ListboxSelect>>",display_pass)
