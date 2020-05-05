import config
import time
import picamera
import logging
logger = logging.getLogger('ma_ap')
import config
import threading
import sys


class CameraManager():
    def __init__(self, streamer):
        self.streamer = streamer
        self.count = 0
        self.start = time.time()
        
        
    def start_capturing(self):
        logger.info('start capturing')
        with picamera.PiCamera() as camera:
            logger.info('got camera')
            camera.resolution = config.videocamera_resolution
            camera.framerate = config.camera_framerate
            time.sleep(2)
            logger.info('camera is ready')
            video_thread = threading.Thread(target=self.start_video_recording, args=(camera,))
            video_thread.start()
            self.start = time.time()
            
            camera.capture_sequence(self.streamer_setter_generator(), 'jpeg', use_video_port=True, resize=config.camera_resolution)

    def start_video_recording(self, camera):
        try:
            while True:
                logger.info('start_video_recording starts')
                raise NotImplementedError('NNotImplementedError')
                camera.start_recording('{}/{}.h264'.format(config.video_folder, time.strftime("%d_%m_%Y_%H_%M_%S")), splitter_port=1)
                logger.info('start_video_recording after start_recording')
                camera.wait_recording(60)
                logger.info('start_video_recording before stop')
                camera.stop_recording(splitter_port=1)
                logger.info('start_video_recording stopped')
        except Exception as e:
            logger.info('Exception start_video_recording {}'.format(e))
            t, value, traceback = sys.exc_info()
            logger.info('exception in start_video_recording {} {} {}'.format(t, value, traceback))


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
