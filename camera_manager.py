import config
import time
import picamera
import logging
logger = logging.getLogger('ma_ap')
import config
import threading

class CameraManager():
    def __init__(self, streamer):
        self.streamer = streamer
        self.count = 0
        self.start = time.time()
        
        
    def start_capturing(self):
        with picamera.PiCamera() as camera:
            camera.resolution = config.videocamera_resolution
            camera.framerate = config.camera_framerate
            time.sleep(2)
            logger.info('camera is ready')
            video_thread = threading.Thread(target=self.start_capturing_and_recording, args=(camera,))
            video_thread.start()
            self.start = time.time()
            
            camera.capture_sequence(self.streamer_setter_generator(), 'jpeg', use_video_port=True, resize=config.camera_resolution)

    def start_capturing_and_recording(self, camera):
        try:
            logger.info('start_capturing_and_recording starts')
            # with picamera.PiCamera() as camera:
            # camera.resolution = config.videocamera_resolution
            # camera.framerate = config.videocamera_framerate
            time.sleep(2)
            logger.info('videocamera is ready')
            
            camera.start_recording('1920_1.h264', splitter_port=1)
            camera.wait_recording(60)
            camera.stop_recording(splitter_port=1)
        except Exception as e:
            logger.info('exception in start_capturing_and_recording {}'.format(e))
            raise e


    def streamer_setter_generator(self):
        logger.info('CameraManager streaming starts')
        while True:
            yield self.streamer.stream
            self.streamer.event.set()
            self.count += 1
        logging.info('CameraManager streaming ends')
    
    def get_total_images_count(self):
        return self.count
    
    def get_fps(self):
        return (time.time()-self.start)/count
