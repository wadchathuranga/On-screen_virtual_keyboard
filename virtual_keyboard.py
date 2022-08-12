import cv2
from cvzone.HandTrackingModule import HandDetector
from time import sleep
from pynput.keyboard import Controller
import pyttsx3


cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

detector = HandDetector(detectionCon=0.8)

keys = [["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"],
        ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
        ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";"],
        ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/"]]


# keys = [["q", "w", "e", "r", "t", "y", "u", "i", "o", "p"],
#         ["a", "s", "d", "f", "g", "h", "j", "k", "l", ";"],
#         ["z", "x", "c", "v", "b", "n", "m", ",", ".", "/"]]

finalText = ""

# keyboard typing
keyboard = Controller()

# Voice
player = pyttsx3.init()

# Voice variation customize
voices = player.getProperty('voices')
player.setProperty('voice', voices[0].id)   # voices[0] for male, voices[1] for female. Default it is set for male voice


def drawAll(img, buttonList):
    for button in buttonList:
        x, y = button.pos
        w, h = button.size
        cv2.rectangle(img, button.pos, (x + w, y + h), (100, 0, 50), cv2.FILLED)
        cv2.putText(img, button.text, (x + 10, y + 55), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
    return img


class Button():
    def __init__(self, pos, text, size=[85, 85]):
        self.pos = pos
        self.text = text
        self.size = size


buttonList = []

for i in range(len(keys)):
    for j, key in enumerate(keys[i]):
        buttonList.append(Button([100 * j + 50, 100 * i + 50], key))

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList, bboxInfo = detector.findPosition(img)

    img = drawAll(img, buttonList)

    if lmList:
        for button in buttonList:
            x, y = button.pos
            w, h = button.size

            if x < lmList[8][0] < x + w and y < lmList[8][1] < y + h:
                cv2.rectangle(img, (x-5, y-5), (x + w + 5, y + h + 5), (175, 0, 175), cv2.FILLED)
                cv2.putText(img, button.text, (x + 10, y + 55), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)

                distance, _, _ = detector.findDistance(8, 12, img, draw=False)
                print(distance)

                # When clicked
                if distance < 50:
                    keyboard.press(button.text)
                    cv2.rectangle(img, button.pos, (x + w, y + h), (0, 225, 0), cv2.FILLED)
                    cv2.putText(img, button.text, (x + 10, y + 55), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
                    finalText += button.text
                    player.say(button.text)   # voice pressed button

                    player.runAndWait()    # voice
                    sleep(0.20)

    # Display canvas to display what characters types
    # cv2.rectangle(img, (50, 450), (1035, 550), (100, 0, 50), cv2.FILLED)
    # cv2.putText(img, finalText, (60, 520), cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 5)

    cv2.imshow('Image', img)
    close = cv2.waitKey(1)
    if close & 0xff == ord('q') or close == 27:
        break
