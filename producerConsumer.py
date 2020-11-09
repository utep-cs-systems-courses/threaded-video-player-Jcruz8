import cv2
import os
import time
import numpy as np
from threading import Thread
from queueFrames import Queue

clipFileName = "clip.mp4"
capacity = 10

readFramesQueue = Queue(capacity)
grayFramesQueue = Queue(capacity)

def extractFrames(clipFileName, readFramesQueue):
    vidcap = cv2.VideoCapture(clipFileName)
    count = 0
    success, image = vidcap.read()
    print(f'Reading frame {count} {success}')
    while success and count < 72:
        success, jpgImage = cv2.imencode('.jpg', image)
        readFramesQueue.enqueue(jpgImage)
        success, image = vidcap.read()
        print(f'Reading frame {count}')
        count += 1
    readFramesQueue.enqueue(None)
    print("Video Extraction completed")

def convertToGrayScale(readFramesQueue, grayFramesQueue):
    count = 0
    inputFrame = readFramesQueue.dequeue()

    while inputFrame is not None and count < 72:
        print(f'Converting frame {count}')
        image = cv2.imdecode(inputFrame, cv2.IMREAD_UNCHANGED)
        grayscaleFrame = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        success, jpgImage = cv2.imencode('.jpg', grayscaleFrame)
        grayFramesQueue.enqueue(jpgImage)
        count += 0
        inputFrame = readFramesQueue.dequeue()
    grayFramesQueue.enqueue(None)
    print("Video has been converted to gray")

def displayFrames(grayFramesQueue):
    count = 0
    frame = grayFramesQueue.dequeue()
    while frame is not None:
        print(f'Displaying frame {count}')
        image = cv2.imdecode(frame, cv2.IMREAD_UNCHANGED)
        cv2.imshow('Video', image)
        if cv2.waitKey(42) and 0xFF == ord("q"):
            break
        count +=1

        frame = grayFramesQueue.dequeue()
    cv2.destroyAllWindows()


extractThread = Thread(target = extractFrames, args = (clipFileName, readFramesQueue)).start()
grayFramesThread = Thread(target = convertToGrayScale, args = (readFramesQueue, grayFramesQueue)).start()
displayThread = Thread(target = displayFrames, args = (grayFramesQueue,)).start()
