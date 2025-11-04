import mediapipe as mp
import cv2

mp_draw = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

with mp_hands.Hands(
    static_image_mode=True,
    max_num_hands=2,
    min_detection_confidence=0.5) as hands:

    image = cv2.imread('images/hand6.jpg')
    height, width, _ = image.shape
    image = cv2.flip(image, 1)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image_rgb)

    print('Handedness:', results.multi_handedness, results.multi_hand_landmarks)

    # Voltear la imagen de vuelta a su orientación original ANTES de dibujar
    image = cv2.flip(image, 1)

    if results.multi_hand_landmarks is not None:

        # Definir los índices de las puntas de los dedos
        fingertips = {
            'THUMB': mp_hands.HandLandmark.THUMB_TIP,      # índice 4
            'INDEX': mp_hands.HandLandmark.INDEX_FINGER_TIP,  # índice 8
            'MIDDLE': mp_hands.HandLandmark.MIDDLE_FINGER_TIP, # índice 12
            'RING': mp_hands.HandLandmark.RING_FINGER_TIP,   # índice 16
            'PINKY': mp_hands.HandLandmark.PINKY_TIP       # índice 20
        }

        # Colores para cada dedo (formato BGR)
        colors = {
            'THUMB': (255, 0, 0),    # Azul
            'INDEX': (0, 255, 0),    # Verde
            'MIDDLE': (0, 0, 255),   # Rojo
            'RING': (255, 255, 0),   # Cyan
            'PINKY': (255, 0, 255)   # Magenta
        }

        # Iterar sobre cada mano detectada
        for hand_landmarks in results.multi_hand_landmarks:
            print('Hand landmarks:', hand_landmarks)

            # Dibujar solo las puntas de los dedos
            for finger_name, finger_landmark in fingertips.items():
                # Obtener las coordenadas normalizadas (0-1)
                landmark = hand_landmarks.landmark[finger_landmark]

                # Convertir a coordenadas de píxeles
                # IMPORTANTE: Invertir la coordenada X porque la imagen ya está volteada
                x = int((1 - landmark.x) * width)
                y = int(landmark.y * height)

                # Dibujar círculo en la punta del dedo
                cv2.circle(image, (x, y), 12, colors[finger_name], -1)  # -1 rellena el círculo

                # Dibujar borde del círculo en negro para mejor contraste
                cv2.circle(image, (x, y), 12, (0, 0, 0), 2)

                # Agregar etiqueta de texto
                cv2.putText(image, finger_name, (x - 30, y - 20),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)


cv2.imshow('Image-gera', image)
cv2.waitKey(0)
