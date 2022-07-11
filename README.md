# Python software activation wrapper

## Learning summary

While learning the C# programming language, I have produced a simple web scraper, that scours Wikipedia web pages, as one of my projects. This project scrapes the links from each page so it can continue crawling, and the content of each page. The content is used as material to determine the letter prevalence of the letters of the English alphabet. These prevalence statistics are then displayed as a bar chart to the user in the console.

* Python programming language: while working on this project, I have learned the syntax of Python. I also learned about useful Python features, such as first-class functions or passing by reference. I used these directly as a part of my solution design.

* Object-oriented programming: while working on this project, I began learning to use object-oriented concepts in my design. While the majority of the codebase is still composed of classes which act like namespaces, and are filled with static methods, this project is where I finally begin to have some actual use of object-oriented techniques. For instance, the classes `SoftwareActivationWindow` and `SampleSoftwareWindow` *inherit* from `Tk`. Other classes still have *private* variables which *abstract* their use, only accessible via public methods.

* Tkinter: this solution was divided into *Server* and *Client*. The latter also has a front end. I chose to make this front end with the Python GUI library Tkinter: learning the baisics of both GUI design and Tkinter. I learnt to make a responsive, interactive and intuitive interface, where the entry meant for the software activation key only lets the user type allowed charecters, and only until the right length. A futher demonstration of the focus on interactivity is that the submit button is diabled unless the correct length key is entered. 

* Database: in this project, the *Server* employed a baisic JSON database to keep track of all the active and used licence keys. Although the database is primitive, it does follow a few baisic principles of the database, such as enforcing database structure integrity. If the database structure is found to be wrong, then it is *fixed*.

* Multithreading: one of the design goals of this project is the ability for many *Client* instances to be able to simultaneously activate their respective softwares by connecting to the same *Server* instance and submitting a licence key. I designed the *Server* to use a multithreaded design to achieve this task. I learned how to use Python's `threading` module to start a new thread to deal with every *Client* connection, so the server can service multiple connections simultaneously.

* Networking: this solution fundamentally relies on networking to work. As a result, I've had to learn to use baisic networking tools that Python has to offer (such as `socket` and `select` modules) to be able to establish TCP connections between the `Client` and `Server` and to be able to sent data from one to another. I also used the data interchange format *MessagePack* to encode JSON messages into binary, which is sent over the network, and then converted back into JSON on the other end. This greatly simplified, and made more flexible, communication between my *Client* and *Server*.

* Security: since this project deals with a sensitive thing like software licencing, the employment of security primitives and technology was paramount, for many reasons.
	- One reason to is to obscure the data and algorithms involved for any output file on the system running a *Client* instance. For this, I've used a custom *symmetric cipher* to encrypt and decrypt the file which confirms that the system has been activated, such that they cannot be read. 
	- Another reason is ensuring the privacy and security of the *Client*. For this, I *hash* the unique machine ID of the machine that *Client* is running on, before sending it to the server. This makes sure to get rid of any trace of identifiable information that could compromise user privacy. I also used the *public key cryptography* algorithm - *RSA* - to enable the *Client* to encrypt their licence keys before sending them to the *Server*.
	- The final reason is that these were necessary or useful for the various algorithms that I've designed. For example, the *signing* capabilities of the *RSA* algorithm were used to prove the *Server* has sent a message back to the * Client*, rather than some erroneous entity.

* Problem-solving: as I employed *problem decomposition* while designing the solution, I noticed that many of the subproblems require me creating novel solutions. For every big algorithm I designed, I took inspiration from my pre-existing knowlege of other concepts to create an algorithm that fits the problem.
	- One example of that, is how my knowlege of *Bitcoin*'s mining algorithm - *Hashcash* - inspired me to design the keygen algorithm for this project, including the central element of *Hashcash* as a part of the design.
	- Or for instance, the *Server* mainloop algorithm was inspired by my knowlege of how CPUs process instructions. I created an instruction set, and an instruction queue. Every cycle, an instruction from the front of the queue is executed. Each instruction is composed of the actual instruction and any number of operands. This is all very much inspired by how CPUs work, and fits the problem.
	- The final example would be my custom *symmetric cipher*. I had prior knowlege of the Caesar cipher and also the flaws that it had, and how simple *cryptanalysis* could break it. Nonetheless, this knowlege inspired me to create a much more advanced version of the Caesar cipher, which was not vunrable to the same problems and *cryptanalysis* techniques that the original was vunrable to.

## How to operate this project

### How to run the project

1. Make sure you have the Python interpreter installed.
2. Run `pip3 install msgpack` and `pip3 install rsa` in the terminal.
3.  Clone this repository.
4. Start the *Server* by running `src/server/main.py`.
5. Start the *Server Control* by running `src/server/servercontrol.py`.
6. Start the *Client* by running `src/client/main.py`.

### Application use

The *Server* from this repository will be initialised with no valid active keys. Use the *Server Control* to generate and add a new valid active key; use options 3 and 4 for that. Once there is a valid active licence key, you can enter it into the client activation GUI and submit it to the server. It should work to activate the software. Once a valid active licence key has been used to activate the software, it becomes a valid used licence key and cannot be used anymore. To undo the software activation, delete the activation file: `src/client/data/activation/software_licence.txt`. 

## Viewing and  modifying  the project

This repository is wasn't editited in a specialised code editor - so doesn't have any code-editor-specific artefacts. Hence, it can be cloned and edited in any text editor of your chosing.
