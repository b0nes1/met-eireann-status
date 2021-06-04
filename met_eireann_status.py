import requests
import json
import tkinter
from tkinter import ttk, messagebox
from datetime import datetime
import textwrap
from os import getcwd

# read json files with weather information
with open(getcwd() + '\\' + "region_codes.json", "r") as file:
    REGION_CODES = json.loads(file.read())

with open(getcwd() + '\\' + "marine_codes.json", "r") as file:
    MARINE_CODES = json.loads(file.read())

dimensions = {"width": "60", "height": "10", }
style_no_warning = {"foreground": "black", "background": "green", "font": "Helvetica 11 bold"}
style_bold = {"font": "Helvetica 9 bold"}
level_to_style = {
    "Yellow": {"foreground": "Black", "background": "yellow"},
    "Orange": {"foreground": "Black", "background": "orange"},
    "Red": {"foreground": "Black", "background": "red"},
}

warnings_objects = []  # Warnings class objects
card_objects = []


class WarningInfo:
    """Stores necessary weather warning information"""

    def __init__(self, json_data):
        warnings_objects.append(self)

        print(json_data)
        self.cap_id = json_data['capId']
        self.id = json_data['id']
        self.type = json_data['type']
        self.severity = json_data['severity']
        self.certainty = json_data['certainty']
        self.level = json_data['level']
        self.issued = json_data['issued']
        self.updated = json_data['updated']
        self.onset = json_data['onset']
        self.expiry = json_data['expiry']
        self.headline = json_data['headline']
        self.description = json_data['description']
        self.regions = json_data['regions']
        self.status = json_data['status']

        self.delta = None
        self.delta_msg = None
        self.style = level_to_style[self.level]

        if update_time(self) == 'expired':
            print("warning is expired")
            warnings_objects.remove(self)
        else:
            Card().make(self)


class Card:
    def __init__(self):
        card_objects.append(self)
        self.frame = tkinter.Frame(root, **dimensions, bg="#CDCDCD")
        self.frame.pack(fill='both', expand=True)

        self.primary = None
        self.headline_label = None
        self.primary_info_frame = None
        self.certainty_frame = None
        self.delta_frame = None
        self.severity_frame = None
        self.certainty_label = None
        self.certainty_text = None
        self.delta_label = None
        self.delta_text = None
        self.severity_label = None
        self.severity_text = None
        self.secondary = None
        self.dates_frame = None
        self.issued_text = None
        self.issued_time = None
        self.expiry_text = None
        self.expiry_time = None
        self.desclabel = None

    def make(self, data: WarningInfo):

        self.primary = tkinter.Frame(self.frame, background=data.level, **dimensions)
        self.primary.pack(fill='both', side='left')
        self.primary.bind('<Button-1>', self.display_extra)

        self.headline_label = tkinter.Label(self.primary, data.style, text=data.headline, justify='center',
                                            wraplength=500, font=('Helvetica', 11, 'bold'), width=59)
        self.headline_label.pack(side='top')

        self.primary_info_frame = tkinter.Frame(self.primary, background=data.level)
        self.certainty_frame = tkinter.Frame(self.primary_info_frame)
        self.delta_frame = tkinter.Frame(self.primary_info_frame)
        self.severity_frame = tkinter.Frame(self.primary_info_frame)
        self.primary_info_frame.pack(side='left')
        self.certainty_frame.pack(side='left')
        self.delta_frame.pack(side='left')
        self.severity_frame.pack(side='left')

        self.certainty_label = tkinter.Label(self.certainty_frame, data.style, text="Certainty: ")
        self.certainty_text = tkinter.Label(self.certainty_frame, data.style, font=('Helvetica', 9, 'bold'),
                                            text=data.certainty)
        self.certainty_label.pack(side='left')
        self.certainty_text.pack(side='left')

        self.delta_label = tkinter.Label(self.delta_frame, data.style, text=data.delta_msg)
        self.delta_text = tkinter.Label(self.delta_frame, data.style, text=data.delta,
                                        font=('Helvetica', 9, 'bold'))
        self.delta_label.pack(side='left')
        self.delta_text.pack(side='left')
        self.severity_label = tkinter.Label(self.severity_frame, text="Severity: ")
        self.severity_text = tkinter.Label(self.severity_frame, data.style, font=('Helvetica', 9, 'bold'),
                                           text=data.severity)

        self.headline_label.bind('<Button-1>', self.display_extra)

        # secondary
        self.secondary = tkinter.Frame(self.frame, **dimensions, relief=tkinter.SUNKEN, borderwidth=4)

        self.dates_frame = tkinter.Frame(self.secondary)
        self.issued_text = tkinter.Label(self.dates_frame, text='Issued: ')
        self.issued_time = tkinter.Label(self.dates_frame, text=friendly_time(data.issued),
                                         font=('Helvetica', 9, 'bold'))
        self.expiry_text = tkinter.Label(self.dates_frame, text='Expiry: ')
        self.expiry_time = tkinter.Label(self.dates_frame, text=friendly_time(data.expiry),
                                         font=('Helvetica', 9, 'bold'))

        self.dates_frame.pack(side='top')
        self.issued_text.pack(side='left')
        self.issued_time.pack(side='left')
        self.expiry_text.pack(side='left')
        self.expiry_time.pack(side='left')

        self.desclabel = tkinter.Label(self.secondary, text=self.format_description(data),

                                       height=4)
        self.desclabel.pack(side='bottom')
        self.secondary.visible = False

    def delete(self):
        self.frame.destroy()
        card_objects.remove(self)
        # TODO remove object from warnings_objects list

    def display_extra(self, _):
        """toggle secondary panel visibility"""

        def forget_old():
            self.certainty_frame.pack_forget()
            self.delta_frame.pack_forget()

        if self.secondary.visible is False:
            self.secondary.pack(fill='both', side='right', expand=True)

            forget_old()
            self.certainty_frame.pack(side='top', anchor='w')
            self.delta_frame.pack(side='top', anchor='w')
        else:
            self.secondary.pack_forget()

            forget_old()
            self.certainty_frame.pack(side='left')
            self.delta_frame.pack(side='left')

        self.secondary.visible = not self.secondary.visible

    def format_description(self, warn: WarningInfo):
        return textwrap.TextWrapper(max_lines=3).fill(text=warn.description)

    def create_non_warning(self, message, style=None):
        if style is None:
            style = style_no_warning
        self.frame.configure(height=10, width=60)
        self.headline_label = tkinter.Label(self.frame, style, text=message)
        self.headline_label.pack(fill='both', expand=True)


