import random
import cv2
import mediapipe
import pygame
import threading
import sys
import os

os.system('clear' if os.name == 'posix' else 'cls')  # 'clear' for macOS/Linux, 'cls' for Windows
print("The app is working...")

pygame.mixer.init()

def resource_path(relative_path):
    """Get the absolute path to a resource, works for PyInstaller."""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

# Update the audio file loading
def play_random_audio():
    def _play():
        file_name = resource_path(f"audio{random.randint(1, 7)}.mp3")
        pygame.mixer.music.load(file_name)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

    threading.Thread(target=_play).start()

mp_face_mesh = mediapipe.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh()

left_played = False
right_played = False

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb_frame)

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            nose = face_landmarks.landmark[1]
            if nose.x < 0.35 and not left_played:
                left_played = True
                right_played = False
                play_random_audio()
            elif nose.x > 0.65 and not right_played:
                right_played = True
                left_played = False
                play_random_audio()

    if cv2.waitKey(5) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()