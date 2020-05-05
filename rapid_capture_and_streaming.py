import socket
import struct
import time
import threading
import picamera
from config import tilda_ip, tilda_port, camera_resolution, camera_framerate, streaming_time, retry_count
import io
import logging
logger = logging.getLogger('ma_ap')
logger.setLevel(logging.INFO)
fh = logging.FileHandler('ma.log')
ch = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s.%(msecs)03d -  %(levelname)s - %(name)s - {%(module)s} - [%(funcName)s] - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
logger.addHandler(fh)
logger.addHandler(ch)
from image_streamer import ImageStreamer
from camera_manager import CameraManager
import sys
import traceback

def start_secure():   
    for i in range(retry_count):
        try:
            logger.info('retrying')
            time.sleep(5)
            new_socket = socket.socket()
            new_socket.connect((tilda_ip, tilda_port))
            logger.info('connecting to {}:{}...'.format(tilda_ip, tilda_port))
            new_connection = new_socket.makefile('wb')
            logger.info('connected to {}:{}'.format(tilda_ip, tilda_port))
            new_streamer = ImageStreamer(new_connection)
            logger.info('Image streamer created ')
            camera_manager = CameraManager(new_streamer)
            logger.info('camera_manager created ')
            camera_manager.start_capturing()
            
            new_streamer.terminated = True
            new_streamer.join()
            logger.info('new_connection write last')
            new_connection.write(struct.pack('<L', 0))
            logger.info('connection write ends')
        except Exception as e:
            t, value, t2 = sys.exc_info()
            logger.error('Exception when retrying streaming {} {}'.format(t, value), exc_info=True)
            logger.info('###duplicate###Exception  when retrying streaming {} {}'.format(t, value))
            traceback.print_tb(err.__traceback__)
            try:
                logger.info(f'Total images sent {camera_manager.get_total_images_count()} on fps {camera_manager.get_fps()}')
            except:
                pass
        finally:
            try:
                new_socket.close()
                new_connection.close()
            except Exception as e:
                t, value, t2 = sys.exc_info()
                logger.error('Exception when retrying to close connection and socket {} {}'.format(t, value), exc_info=True)
                logger.error('@@@duplicate@@@Exception when retrying to close connection and socket {} {}'.format(t, value))
                traceback.print_tb(err.__traceback__)


if __name__ == "__main__":
    start_secure()
    
    # income_manager = IncomeManager(MotionDetectionProcessor())
    # flask_app = create_flask_app(income_manager=income_manager)
    # logging.info('flask started main')
    # image_receiver_thread = threading.Thread(target=income_manager.start_receiving)
    # image_receiver_thread.start()
    # flask_app.run(host='0.0.0.0', port=5000, debug=True,threaded=True, use_reloader=False)