def rdel():
    """recursively delete all Warning_info objects"""
    for obj in card_objects:
        obj.frame.destroy()
    card_objects.clear()


def download_json(selected_region):
    if selected_region == "Demo":
        with open(getcwd() + '\\' + "demo_weather_warning.json", "r") as f:
            response = json.loads(f.read())
    else:
        if selected_region in REGION_CODES:
            areacode = REGION_CODES[selected_region]
        else:
            areacode = MARINE_CODES[selected_region]
            Card().create_non_warning(message="Feature Unsupported!")
            return
        met_url = f"https://www.met.ie/Open_Data/json/warning_{areacode}.json"
        try:
            response = requests.get(met_url).json()  # downloads latest json from api with given region
        except requests.exceptions.ConnectionError:
            tkinter.messagebox.showerror(title='Warning_info',
                                         message='Could not reach Met Eireann API. Please try again later')
            return
    return response


def friendly_time(date_input):
    """format time to be displayed on warning card
    Example: 2021-02-21T14:45:06-00:00 -> Feb 21 At 14:45"""
    date_object = datetime.strptime(date_input, '%Y-%m-%dT%H:%M:%S%z')
    return date_object.strftime('%b %d At %H:%M')


def update_time(obj):
    """For every warning object, compare current time to expiration time to check if warning is expired.
    If expired, return 'expired' and delete the warning card. Otherwise check if warning is in place or not in place yet
    and assign time delta and correct label to the object attribute"""
    t_format = '%Y-%m-%dT%H:%M:%S'
    current_time = datetime.now()

    onset_time = datetime.strptime(obj.onset[:-6], t_format)
    expiry_time = datetime.strptime(obj.expiry[:-6], t_format)

    if current_time > onset_time and current_time > expiry_time:
        # we are past both the onset and the expiration
        # destroy tkinter warning widgets and remove Warnings object.

        obj.delete()
        return "expired"

    elif current_time > onset_time:
        # warning is in place but not expired
        # display time until expiration
        obj.delta = ':'.join(str(expiry_time - current_time).split(':')[:2])
        obj.delta_msg = 'Time until expiration: '

    else:
        # warning is not in place yet
        # display time until warning onset
        obj.delta = ':'.join(str(onset_time - current_time).split(':')[:2])
        obj.delta_msg = 'Time until onset: '


