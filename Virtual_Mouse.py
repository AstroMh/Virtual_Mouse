import cv2
from math import hypot
import mediapipe as mp
import pyautogui as pg
from pynput.mouse import Button, Controller

#Variables
cap = cv2.VideoCapture(0)
mpDraw = mp.solutions.drawing_utils
mpHands = mp.solutions.hands
mouse = Controller()
screen_width, screen_height = pg.size()
pg.FAILSAFE = False

#Setting up
with mpHands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
    while True:
        ret, img = cap.read()
        img = cv2.flip(img, 1)
        img_width, img_height, _ = img.shape
        image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(image)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        lmlist = []
        print(results.multi_hand_landmarks)

        #Drawing landmarks
        if results.multi_hand_landmarks:
            for handlandmark in results.multi_hand_landmarks:
                for id,lm in enumerate(handlandmark.landmark):
                    h, w,_ = img.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    lmlist.append([id, cx, cy])
                mpDraw.draw_landmarks(image, handlandmark, mpHands.HAND_CONNECTIONS,
                                      mpDraw.DrawingSpec(color= (19, 47, 209), thickness= 2, circle_radius= 2 ),
                                      mpDraw.DrawingSpec(color= (10, 173, 19), thickness= 2, circle_radius= 2))

        #Connecting the tip of each finger together
        if lmlist != []:
            if results.multi_hand_landmarks:
                x1, y1 = lmlist[4][1],lmlist[4][2]
                x2, y2 = lmlist[8][1], lmlist[8][2]
                cv2.circle(image, (x1, y1), 4, (255, 255, 255), cv2.FILLED)
                cv2.circle(image, (x2, y2), 4, (255, 255, 255), cv2.FILLED)
                x3, y3 = lmlist[4][1], lmlist[4][2]
                x4, y4 = lmlist[12][1], lmlist[12][2]
                cv2.circle(image, (x3, y3), 4, (255, 255, 255), cv2.FILLED)
                cv2.circle(image, (x4, y4), 4, (255, 255, 255), cv2.FILLED)
                x5, y5 = lmlist[4][1], lmlist[4][2]
                x6, y6 = lmlist[20][1], lmlist[20][2]
                cv2.circle(image, (x5, y5), 4, (255, 255, 255), cv2.FILLED)
                cv2.circle(image, (x6, y6), 4, (255, 255, 255), cv2.FILLED)
                cv2.line(image, (x1, y1), (x2, y2), (230, 92, 124), 1)
                cv2.line(image, (x3, y3), (x4, y4), (139, 34, 214), 1)
                cv2.line(image, (x5, y5), (x6, y6), (135, 219, 44), 1)

                #Calculating the distance between two fingers
                length = hypot(x2-x1, y2-y1)
                length1 = hypot(x4-x3, y4-y3)
                length2 = hypot(x6-x5, y6-y5)

                #Different type of clicks and releases
                if length1 <= 30:
                    if length2 <= 30:
                        mouse.press(Button.left)
                    else:
                        mouse.click(Button.left)
                elif length2 > 80:
                    mouse.release(Button.left)

                #Moving the mouse if conditions are met
                if length <= 30:
                    x = screen_width/img_width*x1
                    y = screen_height/img_height*y1
                    pg.moveTo(x, y)
                    
        if cv2.waitKey(10) & 0xff==ord('q'):
            break
        
cap.release()
cv2.destroyAllWindows()
