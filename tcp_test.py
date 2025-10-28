# minimal_test.py
import socket
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

def minimal_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('0.0.0.0', 5000))
    sock.listen(5)
    
    logger.info("🔧 MINIMAL SERVER listening on 0.0.0.0:5000")
    
    while True:
        logger.info("⏳ Waiting...")
        client, addr = sock.accept()
        logger.info(f"🎯 CONNECTED: {addr}")
        client.send(b'\x06')
        client.close()
        logger.info("🔚 Closed")

if __name__ == "__main__":
    minimal_server()