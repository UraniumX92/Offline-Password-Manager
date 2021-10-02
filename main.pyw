import utils
from TkClass import Application_GUI

# -------------------------------------------------------------------------------- #
window_width = 550
window_height = 200
# -------------------------------------------------------------------------------- #
utils.create_files()

app = Application_GUI(title="Password Manager by Usama",icon="passman.ico",
                      geometry=f"{window_width}x{window_height}",
                      fixed_geometry=True)
x_pos = int(app.winfo_screenwidth()/3)
y_pos = int(app.winfo_screenheight()/3)
app.geometry = f"{window_width}x{window_height}+{x_pos}+{y_pos}"

user_data = utils.load_json(utils.user_data_file)

if user_data['username'] is None:
    app.init_setup()
else:
    app.login_window()

app.run()

#TODO: Commenting in code
#TODO: Exit Button on Main Menu screen
#TODO: Write README.md