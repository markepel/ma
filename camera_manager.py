from config import camera_resolution, camera_framerate
import time

class CameraManager():
    def __init__(self, streamer):
        self.streamer = streamer
        self.count = 0

    def start_capturing():
        camera.resolution = camera_resolution
        camera.framerate = camera_framerate
        time.sleep(2)
        logging.info('camera is ready')
        self.start = time.time()
        camera.capture_sequence(streamer_setter_generator(self.streamer), 'jpeg', use_video_port=True)

    def streamer_setter_generator():
        logging.info('streaming starts')
        while self.finish - self.start < streaming_time:
            logging.info(f'streaming stream is {self.streamer.stream}')
            yield self.streamer.stream
            self.streamer.event.set()
            self.count += 1
            self.finish = time.time()
    
    def get_total_images_count():
        return self.count
    
    def get_fps():
        finish = self.finish if hasattr(self, 'finish') and self.finish else time.time()
        return (finish-self.start)/count
