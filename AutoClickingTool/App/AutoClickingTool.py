import os
import sys
import threading
import time
from datetime import datetime as dt
from tkinter import Toplevel
from tkinter.ttk import Combobox
import keyboard
from PIL import Image, ImageTk
import tkinter as tk
from AutoClicker.assets.Property import Property
from pynput.mouse import Controller, Button
from pynput.keyboard import Listener, KeyCode


class AutoClickingTool(threading.Thread):

    def __init__(self):
        super(AutoClickingTool, self).__init__()

        # Variables
        now = dt.now()
        print(f"\033[36m[{now.strftime("%d.%m.%Y")} - {now.strftime("%H")}:{now.strftime("%M")}:{now.strftime("%S")}]: "
              f"\033[0mInitiating Variables...")
        self.root = tk.Tk()
        self.__status = 0
        self.keys_pressed = 0
        self.started_script_count = 0
        self.clicks_count = 0
        self.start_stop_key = KeyCode(char=Property().get_property("start_stop_key"))
        self.delay = float(Property().get_property("click_delay"))
        self.sleep = float(Property().get_property("sleep"))
        self.button = Button.left
        if str(Property().get_property("button_to_press")) == "left":
            self.button = Button.left
        elif str(Property().get_property("button_to_press")) == "right":
            self.button = Button.right
        self.changing = False
        self.running = False
        self.script_running = True
        self.end = False
        self.click_thread = self
        self.click_delay = self.delay
        self.mouse = Controller()
        self.listener = Listener(on_press=self.on_press)

        # Positioning + Size
        now = dt.now()
        print(f"\033[36m[{now.strftime("%d.%m.%Y")} - {now.strftime("%H")}:{now.strftime("%M")}:{now.strftime("%S")}]: "
              f"\033[0mSetting size and positioning...")
        self.root.minsize(275, 125)
        self.root.maxsize(275, 125)
        self.window_positioning()

        # Start click thread
        now = dt.now()
        print(f"\033[36m[{now.strftime("%d.%m.%Y")} - {now.strftime("%H")}:{now.strftime("%M")}:{now.strftime("%S")}]: "
              f"\033[0mStarting click thread...")
        self.click_thread.start()

        self.root.title("Auto-Clicking Tool")
        ico = Image.open(Property().get_property("icon_path"))
        photo = ImageTk.PhotoImage(ico)
        # noinspection PyTypeChecker
        self.root.wm_iconphoto(False, photo)

        # Key Press Events
        now = dt.now()
        print(f"\033[36m[{now.strftime("%d.%m.%Y")} - {now.strftime("%H")}:{now.strftime("%M")}:{now.strftime("%S")}]: "
              f"\033[0mBinding key events...")
        print(f'\033[35m\033[01m[INFO/ KEY-BIND]:\033[0m \033[31m\033[04mRead\033[0m \033[31mKey-Bind:\033[0m '
              f'"\033[95m{Property().get_property("start_stop_key")}\033[0m" from "\033[94mconf.ini\033[0m".')
        self.key_press = keyboard.on_press(self.pressed_button)

        # Menubar
        now = dt.now()
        print(f"\033[36m[{now.strftime("%d.%m.%Y")} - {now.strftime("%H")}:{now.strftime("%M")}:{now.strftime("%S")}]: "
              f"\033[0mCreating menubar...")
        self.__menu = tk.Menu(self.root)
        options_menu = tk.Menu(self.__menu, tearoff=0)
        options_menu.add_command(label="Values", command=self.change_values)
        options_menu.add_command(label="Reset", command=self.reset_values)
        options_menu.add_command(label="Key Binds", command=self.key_binds)
        options_menu.add_separator()
        options_menu.add_command(label="Exit", command=self.update_gui_off)
        self.__menu.add_cascade(label="Options", menu=options_menu)

        about_menu = tk.Menu(self.__menu, tearoff=0)
        about_menu.add_command(label="About", command=self.open_about)
        self.__menu.add_cascade(label="About", menu=about_menu)
        self.root.config(menu=self.__menu)

        now = dt.now()
        print(f"\033[36m[{now.strftime("%d.%m.%Y")} - {now.strftime("%H")}:{now.strftime("%M")}:{now.strftime("%S")}]: "
              f"\033[0mCreating labels...")
        print("\033[1m=================================================================\n\033[0m")
        print("\033[91m\033[01m[Logging]\033[0m\n")
        self.__status_label = tk.Label(self.root, text="Off", bg="#FA8072", fg="white", font=("Arial", 13))
        self.__status_label.pack(fill="both", expand=True)

        # Keep the window always on top
        self.root.attributes("-topmost", True)

        # Protocol
        self.root.protocol(name="WM_DELETE_WINDOW", func=self.update_gui_off)

    def start_clicking(self):
        self.running = True

    def stop_clicking(self):
        self.running = False

    # script runtime
    def run(self):
        while self.script_running:
            while self.running:
                self.mouse.click(self.button)
                self.clicks_count += 1
                time.sleep(self.delay)
            time.sleep(self.sleep)

    def window_positioning(self):
        if os.path.isfile("../assets/conf.ini") and Property().get_property("geometry"):
            now = dt.now()
            print(f"\033[36m[{now.strftime("%d.%m.%Y")} - {now.strftime("%H")}:{now.strftime("%M")}:{now.strftime("%S")}]: "
                  f"\033[0mReading window position...")
            self.root.geometry(Property().get_property("geometry"))
            msg = (f"\033[95m{Property().get_property("geometry")[0:7]}\033[0m with offset: x = "
                   f"\033[95m{Property().get_property("geometry")[8:11]}\033[0m + y = "
                   f"\033[95m{Property().get_property("geometry")[12:]}")
            print(f"\033[35m\033[01m[INFO/ SUCCESSFUL READ]:\033[0m \033[31m\033[04mRead\033[0m \033[31mMain-Window Geometry: {msg}\033[0m.")
            if str(self.root.geometry())[-7:] == Property().get_property("geometry")[-7:]:
                print(f"\033[35m\033[01m[INFO/ PLACEMENT]: \033[0mWindow has been positioned.")
            else:
                self.root.after(250)
                print(f"\033[31m\033[01m[ERROR/ PLACEMENT]: \033[0mWindow \033[04mcould not\033[0m be positioned.")
        else:
            now = dt.now()
            print(f"\033[36m[{now.strftime("%d.%m.%Y")} - {now.strftime("%H")}:{now.strftime("%M")}:{now.strftime("%S")}]: "
                  f"\033[0mCreating window position...")
            #self.eval('tk::PlaceWindow . center')
            self.root.geometry('275x125+1600+40')
            geo = "275x125+1600+40"
            msg = f"\033[95m{geo[0:7]}\033[0m with offset: x = \033[95m{geo[8:11]}\033[0m + y = \033[95m{geo[12:]}"
            print(f"\033[35m\033[01m[INFO/ NEW ENTRY]:\033[0m \033[31m\033[04mCreated\033[0m \033[31mMain-Window Geometry: {msg}\033[0m.")
            if str(self.root.geometry())[-7:] == Property().get_property("geometry")[-7:]:
                print(f"\033[35m\033[01m[INFO/ PLACEMENT]: \033[0mWindow has been positioned.")
            else:
                self.root.after(250)
                print(f"\033[31m\033[01m[ERROR/ PLACEMENT]: \033[0mWindow \033[04mcould not\033[0m be positioned.")

    def on_close(self):
        print("\033[1m=================================================================\n\033[0m")
        print("\033[91m\033[01m[Finalizing]\033[0m\n")
        print("\033[93mClosing script...\033[0m")
        self.stop_clicking()
        self.script_running = False
        Property().set_property("geometry", str(self.root.geometry()))
        print(f"\033[35m\033[1m[INFO]:\033[0m script has been started "
              f"\033[95m{round(self.started_script_count / 2)}\033[0m times.\033[0m")
        print(f"\033[35m\033[1m[INFO]:\033[0m \033[95m{self.keys_pressed}"
              f"\033[0m Key-presses have been made.\033[0m")
        print(f"\033[35m\033[1m[INFO]:\033[0m The script has clicked \033[95m{self.clicks_count}"
              f"\033[0m times.\033[0m")
        print("\n\033[35m\033[01m[INFO/ USER-ACTION]:\033[0m \033[31mWindow has closed successfully.\033[0m")

    # Controls UI of the script
    def on_press(self, key):
        # FIXME: Quits the script and closes the window (NOT WORKING >>> MEMORY LEAK) [ctrl + q]
        #if str(key) == f"'{chr(92)}x11'":
        #    self.click_thread.stop_clicking()
        #    self.update_gui_off()
        if key == self.start_stop_key and not self.changing:
            self.__status = self.__status % 2 + 1
            self.started_script_count += 1
            if self.__status == 1:
                # Start script
                print("\033[92m>>> Starting script...\033[0m")
                self.click_thread.start_clicking()
            else:
                # Stop script
                print("\033[94m>>> Pausing script...\033[0m")
                self.click_thread.stop_clicking()
            self.update_gui_on_and_pause()

    # Key-press counter + logging
    def pressed_button(self, event):
        self.keys_pressed += 1
        now = dt.now()
        print(f"\033[36m[{now.strftime("%d.%m.%Y")} - {now.strftime("%H")}:{now.strftime("%M")}:"
              f"{now.strftime("%S")}]: \033[4mPressed Button '{event.name}'\033[0m")

    def update_gui_on_and_pause(self):
        # If not changing key-binds or values
        if not self.changing:
            if self.__status == 1:
                self.__status_label.config(text="Running...", bg="#66CDAA")  # Medium green
            else:
                self.__status_label.config(text="Paused...", bg="#FA8072")  # Medium red
            self.__status_label.update()

    def update_gui_off(self):
        self.__status = 3
        self.end = True
        self.script_running = False
        if self.__status == 3:
            self.root.after(50)
            self.__status_label.config(text="Shutting Down...", bg="#FFB152") # Medium yellow
            self.__status_label.update()
            self.root.after(1000)
        self.menu_close()

    def change_values(self):
        # Prevent script from running, to not cause unwanted clicking
        self.changing = True
        self.running = False

        now = dt.now()
        print(f'\033[36m[{now.strftime("%d.%m.%Y")} - {now.strftime("%H")}:{now.strftime("%M")}:{now.strftime("%S")}]: '
              f'\033[0mOpening "\033[93mValue-Changing\033[0m"-Window...')
        value_window = Toplevel(self.root)
        value_window.wait_visibility()
        value_window.title("Values")
        value_window.geometry("320x200")

        value_window.resizable(False, False)

        ico = Image.open(Property().get_property("icon_path"))
        photo = ImageTk.PhotoImage(ico)
        # noinspection PyTypeChecker
        value_window.wm_iconphoto(False, photo)

        value_window.attributes("-topmost", True)
        x = self.root.winfo_x() + self.root.winfo_width() // 2 - value_window.winfo_width() // 2
        y = self.root.winfo_y() + self.root.winfo_height() // 2 - value_window.winfo_height() // 2
        value_window.geometry(f"+{x}+{y}")
        value_window.protocol(name="WM_DELETE_WINDOW",
                              func=lambda: [self.on_toplevel_close("Value"), value_window.destroy()])
        value_window.grab_set()

        # Grid Configuration
        value_window.rowconfigure(1, weight=1)
        value_window.columnconfigure(1, weight=1)

        # Variables
        delay_var = tk.StringVar()
        sleep_var = tk.StringVar()
        mouse_var = tk.StringVar()

        # Delay box
        delay_text = tk.Label(value_window, text="Delay:", anchor='w', padx=8)
        delay_entry = tk.Entry(value_window, textvariable=delay_var)

        # Sleep box
        sleep_text = tk.Label(value_window, text="Sleep:", anchor='w', padx=8)
        sleep_entry = tk.Entry(value_window, textvariable=sleep_var)

        # Mouse button box
        choices = ["Left", "Right"]
        placeholder_mouse = "Select Mouse Button"
        mouse_text = tk.Label(value_window, text="Mouse Button:", anchor='w', padx=8)
        mouse_entry = Combobox(value_window, textvariable=mouse_var, values=choices, state="readonly")
        mouse_var.set("Left")

        # Placeholder functions for Delay and Sleep fields
        def add_placeholder(entry, placeholder):
            if entry.get() == '':
                entry.insert(0, placeholder)
                entry.config(fg='grey')

        def remove_placeholder(entry, placeholder):
            if entry.get() == placeholder:
                entry.delete(0, tk.END)
                entry.config(fg='black')

        # Bind focus events to remove placeholder and reset if no value selected
        def remove_combobox_placeholder(event):
            if mouse_entry.get() == placeholder_mouse and event:
                mouse_entry.set('')
                mouse_entry.config(foreground='black')

        def add_combobox_placeholder(event):
            if mouse_entry.get() == '' and event:
                mouse_entry.set(placeholder_mouse)
                mouse_entry.config(foreground='grey')

        # Set the placeholder color to grey initially
        mouse_entry.config(foreground='grey')

        # Confirm Button
        confirm_button = tk.Button(value_window, text="Confirm",
                                   command=lambda: [self.on_confirm(delay_var.get(), sleep_var.get(),
                                                                    mouse_var.get()), value_window.destroy()],
                                   height=1, width=35)

        # Padding for layout
        padding = {'padx': 20, 'pady': 10}

        # Grid layout for all widgets with spacing
        delay_text.grid(row=0, column=0, sticky='w', **padding)
        delay_entry.grid(row=0, column=1, **padding)

        sleep_text.grid(row=1, column=0, sticky='w', **padding)
        sleep_entry.grid(row=1, column=1, **padding)

        # Placeholder text
        placeholder_delay = "in seconds"
        placeholder_sleep = "in seconds"

        # Set placeholders
        add_placeholder(delay_entry, placeholder_delay)
        add_placeholder(sleep_entry, placeholder_sleep)

        # Bind events for placeholders
        delay_entry.bind("<FocusIn>", lambda event: remove_placeholder(delay_entry, placeholder_delay))
        delay_entry.bind("<FocusOut>", lambda event: add_placeholder(delay_entry, placeholder_delay))

        sleep_entry.bind("<FocusIn>", lambda event: remove_placeholder(sleep_entry, placeholder_sleep))
        sleep_entry.bind("<FocusOut>", lambda event: add_placeholder(sleep_entry, placeholder_sleep))

        mouse_entry.bind("<FocusIn>", remove_combobox_placeholder)
        mouse_entry.bind("<FocusOut>", add_combobox_placeholder)

        mouse_text.grid(row=2, column=0, sticky='w', **padding)
        mouse_entry.grid(row=2, column=1, **padding)

        confirm_button.grid(row=3, columnspan=2, pady=20)

    def on_confirm(self, delay, sleep, button):
        if str(delay) == "in seconds" or str(delay) == "":
            delay = "-"
        if str(sleep) == "in seconds" or str(sleep) == "":
            sleep = "-"
        try:
            if type(float(delay)) is float:
                Property().set_property("click_delay", float(delay))
                print(f"\033[35m\033[1m[INFO/ VALUE-CHANGE]:\033[0m \033[95m{delay}"
                      f"\033[0m is now the new value of the clicking delay.\033[0m")
        except ValueError:
            print(f'\033[91m\033[01m[WARNING/ ERROR]:\033[0m Could not change value of "\033[94mDelay\033[0m" '
                  f'(\033[95m{delay}\033[0m), due to wrong data type.')
        try:
            if type(float(sleep)) is float:
                Property().set_property("sleep", float(sleep))
                print(f"\033[35m\033[1m[INFO/ VALUE-CHANGE]:\033[0m \033[95m{sleep}"
                      f"\033[0m is now the new value of the script sleep-delay.\033[0m")
        except ValueError:
            print(f'\033[91m\033[01m[WARNING/ ERROR]:\033[0m Could not change value of "\033[94mSleep\033[0m" '
                  f'(\033[95m{sleep}\033[0m), due to wrong data type.')
        try:
            if str(button).upper() == "LEFT":
                Property().set_property("button_to_press", "left")
                print(f"\033[35m\033[1m[INFO/ VALUE-CHANGE]:\033[0m \033[95mLEFT"
                      f"\033[0m is now the new Button which is being pressed.\033[0m")
            elif str(button).upper() == "RIGHT":
                Property().set_property("button_to_press", "right")
                print(f"\033[35m\033[1m[INFO/ VALUE-CHANGE]:\033[0m \033[95mRIGHT"
                      f"\033[0m is now the new Button which is being pressed.\033[0m")
            else:
                Property().set_property("button_to_press", "left")
                print(f"\033[35m\033[1m[INFO/ VALUE-CHANGE]:\033[0m \033[95mLEFT"
                      f"\033[0m is now the new Button which is being pressed.\033[0m")
        except ValueError:
            print(f'\033[91m\033[01m[WARNING/ ERROR]:\033[0m Could not change value of "\033[94mButton\033[0m" '
                  f'(\033[95m{button}\033[0m), due to wrong data type.')
        self.update_script()

    def update_script(self):
        # Check New Button Press
        if str(Property().get_property("button_to_press")) == "left":
            self.button = Button.left
        elif str(Property().get_property("button_to_press")) == "right":
            self.button = Button.right

        # Check New Sleep
        self.sleep = float(Property().get_property("sleep"))

        # Check New Delay
        self.delay = float(Property().get_property("click_delay"))

        # Enable script functionality
        self.changing = False
        self.running = True
        self.click_thread.stop_clicking()

    def reset_values(self):
        # Button
        Property().set_property("button_to_press", "left")
        print(f"\033[35m\033[1m[INFO/ VALUE-CHANGE]:\033[0m \033[95mLEFT"
              f"\033[0m is now the new Button which is being pressed.\033[0m")

        # Delay
        Property().set_property("click_delay", 0.01)
        print(f"\033[35m\033[1m[INFO/ VALUE-CHANGE]:\033[0m \033[95m{0.01}"
              f"\033[0m is now the new value of the clicking delay.\033[0m")

        # Sleep
        Property().set_property("sleep", 0.20)
        print(f"\033[35m\033[1m[INFO/ VALUE-CHANGE]:\033[0m \033[95m{0.20}"
              f"\033[0m is now the new value of the script sleep-delay.\033[0m")
        self.update_script()

    def key_binds(self):
        # Prevent script from running, to not cause unwanted clicking
        self.changing = True
        self.running = False

        now = dt.now()
        print(f'\033[36m[{now.strftime("%d.%m.%Y")} - {now.strftime("%H")}:{now.strftime("%M")}:{now.strftime("%S")}]: '
              f'\033[0mOpening "\033[93mKey-Bind\033[0m"-Label...')
        self.__status_label.config(text='Press any button,\nto assign the new\n"Start-Stop-Key"', bg="#1D004D")
        self.__status_label.update()
        key_bind_label = tk.Label()
        key = None
        while not key:
            key = keyboard.read_key()
        if str(key) != Property().get_property("start_stop_key"):
            key_bind_label = tk.Label(self.root, text=f'"{key}"',
                  bg="#1D004D", fg="white", font=("Arial", 13))
            key_bind_label.pack(fill="both", expand=True)
            self.__status_label.config(text='Press the button again,\nto assign the new key-bind.', bg="#1D004D")
            self.__status_label.update()
            confirm_key = None
            while not confirm_key:
                confirm_key = keyboard.read_key()
            if confirm_key == key:
                Property().set_property("start_stop_key", str(key))
                key_bind_label.destroy()
                self.__status_label.config(text='Success!', bg="#1D004D")
                self.__status_label.update()
                self.start_stop_key = KeyCode(char=Property().get_property("start_stop_key"))
                print(f'\033[35m\033[01m[INFO/ KEY-BIND/ USER-ACTION]:\033[0m \033[31m\033[04mChanged\033[0m '
                      f'\033[31mKey-Bind to: \033[0m"\033[95m{Property().get_property("start_stop_key")}\033[0m".')
        else:
            print(f'\033[35m\033[01m[INFO/ KEY-BIND]:\033[0m \033[31m\033[04mDid not change\033[0m \033[31mKey-Bind.')
            self.__status = 0
            self.changing = False
            self.update_gui_on_and_pause()
        key_bind_label.destroy()

        # Reactivate script and stop it from instantly clicking
        self.changing = False
        self.running = True
        self.click_thread.stop_clicking()

    def menu_close(self):
        self.__status = 3
        self.end = True
        self.root.bind("<Configure>", self.on_close())
        self.root.after(1000)
        self.root.destroy()
        self.listener.stop()
        sys.exit(0)

    def open_about(self):
        now = dt.now()
        print(f'\033[36m[{now.strftime("%d.%m.%Y")} - {now.strftime("%H")}:{now.strftime("%M")}:{now.strftime("%S")}]: '
              f'\033[0mOpening "\033[93mAbout\033[0m"-Window...')
        about_window = Toplevel(self.root)
        about_window.wait_visibility()
        about_window.title("About")
        about_window.geometry("210x80")
        about_window.resizable(False, False)
        window_label = tk.Label(about_window, text="Auto-Clicking Tool\nby: Xaro\nv1.0.2",
              bg="#1D004D", fg="white", font=("Arial", 13))
        window_label.pack(fill="both", expand=True)
        ico = Image.open(Property().get_property("icon_path"))
        photo = ImageTk.PhotoImage(ico)
        # noinspection PyTypeChecker
        about_window.wm_iconphoto(False, photo)
        about_window.attributes("-topmost", True)
        x = self.root.winfo_x() + self.root.winfo_width() // 2 - about_window.winfo_width() // 2
        y = self.root.winfo_y() + self.root.winfo_height() // 2 - about_window.winfo_height() // 2
        about_window.geometry(f"+{x}+{y}")
        about_window.protocol(name="WM_DELETE_WINDOW",
                              func=lambda: [self.on_toplevel_close("About"), about_window.destroy()])
        about_window.grab_set()

    @staticmethod
    def on_toplevel_close(window_name: str) -> bool:
        now = dt.now()
        print(f'\033[36m[{now.strftime("%d.%m.%Y")} - {now.strftime("%H")}:{now.strftime("%M")}:{now.strftime("%S")}]: '
              f'\033[0mClosing "\033[93m{window_name}\033[0m"-Window...')
        return True

    def exit_script(self):
        self.stop_clicking()
        self.script_running = False

    def start_listener(self):
        # Start main loop in the main thread
        with self.listener:
            if not self.end:
                self.root.mainloop()
                self.listener.join()
            else:
                self.listener.stop()
                sys.exit()


os.system("")
print("\033[91m\033[01m[Initializing]\033[0m\n")
now = dt.now()
print(f"\033[36m[{now.strftime("%d.%m.%Y")} - {now.strftime("%H")}:{now.strftime("%M")}:{now.strftime("%S")}]: "
      f"\033[0mStarting App...")
app = AutoClickingTool()
while True:
    app.start_listener()
