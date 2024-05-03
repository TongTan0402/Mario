import pygame
import os
import os.path

pygame.init()

clock = pygame.time.Clock()

start = True

path = "level/level_2.1.csv"

pixel_width = 20
pixel_height = 15

tiles_per_length = 40
tiles_per_width = 40
map_width = pixel_width * tiles_per_length
map_height = pixel_height * tiles_per_width

screen_width = 1290
screen_height = 700

screen = pygame.display.set_mode((screen_width, screen_height))

main_screen = pygame.Surface((pixel_width * 40,pixel_height * 40))
main_screen_rect = main_screen.get_rect()
(main_screen_rect.x, main_screen_rect.y) = (30,20)
secondary_screen = pygame.Surface((int(pixel_width / 2) * 40, int(pixel_height / 2) * 40))
secondary_screen_rect = secondary_screen.get_rect()
(secondary_screen_rect.x, secondary_screen_rect.y) = (860,20)
tile_screen = pygame.Surface((310, 300), pygame.SRCALPHA)
tile_screen_rect = tile_screen.get_rect()
(tile_screen_rect.x, tile_screen_rect.y) = (860 + secondary_screen_rect.width // 2 - tile_screen_rect.width // 2,40*7 + 40)

class World():
    def __init__(self):
        self.reset()

    def reset(self):
        self.platform_list = []
        self.detail_list = []
        self.hidden_list =[]
        dx = int(display.delta / 2)

        with open(path,"r") as map:
            row_count = 0
            for row in map:
                col_count = 0
                row = row.split(',')
                for tile in row:
                    try:
                        platform_img = pygame.image.load(f"images/background/{tile}-platform.png")
                        platform_img = pygame.transform.scale(platform_img,(int(pixel_width / 2), int(pixel_height / 2)))
                        platform_img_rect = platform_img.get_rect()
                        platform_img_rect.x = col_count * int(pixel_width / 2) - dx
                        platform_img_rect.y = row_count * int(pixel_height / 2)
                        infor = (platform_img, platform_img_rect)
                        self.platform_list.append(infor)
                    except:
                        pass
                    try:
                        detail_img = pygame.image.load(f"images/background/{tile}-detail.png")
                        detail_img = pygame.transform.scale(detail_img,(int(pixel_width / 2), int(pixel_height / 2)))
                        detail_img_rect = detail_img.get_rect()
                        detail_img_rect.x = col_count * int(pixel_width / 2) - dx
                        detail_img_rect.y = row_count * int(pixel_height / 2)
                        infor = (detail_img, detail_img_rect)
                        self.detail_list.append(infor)
                    except:
                        pass 
                    try:
                        hidden_img = pygame.image.load(f"images/test images/test/54-hidden.png")
                        hidden_img = pygame.transform.scale(hidden_img,(int(pixel_width / 2), int(pixel_height / 2)))
                        hidden_img_rect = hidden_img.get_rect()
                        hidden_img_rect.x = col_count * int(pixel_width / 2) - dx
                        hidden_img_rect.y = row_count * int(pixel_height / 2)
                        hidden_img_rect.width = int(pixel_width / 2)
                        hidden_img_rect.height = int(pixel_height / 2)
                        infor = (hidden_img, hidden_img_rect)
                        self.hidden_list.append(infor)
                    except:
                        pass
                    if tile == '29' or tile == '30' or tile == '31' or tile == '32':
                        platform_img = pygame.image.load(f"images/background/secret.png")
                        platform_img = pygame.transform.scale(platform_img,(int(pixel_width / 2), int(pixel_height / 2)))
                        platform_img_rect = platform_img.get_rect()
                        platform_img_rect.x = col_count * int(pixel_width / 2) - dx
                        platform_img_rect.y = row_count * int(pixel_height / 2)
                        infor = (platform_img, platform_img_rect)
                        self.platform_list.append(infor)
                    if tile == '21':
                        platform_img = pygame.image.load(f"images/background/21-brick.png")
                        platform_img = pygame.transform.scale(platform_img,(int(pixel_width / 2), int(pixel_height / 2)))
                        platform_img_rect = platform_img.get_rect()
                        platform_img_rect.x = col_count * int(pixel_width / 2) - dx
                        platform_img_rect.y = row_count * int(pixel_height / 2)
                        infor = (platform_img, platform_img_rect)
                        self.platform_list.append(infor)
                    if tile == '58':
                        platform_img = pygame.image.load(f"images/coin/coin_1.png")
                        platform_img = pygame.transform.scale(platform_img,(int(pixel_width / 2), int(pixel_height / 2)))
                        platform_img_rect = platform_img.get_rect()
                        platform_img_rect.x = col_count * int(pixel_width / 2) - dx
                        platform_img_rect.y = row_count * int(pixel_height / 2)
                        infor = (platform_img, platform_img_rect)
                        self.detail_list.append(infor)
                    if tile == '16' or tile == '19' or tile == '20': # up and down
                        flying_platform = Flying_platform(col_count * int(pixel_width / 2) - dx, row_count * int(pixel_height / 2), 1, 0)
                        flying_platform_group.add(flying_platform)
                    if tile == '15' or tile == '17' or tile == '18': # left and right
                        flying_platform = Flying_platform(col_count * int(pixel_width / 2) - dx, row_count * int(pixel_height / 2), 0, 1)
                        flying_platform_group.add(flying_platform)
                    if tile == '59':
                        enermy = Enermy(col_count * int(pixel_width / 2) - dx, row_count * int(pixel_height / 2))
                        enermy_group.add(enermy)
                    if tile == '41' or tile == '42' or tile == '43':
                        for i in range(-1,2):
                            for j in range(-1, 2):
                                waterfall = Waterfall((col_count + j) * int(pixel_width / 2) - dx, (row_count - i) * int(pixel_height / 2), tile)
                                waterfall_group.add(waterfall)
                    if tile == '44':
                        for i in range(-1,2):
                            if i == 0 or row[col_count + i] != tile:
                                still_water = Still_water((col_count + i) * int(pixel_width / 2) - dx, row_count * int(pixel_height / 2))
                                still_water_group.add(still_water)
                    if tile == '50' or tile == '51': # above (50: auto)
                        spike_trap = Spike_trap(col_count * int(pixel_width / 2) - dx, row_count * int(pixel_height / 2), int(tile) - 50)
                        spike_trap_group.add(spike_trap)
                    if tile == '52' or tile == '53': # below (53: auto)
                        spike_trap = Spike_trap(col_count * int(pixel_width / 2) - dx, row_count * int(pixel_height / 2), int(tile) - 53)
                        spike_trap_group.add(spike_trap)
                    if tile == '45' or tile == '46' or tile == '47':
                        for i in range(-1,2):
                            for j in range(-1, 2):
                                lava = Lava_waterfall((col_count + j) * int(pixel_width / 2) - dx, (row_count - i) * int(pixel_height / 2), tile)
                                lava_waterfall_group.add(lava)
                    if tile == '48':
                        for i in range(-1,2):
                            if i == 0 or row[col_count + i] != tile:
                                lava = Lava((col_count + i) * int(pixel_width / 2) - dx, row_count * int(pixel_height / 2))
                                lava_group.add(lava)
                    if tile == '60':
                        carnivorous_plant = Carnivorous_plant(col_count * int(pixel_width / 2) - dx, row_count * int(pixel_height / 2))
                        carnivorous_plant_group.add(carnivorous_plant)
                    col_count += 1

                row_count +=1
                self.col = col_count -1

    # draw world
    def draw(self):
        # check move
        if display.move:
            key = pygame.key.get_pressed()
            if key[pygame.K_LEFT]:
                for tile in self.platform_list:
                    tile[1].x += int(pixel_width / 2)
                for tile in self.detail_list:
                    tile[1].x += int(pixel_width / 2)
                for tile in self.hidden_list:
                    tile[1].x += int(pixel_width / 2)
            if key[pygame.K_RIGHT]:
                for tile in self.platform_list:
                    tile[1].x -= int(pixel_width / 2)
                for tile in self.detail_list:
                    tile[1].x -= int(pixel_width / 2)
                for tile in self.hidden_list:
                    tile[1].x -= int(pixel_width / 2)

        for tile in self.platform_list:
            secondary_screen.blit(tile[0], tile[1])
        for tile in self.detail_list:
            secondary_screen.blit(tile[0], tile[1])
        for tile in self.hidden_list:
            secondary_screen.blit(tile[0], tile[1])
        screen.blit(secondary_screen,secondary_screen_rect)

class Flying_platform(pygame.sprite.Sprite):
    def __init__(self, x, y, up_down, left_right):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/background/15,16,17,18,19,20-flying_platform.png")
        self.image = pygame.transform.scale(self.image, (int(pixel_width / 2) * 3, int(pixel_height / 2)))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.x = self.rect.x
        self.y = self.rect.y
        self.direction = 1
        self.up_down = up_down # up:1 , down:-1
        self.left_right = left_right # right:1 , left:-1 
        self.limited_distance = 100
        self.count = 0

        self.dx = 0
        self.dy = 0

    def update(self):
        self.dx = 0
        self.dy = 0

        if self.count > self.limited_distance:
            self.count = -1
            self.direction *= -1
        self.count += 1
        self.dx = self.direction * self.left_right
        self.dy = -self.direction * self.up_down
        self.rect.x += self.dx
        self.rect.y += self.dy
        # check move
        if display.move:
            key = pygame.key.get_pressed()
            if key[pygame.K_LEFT]:
                self.rect.x += int(pixel_width / 2)
            if key[pygame.K_RIGHT]:
                self.rect.x -= int(pixel_width / 2)
        
# lava 
class Lava(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.img_list = []
        self.index = 0
        for i in range(4):
            image = pygame.image.load(f"images/background/lava_{i}.png")
            image = pygame.transform.scale(image, (int(pixel_width / 2), int(pixel_height / 2)))
            image.set_alpha(255)
            self.img_list.append(image)
        self.image = self.img_list[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y + 2
        self.count = 0
        self.direction = 1
        self.delay = 10

    def update(self):
        if self.count > self.delay:
            self.count = -1
            self.index += 1
            if self.index > 3:
                self.index = 0
            self.image = self.img_list[self.index]
        self.count += 1
        # check move
        if display.move:
            key = pygame.key.get_pressed()
            if key[pygame.K_LEFT]:
                self.rect.x += int(pixel_width / 2)
            if key[pygame.K_RIGHT]:
                self.rect.x -= int(pixel_width / 2)
        
# lava
class Lava_waterfall(pygame.sprite.Sprite):
    def __init__(self, x, y, tile):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(f"images/background/{tile}-lava_waterfall.png")
        self.image = pygame.transform.scale(self.image, (int(pixel_width / 2), int(pixel_height / 2)))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.count = 0

    def update(self):
        if self.count >= int(pixel_height / 2):
            self.rect.y -= self.count
            self.count = 0

        self.rect.y += 1
        self.count += 1
        # check move
        if display.move:
            key = pygame.key.get_pressed()
            if key[pygame.K_LEFT]:
                self.rect.x += int(pixel_width / 2)
            if key[pygame.K_RIGHT]:
                self.rect.x -= int(pixel_width / 2)

# water 
class Still_water(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.img_list = []
        self.index = 0
        for i in range(5):
            image = pygame.image.load(f"images/background/stillwater_{i}.png")
            image = pygame.transform.scale(image, (int(pixel_width / 2), int(pixel_height / 2)))
            image.set_alpha(150)
            self.img_list.append(image)
        self.image = self.img_list[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y + 2
        self.count = 0
        self.direction = 1
        self.delay = 10

    def update(self):
        if self.count > self.delay:
            self.count = -1
            self.index += self.direction
            if self.index == 0 or self.index == 4:
                self.direction *= -1
            self.image = self.img_list[self.index]
        self.count += 1
        # check move
        if display.move:
            key = pygame.key.get_pressed()
            if key[pygame.K_LEFT]:
                self.rect.x += int(pixel_width / 2)
            if key[pygame.K_RIGHT]:
                self.rect.x -= int(pixel_width / 2)

# water
class Waterfall(pygame.sprite.Sprite):
    def __init__(self, x, y, tile):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(f"images/background/{tile}-waterfall.png")
        self.image = pygame.transform.scale(self.image, (int(pixel_width / 2), int(pixel_height / 2)))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.count = 0

    def update(self):
        if self.count >= int(pixel_height / 2):
            self.rect.y -= self.count
            self.count = 0

        self.rect.y += 1
        self.count += 1
        # check move
        if display.move:
            key = pygame.key.get_pressed()
            if key[pygame.K_LEFT]:
                self.rect.x += int(pixel_width / 2)
            if key[pygame.K_RIGHT]:
                self.rect.x -= int(pixel_width / 2)

# Carnivorous plants
class Carnivorous_plant(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.index = 0
        self.img_list = []
        for i in range(2):
            image = pygame.image.load(f"images/enermy/flower_{i}.png")
            image = pygame.transform.scale(image, (int(pixel_width / 2) + 4, int(pixel_height / 2) + 4))
            self.img_list.append(image)
        self.image = self.img_list[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = x + int(pixel_width / 2) // 2 - 2
        self.rect.y = y + int(pixel_height / 2) + 1
        self.img_count = 0
        self.delay = 5
        self.count = 0
        self.cooldown = 0

    def update(self):
        trap_time = 30

        if self.img_count > self.delay:
            self.image = self.img_list[self.index]
            self.index += 1
            if self.index > 1: self.index = 0
            self.img_count = 0
        self.img_count += 1

        if self.count >= 0 and self.count < self.rect.height:
            self.rect.y -= 1
        if self.count >= self.rect.height + trap_time and self.count < self.rect.height * 2 + trap_time:
            self.rect.y += 1
        if self.count > self.rect.height * 2 + trap_time + self.cooldown:
            self.count = -1
        self.count += 1

        # check move
        if display.move:
            key = pygame.key.get_pressed()
            if key[pygame.K_LEFT]:
                self.rect.x += int(pixel_width / 2)
            if key[pygame.K_RIGHT]:
                self.rect.x -= int(pixel_width / 2)

# Trap
class Spike_trap(pygame.sprite.Sprite):
    def __init__(self, x, y, move):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/background/50,51-spike_trap.png")
        self.image = pygame.transform.scale(self.image, (int(pixel_width / 2), int(pixel_height / 2)))
        flip = False
        if move == -1: flip = True
        self.image = pygame.transform.flip(self.image, False, flip)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y + int(pixel_height / 2) * move  + move
        self.move = move
        self.count = 0
        self.cooldown = 0

    def update(self):
        warning_time = 40
        trap_time = 10
        dx = self.move * 1

        if self.move == 0:
            pass
        else:
            if self.count == 0:
                self.rect.y -= dx
            if self.count >= warning_time and self.count < warning_time + int(self.rect.height - abs(dx)):
                self.rect.y -= self.move
            if self.count >= warning_time + int(self.rect.height - abs(dx)) + trap_time and self.count < warning_time + int(self.rect.height - abs(dx)) + trap_time + self.rect.height:
                self.rect.y += self.move
            if self.count > warning_time + int(self.rect.height - abs(dx)) + trap_time + self.rect.height + self.cooldown:
                self.count = -1
            self.count += 1
        # check move
        if display.move:
            key = pygame.key.get_pressed()
            if key[pygame.K_LEFT]:
                self.rect.x += int(pixel_width / 2)
            if key[pygame.K_RIGHT]:
                self.rect.x -= int(pixel_width / 2)
        
   
# create enermy
class Enermy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.img_list = []
        for i in range(4):
            img = pygame.image.load(f'images/enermy/turtle_{i}.png')
            if i == 2 or i == 3:
                img = pygame.transform.scale(img, (int(pixel_width / 2), int(pixel_height / 2)))
            else:
                img = pygame.transform.scale(img, (int(pixel_width / 2) // 0.7, int(pixel_height / 2) // 0.7))
            self.img_list.append(img)
        self.image = self.img_list[0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = 1
        self.direction = False
        self.count = 0
        self.index = 0
        # limited movement area
        self.limited_movement_area = int((pixel_width / 2) * 3.5)
        self.left_limit = self.rect.centerx - self.limited_movement_area
        self.right_limit = self.rect.centerx + self.limited_movement_area

        self.vel = 0

    # action
    def update_action(self,action):
        if action == 'run':
            self.count += 1
            if self.count >= 5:
                self.image = self.img_list[self.index]
                self.image = pygame.transform.flip(self.image,self.direction, False)
                self.count = 0
                self.index += 1
                if self.index >= 2: self.index = 0

    def update(self):
        dx = 0
        dy = 0  
        # set gravity
        self.vel += 1
        if self.vel > 10: 
            self.vel = 10
        dx = self.move_direction
        dy = self.vel

        # check for collision with platform
        for tile in world.platform_list:
            # in x direction
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.rect.width, self.rect.height):
                self.move_direction *= -1
                self.direction = not self.direction
                dx = 0
            # in y direction
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.rect.width, self.rect.height):
                dy = tile[1].top - self.rect.bottom

        # limited movement area
        if self.rect.x >= self.right_limit or self.rect.x <= self.left_limit:
            self.move_direction *= -1
            self.rect.x += self.move_direction*2
            self.direction = not self.direction

        self.update_action('run')

        self.rect.x += dx
        self.rect.y += dy

        # check move
        if display.move:
            key = pygame.key.get_pressed()
            if key[pygame.K_LEFT]:
                self.rect.x += int(pixel_width / 2)
                self.left_limit += int(pixel_width / 2)
                self.right_limit += int(pixel_width / 2)
            if key[pygame.K_RIGHT]:
                self.rect.x -= int(pixel_width / 2)
                self.left_limit -= int(pixel_width / 2)
                self.right_limit -= int(pixel_width / 2)


flying_platform_group = pygame.sprite.Group()
carnivorous_plant_group = pygame.sprite.Group()
waterfall_group = pygame.sprite.Group()
still_water_group = pygame.sprite.Group()
lava_waterfall_group = pygame.sprite.Group()
lava_group = pygame.sprite.Group()
spike_trap_group = pygame.sprite.Group()
enermy_group = pygame.sprite.Group()


# create file
def Create():
    with open(path, "w") as file:
        for row in range(tiles_per_width):
            for col in range(tiles_per_length):
                file.write("0,")
            file.write("\n")


# save file
def Save():
    with open(path, "w") as file:
        for row in display.data:
            for col in row:
                if col == '':
                    continue
                file.write(col + ",")
            file.write("\n")

def check():
    global tiles_per_length, tiles_per_width, map_width, map_height
    if os.path.isfile(path) == False:
        Create()
    else:
        row_count = 0
        col_count = 0
        with open(path, "r") as file:
            for f in file:
                r = f.strip()
                r = r.split(",")
                col_count = len(r)
                row_count += 1
        tiles_per_length = col_count - 1
        tiles_per_width = row_count
        map_width = pixel_width * tiles_per_length
        map_height = pixel_height * tiles_per_width


    # else:
    #     with open(path, "r") as file:
    #         row_count = 0
    #         for f in file:
    #             r = f.strip()
    #             r = r.split(",")
    #             if len(r) < tiles_per_length:
    #                 Create()
    #                 break
    #             row_count += 1
    #         if row_count < tiles_per_width:
    #             Create()

# read file
def Read():
    check()
    
    data = []
    with open(path, "r") as file:
        for f in file:
            r = f.strip()
            r = r.split(",")
            data.append(r)
    return data

def FileName(Path):
    list = []
    for file in os.listdir(Path):
        list.append(file)
    return list

class Display():
    def __init__(self):
        self.data = Read()
        self.rect = pygame.Rect(0, 0, pixel_width, pixel_height)
        self.img_list = []
        self.col_count = 0
        self.delta = 0
        self.move = False
        self.blurred_img = tiled.img
        self.blurred_img_rect = self.blurred_img.get_rect()

        self.first_coordinates = (0,0)
        self.left_mouse = False
        self.right_mouse = False
        self.blurred_list = []

        # update from file
        row_count = 0
        for row in self.data:
            self.col_count = 0
            for col in row:
                if col == '':
                    continue
                if col != '0':
                    for img in tiled.img_list:
                        if int(col) == img[2]:
                            rect = img[0].get_rect()
                            delta = int((rect.width / pixel_width) / (rect.height / pixel_height))
                            image = pygame.transform.scale(img[0], (pixel_width * delta, pixel_height))
                            rect = image.get_rect()
                            rect.x = self.col_count * pixel_width
                            rect.y = row_count * pixel_height
                            self.img_list.append((image, rect))
                            break
                self.col_count += 1
            row_count += 1

    def update(self):
        self.blurred_list.clear()
        #add
        mouse = pygame.mouse.get_pos()
        self.rect.x = int((mouse[0] - main_screen_rect.x) / pixel_width) * pixel_width
        self.rect.y = int((mouse[1] - main_screen_rect.y) / pixel_height) * pixel_height

        self.blurred_img = tiled.img
        self.blurred_img_rect = self.blurred_img.get_rect()
        delta = int((self.blurred_img_rect.width / pixel_width) / (self.blurred_img_rect.height / pixel_height))
        self.blurred_img = pygame.transform.scale(self.blurred_img, (pixel_width * delta, pixel_height))
        self.blurred_img_rect.x = self.rect.x
        self.blurred_img_rect.y = self.rect.y
        
        if main_screen_rect.collidepoint(mouse[0], mouse[1]):
            # add tile
            row = int((mouse[1] - main_screen_rect.y) / pixel_height)
            col = int((mouse[0] - main_screen_rect.x + self.delta) / pixel_width)
            if pygame.mouse.get_pressed()[0]:
                if self.left_mouse == False:
                    self.first_coordinates = (row, col)
                    self.left_mouse = True
                range_row = 1
                range_col = 1
                if (row - self.first_coordinates[0]) < 0:
                    range_row = -1
                if (col - self.first_coordinates[1]) < 0:
                    range_col = -1
                for row_count in range(self.first_coordinates[0], row + range_row, range_row):
                    for col_count in range(self.first_coordinates[1], col + range_col, range_col):
                        blurred_img = tiled.img
                        blurred_img_rect = blurred_img.get_rect()
                        delta = int((blurred_img_rect.width / pixel_width) / (blurred_img_rect.height / pixel_height))
                        blurred_img = pygame.transform.scale(blurred_img, (pixel_width * delta, pixel_height))
                        blurred_img.set_alpha(150)
                        blurred_img_rect.x = (col_count - int(self.delta / pixel_width)) * pixel_width
                        blurred_img_rect.y = row_count * pixel_height
                        self.blurred_list.append((blurred_img, blurred_img_rect))

            if pygame.mouse.get_pressed()[0] == False and self.left_mouse:
                self.left_mouse = False
                range_row = 1
                range_col = 1
                if (row - self.first_coordinates[0]) < 0:
                    range_row = -1
                if (col - self.first_coordinates[1]) < 0:
                    range_col = -1
                for row_count in range(self.first_coordinates[0], row + range_row, range_row):
                    for col_count in range(self.first_coordinates[1], col + range_col, range_col):
                        if self.data[row_count][col_count] != str(tiled.order):
                            image = tiled.img
                            rect = image.get_rect()
                            delta = int((rect.width / pixel_width) / (rect.height / pixel_height))
                            image = pygame.transform.scale(image, (pixel_width * delta, pixel_height))
                            rect.x = (col_count - int(self.delta / pixel_width)) * pixel_width
                            rect.y = row_count * pixel_height
                            for img in self.img_list:
                                if (img[1].x, img[1].y) == (rect.x, rect.y):
                                    self.img_list.remove(img)
                            self.data[row_count][col_count] = str(tiled.order)
                            self.img_list.append((image, rect))

            # if pygame.mouse.get_pressed()[0]:
            #     if self.data[row][col] != str(tiled.order):
            #         for img in self.img_list:
            #             if (img[1].x, img[1].y) == (self.rect.x, self.rect.y):
            #                 self.img_list.remove(img)
            #         self.data[row][col] = str(tiled.order)
            #         img = tiled.img
            #         rect = img.get_rect()
            #         delta = int((rect.width / pixel_width) / (rect.height / pixel_height))
            #         img = pygame.transform.scale(tiled.img,(pixel_width * delta, pixel_height))
            #         rect = img.get_rect()
            #         rect.x = self.rect.x
            #         rect.y = self.rect.y
            #         self.img_list.append((img, rect))
                            
            #delete tile
            # if pygame.mouse.get_pressed()[-1]:
            #     if self.data[row][col] != '0':
            #         self.data[row][col] = '0'
            #         for img in self.img_list:
            #             if (img[1].x, img[1].y) == (self.rect.x, self.rect.y):
            #                 self.img_list.remove(img)
                            
            if pygame.mouse.get_pressed()[-1]:
                if self.right_mouse == False:
                    self.first_coordinates = (row, col)
                    self.right_mouse = True
                range_row = 1
                range_col = 1
                if (row - self.first_coordinates[0]) < 0:
                    range_row = -1
                if (col - self.first_coordinates[1]) < 0:
                    range_col = -1
                for row_count in range(self.first_coordinates[0], row + range_row, range_row):
                    for col_count in range(self.first_coordinates[1], col + range_col, range_col):
                        blurred_img = pygame.Surface((pixel_width, pixel_height))
                        blurred_img_rect = blurred_img.get_rect()
                        blurred_img.fill((137,137,137))
                        blurred_img.set_alpha(200)
                        blurred_img_rect.x = (col_count - int(self.delta / pixel_width)) * pixel_width
                        blurred_img_rect.y = row_count * pixel_height
                        self.blurred_list.append((blurred_img, blurred_img_rect))

            if pygame.mouse.get_pressed()[-1] == False and self.right_mouse:
                self.right_mouse = False
                range_row = 1
                range_col = 1
                if (row - self.first_coordinates[0]) < 0:
                    range_row = -1
                if (col - self.first_coordinates[1]) < 0:
                    range_col = -1
                for row_count in range(self.first_coordinates[0], row + range_row, range_row):
                    for col_count in range(self.first_coordinates[1], col + range_col, range_col):
                        if self.data[row_count][col_count] != '0':
                            for img in self.img_list:
                                if (img[1].x, img[1].y) == ((col_count - int(self.delta / pixel_width)) * pixel_width, row_count * pixel_height):
                                    self.img_list.remove(img)
                            self.data[row_count][col_count] = '0'
        
        # move
        key = pygame.key.get_pressed()
        self.move = False
        if self.delta > 0 and self.delta <= map_width - main_screen_rect.width:
            if key[pygame.K_LEFT]:
                self.move = True
                self.delta -= pixel_width
                for tile in self.img_list:
                    tile[1].x += pixel_width
        if self.delta >= 0 and self.delta < map_width - main_screen_rect.width:
            if key[pygame.K_RIGHT]:
                self.move = True
                self.delta += pixel_width
                for tile in self.img_list:
                    tile[1].x -= pixel_width

    def draw(self):
        main_screen.fill((137, 137, 137))

        #draw grid
        for row in range(main_screen.get_height() // pixel_height + 1):
            for col in range(main_screen.get_width() // pixel_width + 1):
                pygame.draw.line(main_screen, (79,79,79), (0, row * pixel_height), (main_screen.get_width(), row * pixel_height))
                pygame.draw.line(main_screen, (79,79,79), (col * pixel_width, 0), (col * pixel_width, main_screen.get_height()))

        for img in self.img_list:
            main_screen.blit(img[0], img[1])
        for img in self.blurred_list:
            main_screen.blit(img[0], img[1])
        self.blurred_img.set_alpha(150)
        main_screen.blit(self.blurred_img,self.blurred_img_rect)
        pygame.draw.rect(main_screen, (255,0,0), self.rect, 1)
        screen.blit(main_screen,main_screen_rect)

class Tiled():
    def __init__(self):
        Path = "images/test"
        path_list = FileName(Path)
        self.width = pixel_width * 3
        self.height = pixel_height * 3
        stretch = (tile_screen.get_width() - self.height * 4) // 4
        self.img_list = []
        self.count = 0
        self.count_tiled = 0
        self.col_count = 0
        self.row_count = 0
        for file in path_list:
            img = pygame.image.load(Path + "/" + file)
            rect = img.get_rect()
            delta = int((rect.width / pixel_width) / (rect.height / pixel_height))
            if delta == 0:
                delta = 1
            img = pygame.transform.scale(img, (self.width * delta, self.height))
            rect = img.get_rect()
            if delta == 2 and self.count % 3 > 1:
                self.row_count += 1
                self.count = 0
            if delta == 3 and self.count % 3 > 0:
                self.row_count += 1
                self.count = 0
            self.col_count = self.count % 3
            rect.x = self.col_count * self.width + stretch * (self.col_count + 1)
            rect.y = self.row_count * self.height + stretch * (self.row_count + 1)
            self.img_list.append((img, rect, self.count_tiled + 1))
            if self.count % 3 == 2 or delta == 2 or delta == 3:
                self.row_count += 1
                self.count = -1
            self.count += 1
            self.count_tiled += 1

        self.length = self.row_count * self.height + stretch * (self.row_count + 1) - (self.height + stretch * 2) * 1
        self.count = 0
        self.img = self.img_list[0][0]
        self.order = 1

        self.borders = self.img_list[0][1]
        self.mark = pygame.Surface(self.img_list[0][1].size)

    def update(self):
        mouse = pygame.mouse.get_pos()
        for tile in self.img_list:
            if tile[1].collidepoint(mouse[0] - tile_screen_rect.x, mouse[1] - tile_screen_rect.y):
                if pygame.mouse.get_pressed()[0]:
                    self.borders = tile[1]
                    self.mark = pygame.Surface(tile[1].size)
                    self.img = tile[0]
                    self.order = tile[2]
    def draw(self):
        pygame.draw.rect(tile_screen, (255,255,255), (0,0, tile_screen_rect.width, tile_screen_rect.height), border_radius= 20)

        for tile in self.img_list:
            tile_screen.blit(tile[0], tile[1])

        pygame.draw.rect(tile_screen, (255,0,0), self.borders, 1)
        self.mark.fill((79, 79, 79))
        self.mark.set_alpha(160)
        tile_screen.blit(self.mark,self.borders)

        # draw tiled screen
        screen.blit(tile_screen,tile_screen_rect)

# Button
class Button():
    def __init__(self, centerx, centery, text):
        self.clicked = False
        self.font = pygame.font.SysFont("Cambria", 30, True)
        self.text = self.font.render(text, True, (255,255,255))
        self.rect = self.text.get_rect()
        self.rect.center = (centerx, centery)
        self.bordered_rect = pygame.Rect(self.rect.x - 10, self.rect.y, self.rect.width + 20, self.rect.height + 4)
        self.color = (0, 180, 200)
        self.original_color = self.color

    def check(self):
        mouse = pygame.mouse.get_pos()
        self.color = list(self.original_color)

        if self.rect.collidepoint(mouse):
            if pygame.mouse.get_pressed()[0]:
                if self.clicked == False:
                    self.clicked = True
                for i in range(3):
                    self.color[i] -= 60
                    if self.color[i] < 0:
                        self.color[i] = 0
            if pygame.mouse.get_pressed()[0] == False:
                self.clicked = False
                for i in range(3):
                    self.color[i] += 60
                    if self.color[i] > 255:
                        self.color[i] = 255

        return self.clicked

    def draw(self):
        self.color = tuple(self.color)
        pygame.draw.rect(screen, self.color, self.bordered_rect, border_radius= 10)
        pygame.draw.rect(screen, (0,0,0), self.bordered_rect, 1, 10)
        screen.blit(self.text, self.rect)

class Game():
    def __init__(self):
        pass
    def draw(self):
        screen.fill((0,200,200))
        tiled.update()
        tiled.draw()
        display.update()
        display.draw()
        save_button.draw()
        play_button.draw()

        secondary_screen.fill((137, 137, 137))
        flying_platform_group.update()
        flying_platform_group.draw(secondary_screen)
        carnivorous_plant_group.update()
        carnivorous_plant_group.draw(secondary_screen)
        waterfall_group.update()
        waterfall_group.draw(secondary_screen)
        still_water_group.update()
        still_water_group.draw(secondary_screen)
        lava_waterfall_group.update()
        lava_waterfall_group.draw(secondary_screen)
        lava_group.update()
        lava_group.draw(secondary_screen)
        spike_trap_group.update()
        spike_trap_group.draw(secondary_screen)
        enermy_group.update()
        enermy_group.draw(secondary_screen)
        world.draw()
        #draw grid
        # for row in range(secondary_screen.get_height() // int(pixel_height / 2) + 1):
        #     for col in range(secondary_screen.get_width() // int(pixel_width / 2) + 1):
        #         pygame.draw.line(secondary_screen, (79,79,79), (0, row * int(pixel_height / 2)), (secondary_screen.get_width(), row * int(pixel_height / 2)))
        #         pygame.draw.line(secondary_screen, (79,79,79), (col * int(pixel_width / 2), 0), (col * int(pixel_width / 2), secondary_screen.get_height()))
        screen.blit(secondary_screen,secondary_screen_rect)

    def reset(self):
        flying_platform_group.empty()
        carnivorous_plant_group.empty()
        waterfall_group.empty()
        still_water_group.empty()
        lava_waterfall_group.empty()
        lava_group.empty()
        spike_trap_group.empty()
        enermy_group.empty()
        world.reset()

tiled = Tiled()
display = Display()
world = World()
game = Game()

save_button = Button(1060, 650, "Save")
play_button = Button(950, 650, "Play")

font = pygame.font.SysFont("Arial", 30, True)

save = False
run = True
while run:
    game.draw()
    key = pygame.key.get_pressed()
    if play_button.check() or key[pygame.K_SPACE]:
        run = False
        start = True
        from mario import *

    if save_button.check() or (key[pygame.K_LCTRL] and key[pygame.K_s]):
        if save == False:
            Save()
            game.reset()
            save = True
    else:
        save = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEWHEEL:
            # check scroll in tile_screen
            mouse = pygame.mouse.get_pos()
            if tile_screen_rect.collidepoint(mouse):
                if tiled.count >= 0 and tiled.count <= tiled.length:
                    for tile in tiled.img_list:
                        tile[1].y += event.y * 50
                    tiled.count -= event.y * 50
                if tiled.count < 0:
                    for tile in tiled.img_list:
                        tile[1].y -= event.y * 50
                    tiled.count = 0
                if tiled.count > tiled.length:
                    for tile in tiled.img_list:
                        tile[1].y -= event.y * 50
                    tiled.count = tiled.length

    clock.tick(60)
    pygame.display.update()