def flash_red():
    """Make the headline of warning card flash red and white"""
    for obj in card_objects:
        try:
            if obj.level == "Red":
                if obj.headline_label["background"] != 'white':
                    obj.headline_label.configure(backgroun='white')
                else:
                    obj.headline_label.configure(background='red')
        except AttributeError:
            pass


def refresh(_=None):
    """Called when refresh button is pressed. Deletes all card objects and displays new ones"""
    rdel()

    selected_region = combox.get()  # gets the selected region from combo box
    response = download_json(selected_region)
    if response is None:
        return None

    # if there are no warnings, display it as a message
    if len(response) == 0:
        Card().create_non_warning(message="There are no warnings for the selected region")
    else:
        create_object(response, selected_region)


def create_object(response, selected_region):
    """creates a WarningInfo class object for all warnings that match chosen location"""

    for dict_entry in response:
        if selected_region == 'Demo' or selected_region == "All counties":
            WarningInfo(dict_entry)
        elif REGION_CODES[selected_region] in dict_entry['regions']:
            print(REGION_CODES[selected_region])
            WarningInfo(dict_entry)


def update_combox_val():
    """Changes between marine zones and counties to be displayed on the combo box widget"""
    sea_val = sea_box_val.get()
    if sea_val == 1:
        combox.configure(values=[i for i in MARINE_CODES.keys()])
        location_label.configure(text="Select Marine Zone: ")
    else:
        combox.configure(values=[i for i in REGION_CODES.keys()])
        location_label.configure(text="Select County: ")


def info_action():
    info_window = tkinter.Toplevel()
    info_window.title('Information')
    info_window.iconbitmap("Assets/MetEireann logo-02.ico")
    info_text = tkinter.Label(info_window, justify='left', wraplength=666)
    with open(getcwd() + '\\' + "info.txt", "r") as text:
        info_text['text'] = text.read()
    info_text.pack()
    info_btn['state'] = 'disabled'
    info_btn['relief'] = 'sunken'

    def info_close():
        info_btn['state'] = 'normal'
        info_btn['relief'] = 'raised'
        info_window.destroy()

    info_window.protocol("WM_DELETE_WINDOW", info_close)


# GUI
root = tkinter.Tk()
root.resizable(False, False)
root.title("Met Eireann Status")
root.iconbitmap("Assets/MetEireann logo-02.ico")

options_frame = tkinter.LabelFrame(root, relief=tkinter.RAISED, borderwidth=5, bg='white')
options_frame.pack(fill='x')

location_label = tkinter.Label(options_frame, text="Select County:", width=14)
location_label.grid(column=0, row=0, padx=5, pady=4)

combox = tkinter.ttk.Combobox(options_frame, values=[i for i in REGION_CODES.keys()], state="readonly")
combox.current(27)  # sets default for the combo box
combox.grid(column=1, row=0, padx=5, pady=4)

refresh_button = tkinter.Button(options_frame, text='Refresh', command=refresh)
refresh_button.grid(column=3, row=0, padx=4, pady=5)
root.bind('<Return>', refresh)

sea_box_val = tkinter.IntVar()
sea_check_box = tkinter.Checkbutton(options_frame, variable=sea_box_val, text="Search Marine Warnings",
                                    command=update_combox_val)
sea_check_box.grid(column=4, row=0)

info_btn = tkinter.Button(options_frame, bitmap="info", width=25, command=info_action)
info_btn.grid(column=6, row=0, padx=4)


def tick():
    root.after(1000, tick)
    flash_red()


tick()
root.mainloop()

# todo add all information to be displayed
# todo prevent duplicate warnings
# todo auto launch at startup and check for warnings in background process
# todo implement timer to prevent spamming requests
# todo display time and date on options bar
# todo edit info.txt to explain warning types
# todo place icons for warning type
# todo create a new tab showing a map
# todo give region by province instead of county
# todo daily report
# todo fix blank card showing when warning is expired
