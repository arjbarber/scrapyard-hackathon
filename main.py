import pygame
import cv2
import config
import sys

pygame.init()

WIN = pygame.display.set_mode((config.WIDTH, config.HEIGHT))#,pygame.FULLSCREEN)

def draw_screen(frame):
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = cv2.transpose(frame)
    frame = pygame.surfarray.make_surface(frame)
    frame = pygame.transform.scale(frame, (config.WIDTH, config.HEIGHT))
    WIN.blit(frame, (0, 0))
    pygame.display.update()

def initialize_camera():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open camera.")
        pygame.quit()
        sys.exit()
        return None
    return cap

def main():
    pygame.display.set_caption("Pygame Camera App")
    #capture_button = pygame.rect.Rect(config.)
    clock = pygame.time.Clock()

    cap = initialize_camera()

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
        

        draw_screen(frame)
    
    cap.release()
    pygame.quit()

if __name__ == "__main__":
    main()