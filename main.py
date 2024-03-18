import cv2
import mediapipe as mp
import pyautogui
import time

# Initialize MediaPipe Hands.
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7)

# Initialize drawing utils.
mp_draw = mp.solutions.drawing_utils

# Start capturing video.
cap = cv2.VideoCapture(1)

# Adjust the action threshold and cooldown as needed.
action_threshold =  10 # Lower this if gestures are not being recognized.
last_action = time.time()
action_cooldown = 0.1  # Decrease this if actions are missed due to quick succession.

def get_gesture(landmarks):
    wrist = landmarks[mp_hands.HandLandmark.WRIST]
    index_tip = landmarks[mp_hands.HandLandmark.INDEX_FINGER_TIP]

    # Visual feedback for key points
    cv2.circle(image, (int(wrist.x * width), int(wrist.y * height)), 10, (0, 0, 255), -1)
    cv2.circle(image, (int(index_tip.x * width), int(index_tip.y * height)), 10, (0, 255, 0), -1)

    # Gesture detection
    if index_tip.y < wrist.y - action_threshold / height:
        return 'up'
    elif index_tip.y > wrist.y + action_threshold / height:
        return 'down'
    elif index_tip.x < wrist.x - action_threshold / width:
        return 'left'
    elif index_tip.x > wrist.x + action_threshold / width:
        return 'right'
    return None

while True:
    success, image = cap.read()
    if not success:
        print("Ignoring empty camera frame.")
        continue

    height, width, _ = image.shape
    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
    results = hands.process(image)

    gesture_text = "Gesture: None"
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            
            gesture = get_gesture(hand_landmarks.landmark)
            if gesture and (time.time() - last_action) > action_cooldown:
                gesture_text = f"Gesture Detected: {gesture}"
                print(gesture_text)
                if gesture == 'up':
                    pyautogui.press('up')
                elif gesture == 'down':
                    pyautogui.press('down')
                elif gesture == 'left':
                    pyautogui.press('left')
                elif gesture == 'right':
                    pyautogui.press('right')
                last_action = time.time()

    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    cv2.putText(image, gesture_text, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.imshow('Hand Gesture Subway Surfers Controller', image)

    if cv2.waitKey(5) & 0xFF == 113:
        break

cap.release()
cv2.destroyAllWindows()
