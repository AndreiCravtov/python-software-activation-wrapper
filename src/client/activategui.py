from tkinter import *

class SoftwareActivationWindow(Tk):
    def __init__(self, software_activation_function):
        # Copy over functions needed for operation
        self.software_activation = software_activation_function

        # Create window
        self.instantiate_window()
            
        # Draw the widgets
        self.draw_widgets()

    def instantiate_window(self):
        # Start root window
        super().__init__()

        # Configure root window
        self.title("Activate Your Software")
        self.geometry('650x400')
        self.minsize(650, 400)

        # Make the app responsive
        self.columnconfigure(index=0, weight=1)
        self.columnconfigure(index=1, weight=1)
        self.columnconfigure(index=2, weight=1)
        self.columnconfigure(index=3, weight=1)
        self.rowconfigure(index=0, weight=2)
        self.rowconfigure(index=1, weight=1)
        self.rowconfigure(index=2, weight=1)
        self.rowconfigure(index=3, weight=2)

    def draw_widgets(self):
        # Title label
        self.title_label = Label(self, text="Activate Your Software", font=('Arial', 32))
        self.title_label.grid(column = 0, row = 0, columnspan = 4)

        # Enter key label
        self.enter_key_label = Label(self, text="Enter The Key:", font=('Arial', 14))
        self.enter_key_label.grid(column = 1, row = 1, columnspan = 2)

        # Serial key entry
        self.entry_function_register = self.register(self.validate_key_input)
        self.serial_key_entry = Entry(self, justify='center', validate='key', validatecommand=(self.entry_function_register, '%d', '%S', '%P'), bg='white', fg='black', width='46', font='Arial 17')
        self.serial_key_entry.grid(column = 0, row = 2, columnspan = 4, ipady=10)

        # Activate software button
        self.activate_software_button = Button(self, text='Activate', state='disabled', command=self.attempt_software_activation, height=2, width=10, font=('Arial', 26))
        self.activate_software_button.grid(column = 2, row = 3, columnspan = 2)

    def validate_key_input(self, action_type, text_change, value_after):
        # Text entry validation
        if (action_type == '1' and not 
            (text_change.isalnum() and 
            len(value_after) <= 25)):
            return False

        # Button activation validation
        if action_type == '1' and len(value_after) == 25:
            self.activate_software_button.config(state='normal')
        elif action_type == '0':
            self.activate_software_button.config(state='disabled')

        # Styling the entry
        self.serial_key_entry.config(bg='white')
        self.serial_key_entry.config(fg='black')
        
        return True

    def attempt_software_activation(self):
        software_key = self.serial_key_entry.get()
        result = self.software_activation(software_key)

        if result:
            # Close window upon success
            self.destroy()
        else:
            # Styling entry after rejection
            self.serial_key_entry.config(bg='red')
            self.serial_key_entry.config(fg='white')
        
if __name__ == '__main__': # Checks whether to run main window or not
    raise Exception("GUI file run outside main window...") # If so, quits
