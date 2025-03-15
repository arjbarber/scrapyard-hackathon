import pygame
import mediapipe as mp
import cv2
import config
import numpy as np
import sys
import os
pygame.init()

try:
    os.mkdir("images")
except FileExistsError:
    ...

WIN = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5)

ARROW_FONT = pygame.font.SysFont("Times",50)

blink_counter = 0
blink_detected = False

def draw_screen(frame, capture_button: pygame.Rect, blink_detected):
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = cv2.transpose(frame)
    frame = pygame.surfarray.make_surface(frame)
    frame = pygame.transform.scale(frame, (config.WIDTH, config.HEIGHT))
    WIN.blit(frame, (0, 0))
    pygame.draw.circle(WIN, config.CAPTURE_BUTTON_COLOR, capture_button.center, config.CAPTURE_BUTTON_SIZE // 2)
    if blink_detected == False:
        pygame.display.update()
    else:
        pygame.display.update()
        pygame.time.delay(10000)

def initialize_camera():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open camera.")
        pygame.quit()
        sys.exit()
        return None
    return cap


def eye_aspect_ratio(eye_landmarks):
    """Calculate Eye Aspect Ratio (EAR)"""
    def euclidean_dist(p1, p2):
        return np.linalg.norm(np.array(p1) - np.array(p2))

    # Compute vertical and horizontal distances
    vertical_1 = euclidean_dist(eye_landmarks[1], eye_landmarks[5])
    vertical_2 = euclidean_dist(eye_landmarks[2], eye_landmarks[4])
    horizontal = euclidean_dist(eye_landmarks[0], eye_landmarks[3])

    # EAR calculation
    ear = (vertical_1 + vertical_2) / (2.0 * horizontal)
    return ear

def detect_blink(frame):
    """Detects blink in a given cv2 frame"""
    global blink_counter, blink_detected

    height, width, _ = frame.shape
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(frame_rgb)

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            # Convert normalized coordinates to pixel values
            left_eye = [(face_landmarks.landmark[i].x * width, face_landmarks.landmark[i].y * height) for i in config.LEFT_EYE]
            right_eye = [(face_landmarks.landmark[i].x * width, face_landmarks.landmark[i].y * height) for i in config.RIGHT_EYE]

            # Compute EAR for both eyes
            left_ear = eye_aspect_ratio(left_eye)
            right_ear = eye_aspect_ratio(right_eye)
            avg_ear = (left_ear + right_ear) / 2.0

            # Blink detection logic
            if avg_ear < config.EAR_THRESHOLD:
                blink_counter += 1
            else:
                if blink_counter >= config.BLINK_FRAMES:  # Blink confirmed
                    blink_detected = True
                blink_counter = 0  # Reset counter

    return blink_detected

def main():
    global blink_detected
    pygame.display.set_caption("Camera App")
    capture_button = pygame.rect.Rect(
        config.WIDTH // 2 - config.CAPTURE_BUTTON_SIZE // 2,
        config.HEIGHT - config.CAPTURE_BUTTON_SIZE - config.CAPTURE_BUTTON_PADDING,
        config.CAPTURE_BUTTON_SIZE,
        config.CAPTURE_BUTTON_SIZE,
    )

    clock = pygame.time.Clock()
    cap = initialize_camera()
    blink = 0
    not_blink = 0
    run = True
    while run:
        clock.tick(config.FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame.")
            break

        if detect_blink(frame):
            #print(f"{blink}. Blink detected!")
            blink_detected = False
            filepath = os.path.join('images',f'{blink}. frame.jpg')
            cv2.imwrite(filepath, frame)
            blink += 1
        else:
            #print(f"{not_blink}. Blink Not Detected")
            not_blink += 1

        draw_screen(frame, capture_button, blink_detected)

    cap.release()
    pygame.quit()

def browse():
    pygame.init()
    clock = pygame.time.Clock()
    run = True
    ARROW_FONT = pygame.font.Font(None, 50)

    left_arrow = pygame.Rect(config.ARROW_PADDING, config.HEIGHT // 2 - config.ARROW_SIZE // 2, config.ARROW_SIZE, config.ARROW_SIZE)
    right_arrow = pygame.Rect(config.WIDTH - config.ARROW_SIZE - config.ARROW_PADDING, config.HEIGHT // 2 - config.ARROW_SIZE // 2, config.ARROW_SIZE, config.ARROW_SIZE)

    while run:
        clock.tick(config.FPS)
        WIN.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if left_arrow.collidepoint(event.pos):
                    print("Left arrow clicked")
                elif right_arrow.collidepoint(event.pos):
                    print("Right arrow clicked")

        left_text = ARROW_FONT.render("<", True, (255, 255, 255))
        right_text = ARROW_FONT.render(">", True, (255, 255, 255))

        left_text_rect = left_text.get_rect(center=left_arrow.center)
        right_text_rect = right_text.get_rect(center=right_arrow.center)

        pygame.draw.rect(WIN, (100, 100, 100), left_arrow)
        pygame.draw.rect(WIN, (100, 100, 100), right_arrow)

        WIN.blit(left_text, left_text_rect)
        WIN.blit(right_text, right_text_rect)

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    browse()