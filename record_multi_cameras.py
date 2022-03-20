import threading
import time
import cv2
import os
from matplotlib import pyplot
pyplot.switch_backend('Agg')


class CamThread(threading.Thread):
    def __init__(self, previewName, camID, save_dir):
        threading.Thread.__init__(self)
        self.previewName = previewName
        self.camID = camID
        self.save_dir = save_dir

    def run(self):
        print("Starting " + self.previewName)
        CamPreview(self.previewName, self.camID, self.save_dir)


def CamPreview(previewName, camID, save_dir):
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    cv2.namedWindow(previewName)
    cam = cv2.VideoCapture(camID)
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
    if cam.isOpened():  # try to get the first frame
        rval, frame = cam.read()
    else:
        rval = False

    last_time = time.time()
    capture_duration = 5

    while rval:
        cv2.imshow(previewName, frame)
        rval, frame = cam.read()

        # capture frames
        curr_time = time.time()
        if curr_time - last_time >= capture_duration:
            file_name = str(int(curr_time))+'.jpg'
            file_path = os.path.join(save_dir, file_name)
            cv2.imwrite(file_path, frame)
            last_time = curr_time

        key = cv2.waitKey(20)
        if key == 27:  # exit on ESC
            break
    cv2.destroyWindow(previewName)


if __name__ == '__main__':
    # Create two threads as follows
    # thread1 = CamThread("Camera 1", 0, './camera_0/')
    # thread2 = CamThread("Camera 2", 2)
    # thread1.start()
    # thread2.start()
    CamPreview("Camera 0", 0, './20220317/camera_0/')
