class AtomicPrint():
	def __init__(self, initial_state=''):
		self._output = '' if initial_state == '' else initial_state+'\n'
		
	def add_print(self, state=''):
		self._output += state+'\n'
		
	def print_all(self):
		print_string = self._output[:-1] if self._output.endswith('\n') else self._output
		print(print_string)
		self._output = ''

if __name__ == "__main__": # check if this is code is being executed from the source file
    raise Exception("This is a module. Import it to use...") # if yes, throw an error