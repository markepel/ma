import struct
import threading
import io
import logging


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
                    logging.info('error sending to connection')
                    self.stream = None
                finally:
                    self.stream.seek(0)
                    self.stream.truncate()
                    self.event.clear()