# -*- coding: utf-8 -*-
"""
Created on Sun Jan 14 21:20:03 2024

@author: Admin
"""

import cv2
import mediapipe as mp

# Inicializar la biblioteca de MediaPipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Inicializar la cámara
cap = cv2.VideoCapture(0)

# Variables para el promedio de landmarks
alpha = 0.7
prev_hand_landmarks = None

while cap.isOpened():
    # Leer un frame de la cámara
    ret, frame = cap.read()
    if not ret:
        continue

    # Convertir el frame a RGB (MediaPipe requiere imágenes en formato RGB)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Detectar las manos en el frame
    results = hands.process(rgb_frame)

    # Contador de dedos levantados
    raised_fingers = 0

    # Verificar si se detectaron manos
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Promedio de landmarks para mejorar la estabilidad
            if prev_hand_landmarks:
                for i in range(len(hand_landmarks.landmark)):
                    hand_landmarks.landmark[i].x = alpha * hand_landmarks.landmark[i].x + (1 - alpha) * prev_hand_landmarks.landmark[i].x
                    hand_landmarks.landmark[i].y = alpha * hand_landmarks.landmark[i].y + (1 - alpha) * prev_hand_landmarks.landmark[i].y

            # Evaluar cuántos dedos están levantados
            if prev_hand_landmarks:
                # Evaluar la posición de los dedos
                thumb_tip = hand_landmarks.landmark[4]
                index_tip = hand_landmarks.landmark[8]
                middle_tip = hand_landmarks.landmark[12]
                ring_tip = hand_landmarks.landmark[16]
                pinky_tip = hand_landmarks.landmark[20]

                # Contar dedos levantados
                raised_fingers = sum(1 for tip in [thumb_tip, index_tip, middle_tip, ring_tip, pinky_tip] if tip.y < prev_hand_landmarks.landmark[4].y)

                # Aplicar suavizado a la cuenta de dedos levantados
                raised_fingers = int(alpha * raised_fingers + (1 - alpha) * raised_fingers)

                # Mostrar el número de dedos levantados
                cv2.putText(frame, f'Dedos Levantados: {raised_fingers}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

            # Almacenar la posición actual de la mano para la próxima iteración
            prev_hand_landmarks = hand_landmarks

    # Mostrar el frame con las manos detectadas
    cv2.imshow('Hand Tracking', frame)

    # Salir si se presiona la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar recursos
cap.release()
cv2.destroyAllWindows()

