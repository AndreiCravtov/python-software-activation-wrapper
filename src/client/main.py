# Set up environment for importing other files by including folders
import sys
sys.path.append("./util/")
sys.path.append("./lib/")

from activategui import *
from licence import *

# Import example software
from samplesoftware import *

# Entry point function for main software
def enter_main_software():
    
    # Run sample software
    SampleSoftwareWindow().mainloop()

def main():
    # Checks to make sure software is activated
    if not SoftwareLicence.validate_licence_file():
        SoftwareActivationWindow(SoftwareLicence.activate_software).mainloop()
    if SoftwareLicence.validate_licence_file():

        # Begin running main software
        enter_main_software()

if __name__ == '__main__': # Checks whether to run main window or not
    main()
