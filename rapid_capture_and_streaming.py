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
# create file handler which logs even debug messages
fh = logging.FileHandler('ma.log')
# create console handler with a higher log level
ch = logging.StreamHandler()
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s.%(msecs)03d -  %(levelname)s - %(name)s - {%(module)s} - [%(funcName)s] - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)
# logging.basicConfig(format='%(asctime)s.%(msecs)03d %(levelname)s {%(module)s} [%(funcName)s] %(message)s', datefmt='%Y-%m-%d,%H:%M:%S', level=logging.INFO)
from image_streamer import ImageStreamer
from camera_manager import CameraManager


# try:
#     client_socket = socket.socket()
#     time.sleep(5)
#     client_socket.connect((tilda_ip, tilda_port))
#     logging.info('connecting to {}:{}...'.format(tilda_ip, tilda_port))
#     connection = client_socket.makefile('wb')
#     logging.info('connected to {}:{}'.format(tilda_ip, tilda_port))

#     connection_lock = threading.Lock()

#     count = 0
#     start = time.time()
#     finish = time.time()




#     with picamera.PiCamera() as camera:
#         # pool = [ImageStreamer() for i in range(4)]
#         image_streamer = ImageStreamer(connection)
#         camera.resolution = camera_resolution
#         camera.framerate = camera_framerate
#         time.sleep(2)
#         logging.info('camera is ready')
#         start = time.time()
#         camera.capture_sequence(streamer_setter_generator(image_streamer), 'jpeg', use_video_port=True)

#     # Shut down the streamers in an orderly fashion
#     image_streamer.terminated = True
#     image_streamer.join()
# Write the terminating 0-length to the connection to let the server
        # know we're done
        # with connection_lock:
        #     logging.info('connection write last')
        #     connection.write(struct.pack('<L', 0))
# finally:
#     logging.info('Sent %d images in %d seconds at %.2ffps' % (count, finish-start, count / (finish-start)))
#     connection.close()
#     client_socket.close()

    
for i in range(retry_count):
    try:
        connection_lock = threading.Lock()
        logger.info('retrying')
        time.sleep(5)
        new_socket = socket.socket()
        new_socket.connect((tilda_ip, tilda_port))
        logger.info('connecting to {}:{}...'.format(tilda_ip, tilda_port))
        new_connection = new_socket.makefile('wb')
        logger.info('connected to {}:{}'.format(tilda_ip, tilda_port))
        new_streamer = ImageStreamer(new_connection)
        camera_manager = CameraManager(new_streamer)
        camera_manager.start_capturing()
        
        new_streamer.terminated = True
        new_streamer.join()
        with connection_lock:
            logger.info('new_connection write last')
            new_connection.write(struct.pack('<L', 0))
        logger.info('connection write ends')
    except Exception as e:
        logger.error('Exception when retrying streaming {}'.format(e), exc_info=True)
        try:
            logger.info(f'Total images sent {camera_manager.get_total_images_count()} on fps {camera_manager.get_fps()}')
        except:
            pass
    finally:
        try:
            new_socket.close()
            new_connection.close()
        except Exception as e:
            logger.error('Exception when retrying to close connection and socket {}'.format(e), exc_info=True)



