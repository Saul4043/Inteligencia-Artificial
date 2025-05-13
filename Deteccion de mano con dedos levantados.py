# -*- coding: utf-8 -*-
"""
Created on Sat Jan 20 21:09:09 2024

@author: Admin
"""

import cv2
import numpy as np
import mediapipe as mp

# Configurar el módulo de mediapipe para la detección de manos
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

# Inicializar la cámara
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

# Definir gestos asociados con traducciones
gestos_a_traducciones = {
    'puño': '¡Detente!',
    'paz': 'Paz',
    'dedo_índice': 'Señal',
    'dedo_medio': 'Insulto',
    'dedo_anular': 'Espera',
    'dedo_menique': 'Pequeño'
    # Agrega más gestos y traducciones según sea necesario
}

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Convertir la imagen a color si no tiene 3 canales (RGB)
    if frame.shape[2] != 3:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Obtener las coordenadas de las manos
    results = hands.process(frame)

    # Preprocesar la imagen para la detección de gestos
    if results.multi_hand_landmarks:
        for landmarks in results.multi_hand_landmarks:
            hand_landmarks = np.array([[landmark.x, landmark.y, landmark.z] for landmark in landmarks.landmark])
            hand_landmarks = hand_landmarks.flatten()

            # Normalizar las coordenadas de las manos
            hand_landmarks_normalized = hand_landmarks / hand_landmarks.max()

            # Comparar con gestos predefinidos y mostrar traducción
            for gesto, traduccion in gestos_a_traducciones.items():
                # Ejemplo de condición (ajusta según tus necesidades)
                if gesto_correspondiente(hand_landmarks_normalized, gesto):
                    cv2.putText(frame, f'Traducción: {traduccion}', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

    # Mostrar el frame con la traducción
    cv2.imshow('Gesture Translator', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
