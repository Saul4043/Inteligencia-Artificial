# -*- coding: utf-8 -*-
"""
Created on Wed Jan 24 23:11:29 2024

@author: Admin
"""
import cv2
import mediapipe as mp

# Inicializar el módulo de detección de manos de mediapipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

# Configurar la captura de video desde la cámara
cap = cv2.VideoCapture(0)

# Números asociados a cada dedo (en orden de índice)
numeros_dedos = {
    0: 0,  # Pulgar
    1: 1,  # Índice
    2: 2,  # Medio
    3: 3,  # Anular
    4: 4   # Meñique
}

# Bucle principal
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Convertir la imagen a escala de grises
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Procesar la imagen para detectar manos
    results = hands.process(frame_rgb)

    # Verificar si se detectaron manos
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Contar dedos levantados
            dedos_levantados = []
            for idx, lm in enumerate(hand_landmarks.landmark):
                if lm.y < hand_landmarks.landmark[0].y:  # Comprobar si el punto está por encima de la muñeca
                    dedos_levantados.append(numeros_dedos.get(idx, -1))

            # Concatenar los números de los dedos levantados
            numero_dedo = int(''.join(map(str, dedos_levantados)))

            # Mostrar el número de dedo
            cv2.putText(frame, f'Número: {numero_dedo}', (50, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    # Mostrar el frame procesado
    cv2.imshow('Conteo de Dedos', frame)

    # Salir del bucle al presionar 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar recursos
cap.release()
cv2.destroyAllWindows()
