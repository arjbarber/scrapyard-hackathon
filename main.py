import pygame
import config
pygame.init()

WIN = pygame.display.set_mode((config.WIDTH, config.HEIGHT))

def draw_screen():
    WIN.fill(config.BACKGROUND_COLOR)
    pygame.display.update()

def main():
    
    pygame.display.set_caption("Pygame App")
    clock = pygame.time.Clock()

    run = True
    while run:
        clock.tick(config.FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        draw_screen()
    
    pygame.quit()

if __name__ == "__main__":
    main()