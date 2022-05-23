import time
import os
import sys

import cv2
import curses

density = 'Ñ@#W$9876543210?!abc;:+=-,._ '


def capture_webcam():
    vid = cv2.VideoCapture(0)

    while(True):
        _, frame = vid.read()
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        if frame is not None:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        yield frame

    vid.release()
    cv2.destroyAllWindows()


def main(stdscr):
    win = curses.newwin(90, 90, 2, 2)
    for frame in capture_webcam():
        if frame is not None:
            frame = cv2.resize(frame, (100, 100))
            frame = frame * 0.4
            height, width = frame.shape
            ascii_img = []
            for y in range(height):
                new_row = []
                for x in range(width):
                    density_idx = round(frame[y, x] / 255 * len(density))
                    new_row.append(density[len(density) - density_idx - 1])
                ascii_img.append(new_row)
            for index, row in enumerate(ascii_img):
                if row:
                    try:
                        win.addstr(index, 0, "".join(row)+"\n")
                    except curses.error:
                        pass
            win.refresh()


curses.wrapper(main)
