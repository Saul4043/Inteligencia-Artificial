# -*        - coding: utf-8 -*-
"""
Created on Sat Jan 27 10:09:26 2024

@author: Admin
"""

import cv2
import mediapipe as mp

# Inicializar el módulo de detección de manos de mediapipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

# Iniciar la cámara
cap = cv2.VideoCapture(0)

# Definir el alfabeto
alfabeto = {
    0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E',
    5: 'F', 6: 'G', 7: 'H', 8: 'I', 9: 'J',
    10: 'K', 11: 'L', 12: 'M', 13: 'N', 14: 'O',
    15: 'P', 16: 'Q', 17: 'R', 18: 'S', 19: 'T',
    20: 'U', 21: 'V', 22: 'W', 23: 'X', 24: 'Y', 25: 'Z'
}

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Convertir el fotograma a color (BGR a RGB)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Detección de manos utilizando mediapipe
    results = hands.process(rgb_frame)

    # Verificar si se han detectado manos
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Obtener la posición de las puntas de los dedos
            finger_tip_positions = [(int(landmark.x * frame.shape[1]), int(landmark.y * frame.shape[0]))
                                     for landmark in hand_landmarks.landmark[8:]]  # Puntas de los dedos (8 en adelante)

           # Traducir la posición de los dedos a letras del alfabeto
            letra_detectada = alfabeto.get(round(hand_landmarks.landmark[8].x * 25))

          
                
                

            # Mostrar la letra detectada
            cv2.putText(frame, letra_detectada, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
    
                # Dibujar la mano en la imagen
            mp_drawing = mp.solutions.drawing_utils
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
    
    # Mostrar el fotograma con las manos detectadas
    cv2.imshow("Traductor de Movimientos con Letras", frame)

    # Salir del bucle si se presiona la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar los recursos
cap.release()
cv2.destroyAllWindows()