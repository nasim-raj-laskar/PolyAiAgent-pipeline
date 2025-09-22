import subprocess
import threading
import time
import socket
from dotenv import load_dotenv
from app.common.logger import get_logger
from app.common.custom_exception import CustomException

logger=get_logger(__name__)

load_dotenv()

def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

def run_backend():
    try:
        if is_port_in_use(8000):
            logger.warning("Port 8000 is already in use. Trying port 8001...")
            port = "8001"
        else:
            port = "8000"
        
        logger.info(f"Starting backend on port {port}...")
        subprocess.run(["uvicorn", "app.backend.api:app", "--host", "127.0.0.1", "--port", port], check=True)
    except Exception as e:
        logger.error(f"Error running backend: {e}")
        raise CustomException(f"Error running backend:", e)
    
def run_frontend():
    try:
        logger.info("Starting frontend...")
        subprocess.run(["streamlit", "run", "app/frontend/ui.py"], check=True)
    except CustomException as e:
        logger.error(f"Error running frontend: {e}")
        raise CustomException("Error running frontend: ",e)
    
if __name__ == "__main__":
    try:
        backend_thread = threading.Thread(target=run_backend)
        frontend_thread = threading.Thread(target=run_frontend)

        backend_thread.start()
        time.sleep(3)
        frontend_thread.start()

        backend_thread.join()
        frontend_thread.join()
    except CustomException as e:
        logger.error(f"Error running application: {e}")
        raise CustomException("Error running application:", e)