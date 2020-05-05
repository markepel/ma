import struct
import threading
import io
import logging
logger = logging.getLogger('ma_ap')
import traceback



class ImageStreamer(threading.Thread):
    def __init__(self, connection):
        super(ImageStreamer, self).__init__()
        self.connection = connection
        self.stream = io.BytesIO()
        self.event = threading.Event()
        self.terminated = False
        self.start()

    def run(self):
        # This method runs in a background thread
        while not self.terminated:
            # Wait for the image to be written to the stream
            if self.event.wait(3):
                try:
                    self.connection.write(struct.pack('<L', self.stream.tell()))
                    self.connection.flush()
                    self.stream.seek(0)
                    self.connection.write(self.stream.read())
                except Exception as e:
                    self.stream.seek(0)
                    self.stream.truncate()
                    self.event.clear()
                    logger.info('error sending to connection')
                    t, value, t2 = sys.exc_info()
                    logger.info('exception in start_capturing {} {}'.format(t, value))
                    traceback.print_tb(e.__traceback__)
                    self.stream = None
                finally:
                    self.stream.seek(0)
                    self.stream.truncate()
                    self.event.clear()