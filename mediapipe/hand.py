import mediapipe as mp
import cv2

mp_draw = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

with mp_hands.Hands(
    static_image_mode=True,
    max_num_hands=2,
    min_detection_confidence=0.5) as hands:

    image = cv2.imread('images/hand3.jpg')
    height, width, _ = image.shape
    image = cv2.flip(image, 1)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image_rgb)
    
    print('Handedness:', results.multi_handedness, results.multi_hand_landmarks)
    
    if results.multi_hand_landmarks is not None:


        ### Testing
        for hand_landmarks in results.multi_hand_landmarks:
            print('Hand landmarks:', hand_landmarks)
            mp_draw.draw_landmarks(
                image, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                mp_draw.DrawingSpec(color=(121, 22, 76), thickness=5, circle_radius=8),
                mp_draw.DrawingSpec(color=(250, 44, 250), thickness=5))
            
            #x1 = int(hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x * width)
            #print(x1)
    image = cv2.flip(image, 1)

    
cv2.imshow('Image-gera', image)
cv2.waitKey(0)