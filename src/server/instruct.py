import time
from enum import Enum, auto

import crypto as crp
import database as db

INSTRUCTION_FILE_PATH = 'data/instructionqueue/instructions.txt'

class InstructionSet(Enum):
    NULL = auto()
    QUIT_MAINLOOP = auto()
    ADD_ACTIVE_LICENCE_KEY = auto()
    REMOVE_ACTIVE_LICENCE_KEY = auto()
    ADD_USED_LICENCE_KEY = auto()
    REMOVE_USED_LICENCE_KEY = auto()

class Instruction:
    def __init__(self, instruction, parameters):
        self.instruction = instruction
        self.parameters = parameters

class Mainloop:
    def __init__(self, function, tick_rate):
        while True:
            # read instruction
            current_instruction = Mainloop.read_next_instruction()

            # interpret instructions
            if current_instruction.instruction == InstructionSet.QUIT_MAINLOOP:
                break
            elif current_instruction.instruction != InstructionSet.NULL:
                Mainloop.handle_incoming_instruction(current_instruction)

            # run the functionality
            function()

            # sleep
            time.sleep(1/tick_rate)

    @staticmethod
    def string_to_enum(string):
        for instruction in InstructionSet:
            if string == instruction.name:
                return instruction
        return InstructionSet.NULL
    
    @staticmethod
    def read_next_instruction(instruction_file_path=INSTRUCTION_FILE_PATH):
        # read instruction file
        current_instruction_string = ""
        instructions = open(instruction_file_path, 'r', encoding=crp.ENCODING_STANDARD).readlines()
        
        if not instructions == []:
            # get current instruction
            current_instruction_string = instructions[0].rstrip('\n')

            # save the rest
            del instructions[0]
            left_over_instructions = ''.join(i for i in instructions)
            open(instruction_file_path, 'w', encoding=crp.ENCODING_STANDARD).write(left_over_instructions)

        # if instruction has opcode, then split further
        if '%' in current_instruction_string:
            instruction_parts = current_instruction_string.split('%')
            current_instruction = Instruction(Mainloop.string_to_enum(instruction_parts[0]), instruction_parts[1].split('|'))
        else:
            current_instruction = Instruction(Mainloop.string_to_enum(current_instruction_string), [])

        return current_instruction

    @staticmethod
    def handle_incoming_instruction(instruction):
        print(f"Processing new instruction: {instruction.instruction.name}")
        try:
            # check which instruction it is
            if instruction.instruction == InstructionSet.ADD_ACTIVE_LICENCE_KEY:
                
                # add new active licence key
                db.LicenceDatabaseUtils.add_active_key(instruction.parameters[0], instruction.parameters[1])
            
            elif instruction.instruction == InstructionSet.REMOVE_ACTIVE_LICENCE_KEY:
                
                # remove active licence key
                db.LicenceDatabaseUtils.remove_active_key(instruction.parameters[0], instruction.parameters[1])
            
            elif instruction.instruction == InstructionSet.ADD_USED_LICENCE_KEY:
                
                # add used licence key
                db.LicenceDatabaseUtils.add_used_key(instruction.parameters[0], instruction.parameters[1])
            
            elif instruction.instruction == InstructionSet.REMOVE_USED_LICENCE_KEY:
                
                # remove used licence key
                db.LicenceDatabaseUtils.remove_used_key(instruction.parameters[0], instruction.parameters[1])
            
            print("\tProcessing complete")
        except Exception as e:
            print(f"\tException when executing instruction: {e}")

if __name__ == "__main__": # check if this is code is being executed from the source file
    raise Exception("This is a module. Import it to use...") # if yes, throw an error