import tkinter
import tkinter.messagebox
import customtkinter
from tkinter import filedialog
from main_function import *
import time

customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"
version = "1.0.0"



class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("Mail Spam Filter")
        self.geometry(f"{1100}x{580}")
        #lock the window size
        self.resizable(False, False)


        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Mail Spam Filter", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        
        #create sidebar button 1 for loading dictionary
        #need to using lambda to pass argument to function (it will be called when button is clicked)
        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, command=lambda: self.browse_file(btn_type="Dictionary"))
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        
        #create sidebar button 2 for loading banned words
        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, command=lambda: self.browse_file(btn_type="Banned Words"))
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)
        
        #create sidebar button 3 for loading mail
        self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame, command=lambda: self.browse_file(btn_type="Mail"))
        self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=10)

        # create label and optionmenu for appearance mode 
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Dark","Light", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))

        #create a button for debug mode
        self.debug_button = customtkinter.CTkButton(self.sidebar_frame, text="Debug", command=lambda: self.debug_mode())
        self.debug_button.grid(row=7, column=0, padx=20, pady=(10, 10))

        #create a digial clock
        self.clock = customtkinter.CTkLabel(self.sidebar_frame, text="00:00", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.clock.grid(row=9, column=0, padx=20, pady=(10, 20))

        #update the clock every 1 second
        self.update_clock()



        # create main entry and button
        self.entry = customtkinter.CTkEntry(self, placeholder_text="Input mail content here...")
        self.entry.grid(row=3, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")
        
        self.add_messages = customtkinter.CTkButton(master=self, fg_color="transparent", border_width=2, 
                                                     text_color=("gray10", "#DCE4EE"),
                                                     text="Add Messages", 
                                                     command=lambda: self.add_messages_to_box())
        self.add_messages.grid(row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")


        self.main_button_2 = customtkinter.CTkButton(master=self, border_width=2, 
                                                     text="Check Messages", 
                                                     command=lambda: self.check_messages())
        self.main_button_2.grid(row=1, column=3, padx=(20, 20), pady=(50, 10), sticky="nsew")


        # create textbox
        self.textbox = customtkinter.CTkTextbox(self, width=250)
        self.textbox.grid(row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")


        # create slider and progressbar frame
        self.slider_progressbar_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        self.slider_progressbar_frame.grid(row=1, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.slider_progressbar_frame.grid_columnconfigure(0, weight=1)

        self.tabview = customtkinter.CTkTabview(self.slider_progressbar_frame)
        self.tabview.grid(row=0, column=0, pady=(10, 10), sticky="ew")
        self.tabview.add("Messages")
        self.tabview.add("Dictionary")
        self.tabview.add("Banned Words")

        # Add a read-only textbox to display log in Messages
        self.messenges_textbox = customtkinter.CTkTextbox(self.tabview.tab("Messages"))
        self.messenges_textbox.grid(row=0, column=0, sticky="nsew")
        #make the grid full width column
        self.tabview.tab("Messages").grid_columnconfigure(0, weight=1)

        # Add a read-only textbox to display dictionary in Dictionary
        self.dictionary_textbox = customtkinter.CTkTextbox(self.tabview.tab("Dictionary"))
        self.dictionary_textbox.grid(row=0, column=0, sticky="nsew")
        #make the grid full width column
        self.tabview.tab("Dictionary").grid_columnconfigure(0, weight=1)

        # Add a read-only textbox to display banned words in Banned Words
        self.banned_words_textbox = customtkinter.CTkTextbox(self.tabview.tab("Banned Words"))
        self.banned_words_textbox.grid(row=0, column=0, sticky="nsew")
        #make the grid full width column
        self.tabview.tab("Banned Words").grid_columnconfigure(0, weight=1)



        # create checkbox and switch frame
        self.checkbox_slider_frame = customtkinter.CTkFrame(self)
        self.checkbox_slider_frame.grid(row=0, column=3, padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.label_checkbox_group = customtkinter.CTkLabel(master=self.checkbox_slider_frame, text="Status:")
        self.label_checkbox_group.grid(row=0, column=0, columnspan=1, padx=10, pady=10, sticky="")
        self.dict_checkbox = customtkinter.CTkCheckBox(master=self.checkbox_slider_frame)
        self.dict_checkbox.grid(row=1, column=0, pady=(20, 0), padx=20, sticky="n")
        self.ban_checkbox = customtkinter.CTkCheckBox(master=self.checkbox_slider_frame)
        self.ban_checkbox.grid(row=2, column=0, pady=(20, 0), padx=20, sticky="n")

        # set default values
        self.sidebar_button_1.configure(text="Load Dictionary")
        self.sidebar_button_2.configure(text="Load Bannded Words")
        self.sidebar_button_3.configure(text="Load Mail")
        #name the checkbox
        self.dict_checkbox.configure(text="Dictionary",state="disabled")
        self.ban_checkbox.configure(text="Ban Words",state="disabled")
        #name the tab
        self.dictionary_textbox.insert("0.0", "Dictionary:\n\n")
        self.banned_words_textbox.insert("0.0", "Banned Words:\n\n")
        self.messenges_textbox.insert("0.0", "Status Messages:\n\n")
        #disable the textbox
        self.messenges_textbox.configure(state="disabled")
        self.dictionary_textbox.configure(state="disabled")
        self.banned_words_textbox.configure(state="disabled")
        self.textbox.configure(state="disabled")

        #initialize the variables
        self.dictionary = None
        self.banned_words = None
        self.messages = None
        self._debug_running = False
        self.debug_time = None

    
    def update_clock(self):
        current_time = time.strftime("%I:%M:%S %p")  # Use "%I" for 12-hour format, "%p" for AM/PM
        self.clock.configure(text=current_time)
        self.after(1000, self.update_clock)







    #debug mode let you replace the clock with a select box HH:MM AM/PM
    def debug_mode(self):
        # Toggle the debug mode state on button click
        self._debug_running = not self._debug_running


        if self._debug_running:
            #remove the clock
            self.clock.grid_forget()
            #create a input entry
            self.debug_time = customtkinter.CTkEntry(self.sidebar_frame, placeholder_text="HH:MM")
            self.debug_time.grid(row=9, column=0, padx=20, pady=(10, 20))
            #turn on the text box
            self.textbox.configure(state="normal")

        else:
            #remove the combobox
            self.debug_time.grid_forget()
            #add the clock back
            self.clock.grid(row=9, column=0, padx=20, pady=(10, 20))
            #turn off the text box
            self.textbox.configure(state="disabled")



    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)



    def add_messages_to_box(self):
        #get the time from the debug_time if debug mode is on
        if self._debug_running:
            send_time = self.debug_time.get()
            #check if the input is valid HH:MM 
            match = re.match(r'(\d+):(\d+)', send_time)
            if not match:
                tkinter.messagebox.showerror("Error", "Please input valid time format HH:MM!")
                return
            hour, minute = map(int, match.groups())
            if hour > 12:
                send_time = f"{hour-12}:{minute:02d} PM"
            else:
                send_time = f"{hour}:{minute:02d} AM"
        #if debug mode is off, get the current time
        else:
            send_time = time.strftime("%I:%M %p")

            

        message = self.entry.get()
        if not message:
            tkinter.messagebox.showerror("Error", "Please input message first!")
            return
        self.textbox.configure(state="normal")
        self.textbox.insert("end", f"{send_time} - {message}\n")
        self.textbox.configure(state="disabled")
        self.entry.delete(0, "end")


    

    def browse_file(self, btn_type):
        self.dialog = filedialog.askopenfilename(initialdir = "/", title = "Select a file", filetypes=((btn_type, "*.txt"),))
        if not self.dialog:
            return
        
        #display dictionary in dictionary tab
        if btn_type == "Dictionary":
            self.dictionary = read_dictionary(self.dialog)
            #if self.dictionary is empty set, show error message
            if not self.dictionary:
                tkinter.messagebox.showerror("Error", "Make sure you have right format for Dictionary!")
                return
            self.dictionary_textbox.configure(state="normal")
            self.dictionary_textbox.delete("0.0", "end")
            self.dictionary_textbox.insert("end", "Dictionary:\n")
            for word in self.dictionary:
                self.dictionary_textbox.insert("end", word + "\n")
            self.dictionary_textbox.configure(state="disabled")
            #check the checkbox
            self.dict_checkbox.configure(state="normal")
            self.dict_checkbox.select()
            self.dict_checkbox.configure(state="disabled")


        #display banned words in banned words tab
        if btn_type == "Banned Words":
            self.banned_words = read_banned_words(self.dialog)
            #if self.banned_words is empty set, show error message
            if not self.banned_words:
                tkinter.messagebox.showerror("Error", "Make sure you have right format for Banned Words!")
                return
            self.banned_words_textbox.configure(state="normal")
            self.banned_words_textbox.delete("0.0", "end")
            self.banned_words_textbox.insert("end", "Banned Words:\n")
            for word in self.banned_words:
                self.banned_words_textbox.insert("end", word + "\n")
            self.banned_words_textbox.configure(state="disabled")
            #check the checkbox
            self.ban_checkbox.configure(state="normal")
            self.ban_checkbox.select()
            self.ban_checkbox.configure(state="disabled")


        if btn_type == "Mail":
            self.messages = read_messages(self.dialog)
            #if self.messages is empty list, show error message
            if not self.messages:
                tkinter.messagebox.showerror("Error", "Make sure you have right format for Messages!")
                return
            
            self.textbox.configure(state="normal")
            self.textbox.delete("0.0", "end")
            for i, (send_time, message) in enumerate(self.messages, 1):
                self.textbox.insert("end", f"{send_time} - {message}\n")
            self.textbox.configure(state="disabled")







    def check_messages(self):
        #remove all messages in the textbox
        self.messenges_textbox.configure(state="normal")
        self.messenges_textbox.delete("0.0", "end")
        self.messenges_textbox.insert("end", "Status Messages:\n")
        self.messenges_textbox.configure(state="disabled")

        if not self.dictionary:
            tkinter.messagebox.showerror("Error", "Please load dictionary first!")
            return
        if not self.banned_words:
            tkinter.messagebox.showerror("Error", "Please load banned words first!")
            return
        try:
            #collect all messages from textbox with format "send_time - message"
            messages = self.textbox.get("0.0", "end").strip().split("\n")
            
            #remove any empty string ""
            messages = [message for message in messages if message]
            print(messages)
            self.messages = [(message.split(" - ")[0], message.split(" - ")[1]) for message in messages]
        except Exception as e:
            print(e)
            tkinter.messagebox.showerror("Error", "Make sure you have right format for Messages!")
            return


        if not messages:
            tkinter.messagebox.showerror("Error", "Please load mail or input messages first!")
            return
        
        for i, (send_time, message) in enumerate(self.messages, 1):
            match = re.match(r'(\d+):(\d+)', send_time)
            if match:
                hour, minute = map(int, match.groups())
            if hour > 12:
                send_time = f"{hour-12}:{minute:02d} CH"
            else:
                send_time = f"{hour}:{minute:02d} Sáng"
            if 1 <= hour <= 6 and needs_review(message, self.dictionary, self.banned_words):
                self.messenges_textbox.configure(state="normal")
                self.messenges_textbox.insert("end", f"message  #{i}: FAILED TO SEND.\n")
                self.messenges_textbox.configure(state="disabled")
            else:
                self.messenges_textbox.configure(state="normal")
                self.messenges_textbox.insert("end",f"message #{i}: {message.capitalize()}\n")
                self.messenges_textbox.configure(state="disabled")
        


if __name__ == "__main__":
    app = App()
    app.mainloop()