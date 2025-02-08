import socket
import threading
import hashlib
import random
import time
import os

CHUNK_SIZE = 1024
HOST = 'localhost'
PORT = 12345
DROP_PROBABILITY = 0.1  # 10% chance to simulate packet corruption


def calculate_checksum(data):
    """
    Calculate the checksum for given data using SHA256.
    """
    hasher = hashlib.sha256()
    hasher.update(data)
    return hasher.hexdigest()


def handle_client(conn, addr):
    print(f"Connected to {addr}")
    try:
        checksum = conn.recv(64).decode()
        print(f"Expected checksum: {checksum}")

        received_chunks = {}
        file_data = bytearray()
        expected_sequence_number = 0

        while True:
            packet = conn.recv(CHUNK_SIZE + 8)
            if not packet:
                break

            sequence_number = int(packet[:8].decode())
            chunk_data = packet[8:]

            if random.random() < DROP_PROBABILITY:
                print(f"Simulating packet drop for chunk {sequence_number}")
                continue

            if sequence_number == expected_sequence_number:
                received_chunks[sequence_number] = chunk_data
                print(f"Accepted chunk {sequence_number}")
                conn.sendall(f"ACK:{sequence_number}".encode())
                expected_sequence_number += 1
            else:
                print(f"Out-of-order chunk {sequence_number}, requesting {expected_sequence_number}")
                conn.sendall(f"NACK:{expected_sequence_number}".encode())

        for seq in sorted(received_chunks.keys()):
            file_data.extend(received_chunks[seq])

        computed_checksum = calculate_checksum(file_data)
        print(f"Computed checksum on server: {computed_checksum}")

        if computed_checksum == checksum:
            with open("uploaded_data.txt", "wb") as f:
                f.write(file_data)
            print("File received successfully. Integrity verified.")
            conn.sendall(b"File received successfully.")
        else:
            print("Checksum mismatch. File corrupted during transfer.")
            conn.sendall(b"Checksum mismatch. Please resend.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()
        print(f"Connection with {addr} closed.")


if __name__ == "__main__":
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    print(f"Server listening on {HOST}:{PORT}")

    while True:
        conn, addr = server_socket.accept()
        client_thread = threading.Thread(target=handle_client, args=(conn, addr))
        client_thread.start()