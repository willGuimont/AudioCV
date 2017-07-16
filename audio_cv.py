import cv2
import time

from vision.detector import Detector
from piano.piano import Piano
from note.note import Note
from note.notes_defines import NoteDefines
from regions.region import Region

video_capture = cv2.VideoCapture(0)
detector = Detector()
piano = None
last_time = time.time()

while video_capture.isOpened():

    ret, frame = video_capture.read()

    if not ret:
        break

    if piano is None:
        height, width, channels = frame.shape
        third = int(width / 3)
        regions = [Region((0, 0), (third, height)), Region((2 * third, 0), (width, height))]
        notes = [Note(NoteDefines.C4), Note(NoteDefines.E4)]
        piano = Piano(regions, notes, use_audio=True, filepath="midi/test_01.mid")


    positions, draw, thresh = detector.detect(frame, 2)

    new_time = time.time()
    dt = new_time - last_time

    piano.update(positions, dt)
    piano.draw(draw)

    last_time = new_time

    cv2.imshow("Draw", draw)
    cv2.imshow("Thresh", thresh)

    key = cv2.waitKey(10)
    if key == 32:  # Space to save the position
        pass
    elif key == 27:  # Escape to stop the detection
        piano.close()
        break
    elif key == ord('s'):  # S to skip the frame, useful is the first frame isn't good
        pass
