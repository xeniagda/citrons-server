"""
           DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
                   Version 2, December 2004
 
Copyright (C) 2020 citrons

Everyone is permitted to copy and distribute verbatim or modified
copies of this license document, and changing it is allowed as long
as the name is changed.
 
           DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
  TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION

 0. You just DO WHAT THE FUCK YOU WANT TO.
"""

import socketserver
import random
from sys import argv

HOST = ''
try:
    PORT = int(argv[2])
except:
    PORT = 80
try:
    with open(argv[1],'r') as f:
        BODY = f.read()
except:
    BODY = "<script>while(1)alert('I will now be arrested by the Japanese police')</script>"

class Response: # Revolutionary OOP
    def __init__(self, body=BODY,status=None):
        self.headers = ""
        self.body = body
        self.status = "200 Everyone Is Always Asking What the Status Code Is But No One Ever Asks How the Status Code Is Like If You Agree" if status == None else status
        
        self.add_header('Date', 'Tue, 7 Jan 100 00:58:20 GMT')
        self.add_header('Cache-Control', 'exhibitionist, max-age=45')
        self.add_header('Content-Type', 'text/html; charset=PETSCII')
        self.add_header('P3P', 'CP="Privacy is obselete. Any and all data shall be sold to the highest bidder"')
        self.add_header('Content-Length', len(body) + 1)
        self.add_header('Server', 'Blattidus')
        self.add_header('X-XSS-Protection', '0')
        self.add_header('X-Frame-Options', 'plant-evidence')
        self.add_header('Set-Cookie', 'bloodtype=to-be-collected')
        self.add_header('Accept-Ranges', 'none')
        self.add_header('Vary', '*')
        self.add_header('Warning', '199 It Kind Of Smells Like Piss In Here')
        self.add_header('Connection', 'close')
        self.add_header('Expires', 'Yesterday')
        self.add_header('Pragma', 'hi-mom')
        self.add_header('X-Powered-By', 'Wage Slavery')
        self.add_header('X-Content-Duration', '999999999.666')
        self.add_header('Flacidity', 'about three')
        self.add_header('Bees', 'many')
        self.add_header('Humor-Quality', 'terrible')
        self.add_header('English-Spelling', 'american')
        self.add_header('Namesake', 'cockroach')
        self.add_header('Mood', 'angsty')
        self.add_header('Height', '124cm')
        self.add_header('Freshness', 'rotten')
        self.add_header('Editor', 'vim')
        self.add_header('Wug-Plural', 'wuggen')
        self.add_header('GNU-Copypasta', "I'd just like to interject for a moment. What you're refering to as Linux, is in fact, GNU/Linux, or as I've recently taken to calling it, GNU plus Linux. Linux is not an operating system unto itself, but rather another free component of a fully functioning GNU system made useful by the GNU corelibs, shell utilities and vital system components comprising a full OS as defined by POSIX.Many computer users run a modified version of the GNU system every day, without realizing it. Through a peculiar turn of events, the version of GNU which is widely used today is often called Linux, and many of its users are not aware that it is basically the GNU system, developed by the GNU Project.There really is a Linux, and these people are using it, but it is just a part of the system they use. Linux is the kernel: the program in the system that allocates the machine's resources to the other programs that you run. The kernel is an essential part of an operating system, but useless by itself; it can only function in the context of a complete operating system. Linux is normally used in combination with the GNU operating system: the whole system is basically GNU with Linux added, or GNU/Linux. All the so-called Linux distributions are really distributions of GNU/Linux!")
        self.add_header('PH', '7')
        self.add_header('Orientation', 'pansexual')
        self.add_header('Gender', 'none')
        self.add_header('Identity', 'gamer')
        self.add_header('Political-Afflilation', 'marxist-leninist')
        self.add_header('SSN', '457-55-5462')
        self.add_header('Viscosity', '0.01 poise')
        self.add_header('Favorite-Color', 'orange')
        self.add_header('Complexity', 'O(log n)')
        self.add_header('Computational-Class', 'push-down-automaton')
        self.add_header('Lifespan', '10-20 years')
        self.add_header('Legacy', 'none')
        self.add_header('Zodiac', 'aries')
        self.add_header('Temperature', '62 C')
        self.add_header('Shoe-Size', 'confidential')
        self.add_header('Subscribed-Conspiracy-Theories', 'time-cube')
        self.add_header('Dimensions', '4')
        self.add_header('Distro', 'debian')
        self.add_header('Geometric-Shape', 'cone')
        self.add_header('Random-Number', random.randint(0,10))
        self.add_header('Price', '$32')
        self.add_header('Step-2', 'cover-yourself-in-oil')
        self.add_header('Taxes', 'evaded')
        self.add_header('Crimes-Against-Humanity', 4)

    def add_header(self, header, value):
        self.headers += f"{header}: {value}\n"

    def encode(self):
        return f"HTTP/1.1 {self.status}\n{self.headers}\n\n{self.body}".encode()

class Blattidus(socketserver.BaseRequestHandler):
    def handle(self):
        self.request.sendall(Response().encode())

socketserver.TCPServer((HOST, PORT), Blattidus).serve_forever()
