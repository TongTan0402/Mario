import pygame

# Khởi tạo Pygame
pygame.init()

clock = pygame.time.Clock()

# Tạo cửa sổ game
screen = pygame.display.set_mode((800, 600))

# Tạo một Surface mới với kích thước là (50, 50)
rectangle_surface = pygame.Surface((800, 600))
img = pygame.image.load("images/player/mario_2.png")
img = pygame.transform.scale(img, (100,100))

# Đặt độ trong suốt cho Surface (0 = hoàn toàn trong suốt, 255 = hoàn toàn không trong suốt)

# Vẽ hình chữ nhật trên Surface với màu trắng
# pygame.draw.rect(rectangle_surface, (0, 0, 0), (0, 0, 800, 600))

run = True
i = 0
direction = 5
while run:
    screen.fill((255,255,255))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    i += direction
    if i > 255 or i < 0: 
        direction *= -1
        i += direction
    rectangle_surface.fill((0,0,0))
    rectangle_surface.set_alpha(i)

    # Vẽ Surface lên cửa sổ game
    screen.blit(img, (200,200))
    screen.blit(rectangle_surface, (0, 0))

    clock.tick(60)

    pygame.display.update()
