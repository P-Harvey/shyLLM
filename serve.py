"""
File:           ./serve.py
Name:           Self Host your (own) LLM
Description:    This module launches a local server
                using the uvicorn python package.
                Some attempts have been made to handle
                busy ports, however this is still experimental.
Created by:     P.L. Harvey
LICENSE:        Apache2.0
Copyright:      2024, P.L. Harvey
Modified on:    20241120
"""
from datetime import datetime
from sys import exit as sysexit
from sys import stderr
from random import randint
from socket import error as socket_error
from socket import socket, AF_INET, SOCK_STREAM
import uvicorn

def find_available_port() -> int:
    """
    Find an available port on the local machine.

    This function will keep trying different ports
    above 8000 until it finds one that is available.
    It uses a random port above 8000 to avoid conflicts
    with other services that may be using lower ports.

    Returns:
        int: The available port number
    """
    while True:
        # Choose a random port above 8000
        port = 8000 + randint(0, 65535)

        try:
            # Create a socket and bind it to the chosen port
            sock = socket(AF_INET,
                          SOCK_STREAM)

            sock.bind(("0.0.0.0",
                       port))

            # If the binding is successful,
            # and return the port number
            sock.close()
            return port

        except socket_error:
            # If there's an error,
            # try again with a new port
            pass

def run_server() -> None:
    """
    Run the server using Uvicorn.

    This function will start the server on a randomly
    chosen available port and print out a message
    indicating which port is being used.

    Returns:
        None
    """
    try:
        # Record the start time of the server
        start_time: datetime = datetime.now()

        # Find an available port
        port: int = find_available_port()

        # Run Uvicorn with the chosen port and reload=True
        # to automatically restart if changes are made to the app code
        uvicorn.run("main:app",
                    host = "0.0.0.0",
                    reload = True,
                    port = port)

        # Record the end time of the server
        end_time: datetime = datetime.now()

        # Print out a message indicating which port is being
        # used and how long it took to start the server
        print(f"""
              Uvicorn is serving on port: {port}
              Server started in {(end_time - start_time).total_seconds()} seconds!
              """)

    except OSError as e:
        # Check if the error is due to a refused connection
        if e.errno == 98: # Address already in use
            print("Unable to choose a free port.", file = stderr)
            sysexit(1)
        else:
            raise e

# Run the server
run_server()
