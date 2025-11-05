# File: controllers/thymio_supervisor/thymio_supervisor.py
#
# This script allows Webots' Thymio2 robot to be controlled externally
# through a TCP port compatible with the 'thymiodirect' Python library.
#
# Requirements:
# - Python controller must be enabled in Webots
# - Webots Thymio2 robot node assigned to this controller
# - Simulation must be running (not paused)

from controller import Supervisor
import socket
import threading
import struct
import json

# TCP configuration
HOST = '127.0.0.1'
PORT = 2001

# Create supervisor instance
supervisor = Supervisor()
timestep = int(supervisor.getBasicTimeStep())

# Find the Thymio node
thymio = supervisor.getFromDef("Thymio")
if thymio is None:
    print("[ERROR] No DEF named 'THYMIO' found in the world. Please set your Thymio robot's DEF field to 'THYMIO'.")
    exit(1)

print(f"[INFO] Thymio supervisor started. Listening on TCP port {PORT}...")

# Create TCP server socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen(1)

client_conn = None
client_addr = None
lock = threading.Lock()

# Function to handle client messages
def client_thread(conn, addr):
    global client_conn
    print(f"[INFO] Client connected from {addr}")
    conn.settimeout(0.01)
    while True:
        try:
            data = conn.recv(1024)
            if not data:
                break
            command = data.decode().strip()
            # Example: {"left":200,"right":150}
            try:
                cmd = json.loads(command)
                if "left" in cmd and "right" in cmd:
                    with lock:
                        thymio.getField("leftWheelVelocity").setSFFloat(float(cmd["left"]))
                        thymio.getField("rightWheelVelocity").setSFFloat(float(cmd["right"]))
            except json.JSONDecodeError:
                print("[WARN] Invalid command:", command)
        except socket.timeout:
            pass
    print("[INFO] Client disconnected.")
    conn.close()
    client_conn = None

# Start listener thread
def accept_thread():
    global client_conn, client_addr
    while True:
        conn, addr = server.accept()
        with lock:
            client_conn = conn
            client_addr = addr
        threading.Thread(target=client_thread, args=(conn, addr), daemon=True).start()

threading.Thread(target=accept_thread, daemon=True).start()

# Main supervisor loop
while supervisor.step(timestep) != -1:
    pass

# Cleanup
if client_conn:
    client_conn.close()
server.close()
