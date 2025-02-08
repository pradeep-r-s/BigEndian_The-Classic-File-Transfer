BigEndian: The Classic File Transfer

Project Overview   
This project demonstrates a reliable file transfer system using Python sockets, implementing packet order maintenance and checksum verification for data integrity. The system effectively handles file transfer between a client and server while verifying that all packets are intact and correctly ordered.
Features   
Reliable File Transmission:    Ensures seamless file transfer from the client to the server.
Packet Ordering:    Maintains correct packet order using sequence numbers.
Checksum Verification:   
Each packet includes a SHA-256 checksum to ensure data integrity.
Mismatches trigger retransmission requests (NACK).
Acknowledgment Mechanism:    Utilizes ACK (Acknowledgment) and NACK (Negative Acknowledgment) to ensure accurate packet delivery.

How It Works   
1. The    server    listens for connections from clients.
2. The    client    reads the file in chunks and calculates a checksum for each packet.
3. Packets are transmitted with sequence numbers and checksum values.
4. The server verifies packet integrity and sends appropriate acknowledgments.
5. If checksum verification fails, the server requests a retransmission.

Setup Instructions   
Requirements   
- Python 3.x

Steps to Run the Project   
1. Clone the repository:
  
   git clone <repository-url>

2. Navigate to the project directory:
 
   cd BigEndian_The-Classic-File-Transfer

3. Start the server:
   python3 SERVER.py
   

4. In another terminal, start the client:
   python3 CLIENT.py
   

5. Enter the file path to upload.

     File Descriptions   
-    CLIENT.py:    Handles file reading, packet formation, and transmission to the server.
-    SERVER.py:    Handles incoming connections, packet verification, and file reconstruction.
-    sample.txt:    Example file for testing the transfer.

     Example Output   
  Successful Packet Transmission:
  received packet 1: Checksum valid. Sending ACK.
  Checksum Mismatch:   
  Received packet 2: Checksum invalid. Sending NACK.
  Transfer Completion:   
  File successfully received and verified.
  
     Key Considerations   
-    Checksum Variation:    Different files produce unique checksum values for integrity verification.
-    Data Integrity Assurance:    The server recalculates and compares checksums for each packet.
-    Robust Error Handling:    Retransmissions ensure no packet loss.


     Project Insights   
This project demonstrates critical aspects of networking and communication in computer systems, such as:
- Ensuring data integrity during transmission.
- Employing checksum mechanisms for validation.
- Handling packet retransmissions and acknowledgment mechanisms.
- 
     Contact   
For further queries, please contact [pradeeprs0123@gmail.com](mailto:pradeeprs0123@gmail.com).

