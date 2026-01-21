import cv2
import mediapipe as mp

class HandTracker:
    def __init__(self, max_hands=1, detection_conf=0.7, track_conf=0.7):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            max_num_hands=max_hands,
            min_detection_confidence=detection_conf,
            min_tracking_confidence=track_conf
        )
        self.mp_draw = mp.solutions.drawing_utils

    def process(self, img, draw=True):
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = self.hands.process(img_rgb)

        lm_list = []
        index_pos = None

        if results.multi_hand_landmarks and results.multi_handedness:
            for hand_lms, handed in zip(results.multi_hand_landmarks,
                                        results.multi_handedness):

                label = handed.classification[0].label

                if draw:
                    self.mp_draw.draw_landmarks(
                        img, hand_lms, self.mp_hands.HAND_CONNECTIONS
                    )

                if label == "Right":
                    h, w, _ = img.shape
                    for id, lm in enumerate(hand_lms.landmark):
                        cx, cy = int(lm.x * w), int(lm.y * h)
                        lm_list.append((id, cx, cy))

                    ix, iy = lm_list[8][1], lm_list[8][2]  # index tip
                    index_pos = (ix, iy)

        return index_pos, lm_list
