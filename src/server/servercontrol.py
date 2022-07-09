# Set up enviroment for importing other files by including folders
import sys
sys.path.append("./util/")
sys.path.append("./lib/")

from instruct import INSTRUCTION_FILE_PATH
import crypto as crp
import keygen as kgn

# create a main menu contained in the innit
class ServerControlShell:
    def __init__(self):
        # print initial greeting
        self.initial_greeting()

        while True:
            #display main menu
            self.display_main_menu()

            # get current option entered by the user
            while True:
                try:
                    option = int(input("> "))
                    print('\n')

                    if option in range(1, 8):
                        break
                except:
                    pass
            
            # execute the option the user chose
            if option == 1:
                
                # exit shell
                break

            elif option == 2:
                
                # terminate server
                self.write_instruction('QUIT_MAINLOOP')

            elif option == 3:
                
                # generate and print new key
                print(kgn.ServerKeyUtils.generate_key() + "\n\n")

            elif option == 4:

                # add active licence key
                licence_key = self.get_licence_key()
                checksum = kgn.KeyUtils.get_key_checksum(licence_key)

                self.write_instruction('ADD_ACTIVE_LICENCE_KEY%'+licence_key+'|'+checksum)
                print()

            elif option == 5:

                # remove active licence key
                licence_key = self.get_licence_key()
                checksum = kgn.KeyUtils.get_key_checksum(licence_key)

                self.write_instruction('REMOVE_ACTIVE_LICENCE_KEY%'+licence_key+'|'+checksum)
                print()

            elif option == 6:

                # add used licence key
                licence_key = self.get_licence_key()
                checksum = kgn.KeyUtils.get_key_checksum(licence_key)

                self.write_instruction('ADD_USED_LICENCE_KEY%'+licence_key+'|'+checksum)
                print()
            
            elif option == 7:

                # remove used licence key
                licence_key = self.get_licence_key()
                checksum = kgn.KeyUtils.get_key_checksum(licence_key)

                self.write_instruction('REMOVE_USED_LICENCE_KEY%'+licence_key+'|'+checksum)
                print()

        self.goodbye()
    
    def initial_greeting(self):
        print("Welcome to the Server Control CLI\n\n\tHere you can interact with\n\tthe server by sending it\n\tinstructions.\n\n")

    def display_main_menu(self):
        print("Main Menu:\n\t1: Quit Shell\n\t2: Terminate Server\n\t3: Generate Licence Key\n\t4: Add Active Licence Key\n\t5: Remove Active Licence Key\n\t6: Add Used Licence Key\n\t7: Remove Used Licence Key\n\nSelect an option...\n")

    def goodbye(self):
        print("\n\nGoodbye!")
        input("Press enter to exit...")

    def get_licence_key(self):
        print("Enter a licence key...\n")
        while True:
            try:
                key = input("> ")
                if kgn.ServerKeyUtils.validate_key(key, kgn.SEED, kgn.ALPHABET):
                    break
            except:
                pass
        return key

    def write_instruction(self, string):
        if open(INSTRUCTION_FILE_PATH, 'r', encoding=crp.ENCODING_STANDARD).read() == "":
            open(INSTRUCTION_FILE_PATH, 'a', encoding=crp.ENCODING_STANDARD).write(string)
        else:
            open(INSTRUCTION_FILE_PATH, 'a', encoding=crp.ENCODING_STANDARD).write("\n"+string)

if __name__ == "__main__": #check if this is code is being executed from the source file
    ServerControlShell() #if yes, run
