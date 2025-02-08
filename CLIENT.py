import socket
import hashlib
import os
import time
import random

CHUNK_SIZE = 1024
HOST = 'localhost'
PORT = 12345
TIMEOUT = 5
DROP_PROBABILITY = 0.1  # 10% chance to simulate packet corruption


def calculate_checksum(file_path):
    hasher = hashlib.sha256()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(CHUNK_SIZE), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def send_file_chunks(file_path, conn):
    file_size = os.path.getsize(file_path)
    num_chunks = (file_size // CHUNK_SIZE) + (1 if file_size % CHUNK_SIZE != 0 else 0)

    checksum = calculate_checksum(file_path)
    print(f"Checksum of file on client: {checksum}")

    conn.sendall(checksum.encode())

    with open(file_path, 'rb') as f:
        for sequence_number in range(num_chunks):
            chunk_data = f.read(CHUNK_SIZE)
            packet = f"{sequence_number:08d}".encode() + chunk_data

            if random.random() < DROP_PROBABILITY:
                print(f"Simulating corruption for chunk {sequence_number}")
                packet = packet[:-1] + b'X'  # Corrupt the packet

            conn.sendall(packet)
            print(f"Sent chunk {sequence_number}")

            while True:
                try:
                    response = conn.recv(32).decode()
                    if response.startswith("ACK:"):
                        ack_number = int(response.split(":")[1])
                        if ack_number == sequence_number:
                            print(f"Acknowledged chunk {ack_number}")
                            break
                    elif response.startswith("NACK:"):
                        nack_number = int(response.split(":")[1])
                        print(f"NACK received for chunk {nack_number}, resending...")
                        f.seek(nack_number * CHUNK_SIZE)
                        chunk_data = f.read(CHUNK_SIZE)
                        packet = f"{nack_number:08d}".encode() + chunk_data
                        conn.sendall(packet)
                except socket.timeout:
                    print(f"Timeout on chunk {sequence_number}, resending...")
                    conn.sendall(packet)

    print("File transfer complete.")


if __name__ == "__main__":
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.settimeout(TIMEOUT)
    client_socket.connect((HOST, PORT))

    file_path = input("Enter the path of the file to upload: ")
    if os.path.exists(file_path):
        send_file_chunks(file_path, client_socket)
    else:
        print("File not found.")

    client_socket.close()