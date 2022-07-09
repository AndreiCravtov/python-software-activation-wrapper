from tkinter import *

# Main app class
class SampleSoftwareWindow(Tk):
    def __init__(self):
        # Create window
        self.instantiate_window()
            
        # Draw the widgets
        self.draw_widgets()

    def instantiate_window(self):
        # Start root window
        super().__init__()

        # Configure root window
        self.title("Sample Software Window")
        self.geometry('325x175')
        self.minsize(325, 175)

        # Make the app responsive
        self.columnconfigure(index=0, weight=1)
        self.rowconfigure(index=0, weight=1)

    def draw_widgets(self):
        # File path entry
        self.file_path_entry = Label(self, text="ACTIVATED!")
        self.file_path_entry.grid(column = 0, row = 0)

if __name__ == "__main__": # check if this is code is being executed from the source file
    raise Exception("This is a module. Import it to use...") # if yes, throw an error
