import socket
import struct
import time
import threading
import picamera
from config import tilda_ip, tilda_port, camera_resolution, camera_framerate, streaming_time
import io
import logging
logging.basicConfig(format='%(asctime)s.%(msecs)03d %(levelname)s {%(module)s} [%(funcName)s] %(message)s', datefmt='%Y-%m-%d,%H:%M:%S', level=logging.INFO)
from image_streamer import ImageStreamer


try:
    client_socket = socket.socket()
    time.sleep(5)
    client_socket.connect((tilda_ip, tilda_port))
    logging.info('connecting to {}:{}...'.format(tilda_ip, tilda_port))
    connection = client_socket.makefile('wb')
    logging.info('connected to {}:{}'.format(tilda_ip, tilda_port))

    connection_lock = threading.Lock()

    count = 0
    start = time.time()
    finish = time.time()

    def streamer_setter_generator(streamer):
        global count, finish
        logging.info('streaming starts')
        while finish - start < streaming_time:
            logging.info(f'streaming stream is {streamer.streamer}')
            yield streamer.stream
            streamer.event.set()
            count += 1
            finish = time.time()


    with picamera.PiCamera() as camera:
        # pool = [ImageStreamer() for i in range(4)]
        image_streamer = ImageStreamer(connection)
        camera.resolution = camera_resolution
        camera.framerate = camera_framerate
        time.sleep(2)
        logging.info('camera is ready')
        start = time.time()
        camera.capture_sequence(streamer_setter_generator(image_streamer), 'jpeg', use_video_port=True)

    # Shut down the streamers in an orderly fashion
    image_streamer.terminated = True
    image_streamer.join()

    # Write the terminating 0-length to the connection to let the server
    # know we're done
    with connection_lock:
        logging.info('connection write last')
        connection.write(struct.pack('<L', 0))
    logging.info('connection write ends')

finally:
    logging.info('Sent %d images in %d seconds at %.2ffps' % (count, finish-start, count / (finish-start)))
    connection.close()
    client_socket.close()
