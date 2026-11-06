import pygame

pygame.init()                                   # spustí Pygame
screen = pygame.display.set_mode((800, 600))    # okno 800×600 px
pygame.display.set_caption("Lovec mincí")
clock = pygame.time.Clock()                     # hlídá rychlost smyčky

running = True
while running:                                  # herní smyčka – jeden průchod = jeden snímek
    for event in pygame.event.get():            # projde vše, co uživatel udělal
        if event.type == pygame.QUIT:           # kliknul na křížek
            running = False

    screen.fill((30, 30, 60))                   # vybarví pozadí (R, G, B)
    pygame.display.flip()                       # ukáže nakreslené na obrazovce
    clock.tick(60)                              # max 60 snímků za sekundu

pygame.quit()