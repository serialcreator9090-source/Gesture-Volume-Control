
import cv2
import mediapipe as mp
import numpy as np
from math import hypot
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


class VolumeHandControl:
    def __init__(
        self,
        maxHands=2,
        detectionCon=0.75,
        trackCon=0.75
    ):
        # MediaPipe setup
        self.mpHands = mp.solutions.hands
        self.mpDraw = mp.solutions.drawing_utils

        self.hands = self.mpHands.Hands(
            static_image_mode=False,
            model_complexity=1,
            max_num_hands=maxHands,
            min_detection_confidence=detectionCon,
            min_tracking_confidence=trackCon
        )

        self.lmList = []

        # Windows system volume setup
        devices = AudioUtilities.GetSpeakers()
        self.volume = devices.EndpointVolume.QueryInterface(
            IAudioEndpointVolume
        )

        volRange = self.volume.GetVolumeRange()
        self.minVol = volRange[0]
        self.maxVol = volRange[1]

    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        if draw and self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                self.mpDraw.draw_landmarks(
                    img,
                    handLms,
                    self.mpHands.HAND_CONNECTIONS
                )

        return img

    def findPosition(self, img, handNo=0):
        self.lmList = []

        if (
            not hasattr(self, "results")
            or not self.results.multi_hand_landmarks
            or handNo >= len(self.results.multi_hand_landmarks)
        ):
            return self.lmList

        myHand = self.results.multi_hand_landmarks[handNo]
        h, w, _ = img.shape

        for id, lm in enumerate(myHand.landmark):
            cx = int(lm.x * w)
            cy = int(lm.y * h)
            self.lmList.append([id, cx, cy])

        return self.lmList

    def findDistance(self, p1, p2, img, draw=True):
        if not self.lmList or max(p1, p2) >= len(self.lmList):
            return 0, img, []

        x1, y1 = self.lmList[p1][1:]
        x2, y2 = self.lmList[p2][1:]

        cx = (x1 + x2) // 2
        cy = (y1 + y2) // 2

        length = hypot(x2 - x1, y2 - y1)

        if draw:
            cv2.circle(img, (x1, y1), 10, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), 10, (255, 0, 255), cv2.FILLED)
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
            cv2.circle(img, (cx, cy), 8, (0, 255, 0), cv2.FILLED)

        return length, img, [x1, y1, x2, y2, cx, cy]

    def controlVolume(self, img, draw=True):
        length, img, _ = self.findDistance(4, 8, img, draw)

        if not self.lmList or length == 0:
            return img

        # Map finger distance to the system volume range
        vol = np.interp(
            length,
            [50, 300],
            [self.minVol, self.maxVol]
        )

        self.volume.SetMasterVolumeLevel(float(vol), None)

        volPer = int(np.interp(length, [50, 300], [0, 100]))
        volPer = max(0, min(100, volPer))

        if draw:
            cv2.putText(
                img,
                f"Volume: {volPer}%",
                (40, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2
            )

        return img

    def close(self):
        self.hands.close()


def main():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    detector = None

    try:
        detector = VolumeHandControl()

        while True:
            success, img = cap.read()

            if not success:
                break

            img = cv2.flip(img, 1)

            img = detector.findHands(img)
            detector.findPosition(img, handNo=0)
            img = detector.controlVolume(img)

            cv2.imshow("Gesture Volume Control", img)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    except Exception as e:
        print(f"Error: {e}")

    finally:
        if detector is not None:
            detector.close()

        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
