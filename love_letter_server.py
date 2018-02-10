#!/usr/bin/env python

import os
import socket
import threading

# This file contains a multithreaded server for connecting love_letter_clients.
# @author Troy Madsen

# Class difinition of a ClientThread
class ClientThread(threading.Thread):

    # Initialize ClientThread
    def __init__(self, conn, parent, ip, port):
        threading.Thread.__init__(self)
        self.conn = conn
        self.parent = parent
        self.clientIP = ip
        self.clientPort = port
        print('[+] ' + self.clientIP + ':' + str(self.clientPort) + ' connected to game server')

    # Execution of the ClientThread
    def run(self):
        try:
            while True:
                query = self.conn.recv(1024)
                print('[#] Query receivced: ' + query)
                if query == 'quit':
                    break
        except Exception as e:
            print(e)
        finally:
            print('[-] ' self.clientIP + ':' str(self.clientPort) + ' disconnected')
            self.conn.close()



# Class definition of a LoveLetterServer
class LoveLetterServer:

    def run(self):
        # Multithreaded Python server running over TCP connection
        HOST = socket.gethostbyname(socket.gethostname())
        PORT = 8771

        # Create server
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((HOST, PORT))
        clients = []

        # Wait for clients to connect
        print('Server awaiting players')
        print('Press ^C to exit')

        try:
            while True:
                server.listen(4)
                (conn, (ip, port)) = server.accept()
                new_client = ClientThread(conn, self, ip, port)
                new_client.start()
                clients.append(new_client)
        except Exception as e:
            print(e)
        except KeyboardInterrupt as i:
            print
        finally:
            print('Love Letter Server shutting down')
            for c in clients:
                c.join()



# Entry point of the program
def main():
    server = LoveLetterServer()
    server.run()

# Determine if this is the main program running
if __name__ == '__main__':
    main() 
