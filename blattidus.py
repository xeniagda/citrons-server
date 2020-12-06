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
from sys import argv,stderr

HOST = ''
try:
    PORT = int(argv[1])
except:
    PORT = 80

main_args = argv[2:]
if "--log" in main_args:
    log = True
else:
    log = False

files = list(filter("--log".__ne__, main_args))

def get_path(path):
    if len(path) > 0 and path[0] == '/':
        path = path[1:]
    return path

def get_page(path):
    p = get_path(path)
    if p in files:
        try:
            with open(p,'r') as f:
                return f.read()
        except:
            return None
    else:
        return None

DEFAULT_INDEX = "<script>while(1)alert('I will now be arrested by the Japanese police.')</script>"

try:
    with open("cash-money.txt", 'r') as f:
        CASH_MONEY = f.read().strip()
except:
    print("NOTICE: cash-money.txt IS UNAVAILABLE")
    CASH_MONEY = "poor"

VERSION = "blattidus/1.1.2r"

class Response: # Revolutionary OOP
    def __init__(self, page, status=None):
        self.headers = ""

        self.status = "200 Everyone Is Always Asking What the Status Code Is But No One Ever Asks How the Status Code Is Like If You Agree" if status == None else status

        self.body = DEFAULT_INDEX
        self.get_body(page)

        self.add_header('Date', 'Tue, 7 Jan 100 00:58:20 GMT')
        self.add_header('Cache-Control', 'exhibitionist, max-age=45')
        self.add_header('Content-Type', 'text/html; charset=PETSCII')
        self.add_header('P3P', 'CP="Privacy is obselete. Any and all data shall be sold to the highest bidder"')
        self.add_header('Content-Length', len(self.body.encode()))
        self.add_header('Server', VERSION)
        self.add_header('X-XSS-Protection', '0')
        self.add_header('X-Frame-Options', 'plant-evidence')
        self.add_header('Based-on', 'what')
        self.add_header('Set-Cookie', 'bloodtype=to-be-collected')
        self.add_header('Accept-Ranges', 'none')
        self.add_header('Vary', '*')
        self.add_header('Warning', '199 It Kind Of Smells Like Piss In Here')
        self.add_header('Connection', 'close')
        self.add_header('Last-Modified', 'tomorrow')
        self.add_header('Expires', 'Yesterday')
        self.add_header('Pragma', 'hi-mom')
        self.add_header('Hotel', 'Trivago')
        self.add_header('X-Powered-By', 'Wage Slavery')
        self.add_header('Hotel', 'Trivago')
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
        self.add_header('Variant', 'coralian')
        self.add_header('Gender', 'none')
        self.add_header('Identity', 'gamer')
        self.add_header('Political-Afflilation', 'marxist-leninist')
        self.add_header('SSN', '457-55-5462')
        self.add_header('Viscosity', '0.01 poise')
        self.add_header('Favorite-Color', 'orange')
        self.add_header('Cash-Money', CASH_MONEY)
        self.add_header('Complexity', 'O(log n)')
        self.add_header('Computational-Class', 'push-down-automaton')
        self.add_header('Lifespan', '10-20 years')
        self.add_header('Legacy', 'none')
        self.add_header('Zodiac', 'aries')
        self.add_header('Temperature', '62 C')
        self.add_header('Knuckles', 'Cracked')
        self.add_header('Shoe-Size', 'confidential')
        self.add_header('Subscribed-Conspiracy-Theories', 'time-cube')
        self.add_header('Dimensions', '4')
        self.add_header('Distro', 'debian')
        self.add_header('Geometric-Shape', 'cone')
        self.add_header('Random-Number', random.randint(0,10))
        self.add_header('Price', '$32')
        self.add_header('Step-2', 'cover-yourself-in-oil')
        self.add_header('Taxes', 'evaded')
        self.add_header('Crimes-Against-Humanity', 5)
        self.add_header('Rickroll', 'https://www.youtube.com/watch?v=dQw4w9WgXcQ')
        self.add_header('Income', 'around $73,000')

    def get_body(self, page):
        if self.status.split()[0] != "200":
            self.error_page()
            return
        p = get_page(page)
        if p == None:
            if page == "/index.html":
                self.body = DEFAULT_INDEX
                return
            if not get_path(page) in files:
                self.status = "404 Link Rot"
                self.error_page()
            else:
                self.status = "500 I Am NOT OK"
                self.error_page()
        else:
            self.body = p

    def error_page(self):
        code = self.status.split()[0]
        p = get_page(f"{code}.html")
        if p != None:
            self.body = p
            return
        p = get_page("error.html")
        if p != None:
            p = p.replace('BLATTIDUS ERROR', self.status)
            self.body = p
            return
        self.body = f"<h1>{self.status}</h1>"

    def add_header(self, header, value):
        self.headers += f"{header}: {value}\n"

    def encode(self):
        return f"HTTP/1.1 {self.status}\n{self.headers}\n{self.body}".encode()

class Blattidus(socketserver.BaseRequestHandler):
    def perform_response(self, method, path, status):
        try:
            r = Response(path, status=status)
            self.request.send(r.encode())
        except Exception as err:
            if log:
                stderr.write(f"ERROR ({err}) serving response ({method} {path})\n")
            self.request.send(Response(path, status="500 I Am NOT OK").encode())
            return
        finally:
            self.request.close()
        if log:
            stderr.write(f"{method} {path} -> {r.status}\n")

    def handle(self):
        try:
            data = self.request.recv(1024).decode()
            req_head = data.split('\n')[0].split()
            req_method = req_head[0]
            req_path = req_head[1]
            req_version = req_head[2]
        except:
            self.perform_response("GET", "/", "400 Do You Even Know HTTP?")
            return
            
        status = "405 GET Better at HTTP" if req_method != "GET" else None
        status = "418 I'm a teapot" if req_method == "BREW" or req_method == "WHEN" else None
        
        if req_path == "/":
            req_path = "/index.html"

        self.perform_response(req_method, req_path, status)

class BlattidusTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True

server = BlattidusTCPServer((HOST, PORT), Blattidus)
try:
    server.serve_forever()
except KeyboardInterrupt:
    server.shutdown()
