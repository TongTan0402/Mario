import pygame
from pygame.locals import *
import random
import math
# from tiles import path
import os

pygame.init()
pygame.mixer.init()

clock = pygame.time.Clock()

pixel_width = 26
pixel_height = 20

tile_size = 40
screen_width = tile_size * pixel_width
screen_height = tile_size * pixel_height

frontier = 350
fps = 60
health = 6

font = pygame.font.SysFont("Cambria", pixel_height, bold=True)

screen = pygame.display.set_mode((screen_width,screen_height))
transparency = pygame.Surface((screen_width, screen_height))

#draw grid
def draw_grid():
    for i in range(tile_size):
        pygame.draw.line(screen, (255,255,255), (0, i * pixel_height), (screen_width, i * pixel_height))
        pygame.draw.line(screen, (255,255,255), (i * pixel_width, 0), (i * pixel_width, screen_height))

# create world
class World():
    def __init__(self):
        self.level = 1
        self.current_level = 0
        self.curtain = 1
        self.start = False
        self.reset()

    def reset(self):
        if self.current_level != self.level:
            self.start = False
            self.Original_world = True
            self.x_when_returning = 0
            self.current_level = self.level

        self.platform_list = []
        self.detail_list = []
        self.hidden_list =[]
        self.exit_coordinates = ''
        self.start_coordinates = ''
        self.col = 0
        self.path = f"level/level_{self.level}.{self.curtain}.csv"
        # self.path = path

        with open(self.path,"r") as map:
            row_count = 0
            for row in map:
                col_count = 0
                row = row.split(',')
                for tile in row:
                    try:
                        platform_img = pygame.image.load(f"images/background/{tile}-platform.png")
                        platform_img = pygame.transform.scale(platform_img,(pixel_width, pixel_height))
                        platform_img_rect = platform_img.get_rect()
                        platform_img_rect.x = col_count * pixel_width - self.x_when_returning
                        platform_img_rect.y = row_count * pixel_height
                        infor = (platform_img, platform_img_rect)
                        self.platform_list.append(infor)
                    except:
                        pass
                    try:
                        detail_img = pygame.image.load(f"images/background/{tile}-detail.png")
                        detail_img = pygame.transform.scale(detail_img,(pixel_width, pixel_height))
                        detail_img_rect = detail_img.get_rect()
                        detail_img_rect.x = col_count * pixel_width - self.x_when_returning
                        detail_img_rect.y = row_count * pixel_height
                        infor = (detail_img, detail_img_rect)
                        self.detail_list.append(infor)
                    except:
                        pass 
                    try:
                        hidden_img = pygame.image.load(f"images/background/{tile}-hidden.png")
                        hidden_img = pygame.transform.scale(hidden_img,(pixel_width, pixel_height))
                        hidden_img_rect = hidden_img.get_rect()
                        hidden_img_rect.x = col_count * pixel_width - self.x_when_returning
                        hidden_img_rect.y = row_count * pixel_height
                        hidden_img_rect.width = pixel_width
                        hidden_img_rect.height = pixel_height
                        infor = (hidden_img, hidden_img_rect)
                        self.hidden_list.append(infor)
                    except:
                        pass
                    if tile == '29' or tile == '30' or tile == '31' or tile == '32':
                        secret_box = Secret_box(col_count * pixel_width - self.x_when_returning, row_count * pixel_height, int(tile) - 29)
                        secret_box_group.add(secret_box)
                    if tile == '21':
                        brick = Brick(col_count * pixel_width - self.x_when_returning, row_count * pixel_height)
                        brick_group.add(brick)
                    if tile == '58':
                        coin = Coin(col_count * pixel_width - self.x_when_returning, row_count * pixel_height)
                        coin_group.add(coin)
                    if tile == '62' or tile == '63':
                        get_out = GetOut(col_count * pixel_width - self.x_when_returning, row_count * pixel_height, int(tile) - 62)
                        get_out_group.add(get_out)
                    if tile == '61':
                        get_in = GetIn(col_count * pixel_width - self.x_when_returning, row_count * pixel_height)
                        get_in_group.add(get_in)
                    if tile == '16': # up and down
                        flying_platform = Flying_platform(col_count * pixel_width - self.x_when_returning, row_count * pixel_height, 1, 0, 200, False)
                        flying_platform_group.add(flying_platform)
                    if tile == '15': # left and right
                        flying_platform = Flying_platform(col_count * pixel_width - self.x_when_returning, row_count * pixel_height, 0, 1, 200, False)
                        flying_platform_group.add(flying_platform)
                    if tile == '19': # up auto
                        flying_platform = Flying_platform(col_count * pixel_width - self.x_when_returning, row_count * pixel_height, 1, 0, 200, True)
                        flying_platform_group.add(flying_platform)
                    if tile == '17': # left auto
                        flying_platform = Flying_platform(col_count * pixel_width - self.x_when_returning, row_count * pixel_height, 0, -1, 200, True)
                        flying_platform_group.add(flying_platform)
                    if tile == '20': # down auto
                        flying_platform = Flying_platform(col_count * pixel_width - self.x_when_returning, row_count * pixel_height, -1, 0, 200, True)
                        flying_platform_group.add(flying_platform)
                    if tile == '18': #right auto
                        flying_platform = Flying_platform(col_count * pixel_width - self.x_when_returning, row_count * pixel_height, 0, 1, 300, True)
                        flying_platform_group.add(flying_platform)
                    if tile == '59':
                        enermy = Enermy(col_count * pixel_width - self.x_when_returning, row_count * pixel_height)
                        enermy_group.add(enermy)
                    if tile == '41' or tile == '42' or tile == '43':
                        for i in range(-1,2):
                            for j in range(-1, 2):
                                waterfall = Waterfall((col_count + j) * pixel_width - self.x_when_returning, (row_count - i) * pixel_height, tile)
                                waterfall_group.add(waterfall)
                    if tile == '44':
                        for i in range(-1,2):
                            if i == 0 or row[col_count + i] != tile:
                                still_water = Still_water((col_count + i) * pixel_width - self.x_when_returning, row_count * pixel_height)
                                still_water_group.add(still_water)
                    if tile == '50' or tile == '51': # above (50: auto)
                        spike_trap = Spike_trap(col_count * pixel_width - self.x_when_returning, row_count * pixel_height, int(tile) - 50)
                        spike_trap_group.add(spike_trap)
                    if tile == '52' or tile == '53': # below (53: auto)
                        spike_trap = Spike_trap(col_count * pixel_width - self.x_when_returning, row_count * pixel_height, int(tile) - 53)
                        spike_trap_group.add(spike_trap)
                    # exit
                    if tile == '57':
                        self.exit_coordinates = pygame.Rect((col_count + 1) * pixel_width - 2 - self.x_when_returning, row_count * pixel_height, pixel_width, pixel_height * 2)
                    # start
                    if tile == '56':
                        self.start_coordinates = pygame.Rect((col_count - 1) * pixel_width - self.x_when_returning, row_count * pixel_height, pixel_width, pixel_height * 2)
                    # lava waterfall
                    if tile == '45' or tile == '46' or tile == '47':
                        for i in range(-1,2):
                            for j in range(-1, 2):
                                lava = Lava_waterfall((col_count + j) * pixel_width - self.x_when_returning, (row_count - i) * pixel_height, tile)
                                lava_waterfall_group.add(lava)
                    # lava
                    if tile == '48':
                        for i in range(-1,2):
                            if i == 0 or row[col_count + i] != tile:
                                lava = Lava((col_count + i) * pixel_width - self.x_when_returning, row_count * pixel_height)
                                lava_group.add(lava)
                    # Lava
                    if tile == '49':
                        for i in range(-1,2,2):
                            if row[col_count + i] != tile:
                                detail_img = pygame.image.load(f"images/background/{tile}-platform.png")
                                detail_img = pygame.transform.scale(detail_img,(pixel_width, pixel_height))
                                detail_img_rect = detail_img.get_rect()
                                detail_img_rect.x = (col_count + i) * pixel_width - self.x_when_returning
                                detail_img_rect.y = row_count * pixel_height
                                infor = (detail_img, detail_img_rect)
                                self.detail_list.append(infor)
                    # Carnivorous_plant
                    if tile == '60':
                        carnivorous_plant = Carnivorous_plant(col_count * pixel_width - self.x_when_returning, row_count * pixel_height)
                        carnivorous_plant_group.add(carnivorous_plant)
                    col_count += 1

                row_count +=1
                self.col = col_count -1

    # draw world
    def draw_platform(self): 
        # check if map scrolls
        if player.check_map_scroll:
            for tile in self.platform_list:
                tile[1].x -= player.dx
            for tile in self.detail_list:
                tile[1].x -= player.dx
            for tile in self.hidden_list:
                tile[1].x -= player.dx
            try:
                self.exit_coordinates.x -= player.dx
            except:
                pass

        for tile in self.platform_list:
            screen.blit(tile[0], tile[1])

    def draw_detail(self):
        for tile in self.detail_list:
            screen.blit(tile[0], tile[1])

# create player
player_size = (pixel_height + 4, pixel_height + 4)
giant_player_size = (pixel_height + 8, pixel_height + 14)
class Player():
    def __init__(self):
        self.get_in = False
        self.got_in = False
        self.exit = False
        self.got_out = False
        self.died = False
        self.giant = False
        self.shooting_ability = False
        self.index = 0
        self.col_count = 0
        self.img_list = []
        for i in range(10):
            try:
                img = pygame.image.load(f"images/player/mario_{i}.png").convert_alpha()
                img = pygame.transform.scale(img, player_size)
                self.img_list.append(img)
            except:
                pass
        self.img = self.img_list[self.index]
        self.rect = self.img.get_rect()
        self.reset()

    #reset 
    def reset(self):
        self.count = 0
        self.clock = 0
        self.vel = 0
        self.height_of_jumping = -15
        self.weight = 10
        self.speed = 3
        self.flip = False
        self.direction = 1
        self.check_wall = True
        self.jumped = False
        self.get_in = False
        self.shot = False
        self.under_the_water = False
        self.died_music = False
        self.recoil = 10
        self.recoil_count = 0
        self.walk_cooldown = 5
        self.shoot_cooldown = 20
        self.shoot_count = 0
        self.animation = ''
        if world.Original_world:
            self.col_count = 0
        if self.died == True:
            self.giant = False
            self.shooting_ability = False
        if world.start == False:
            try:
                self.rect.x = world.start_coordinates.x
                self.rect.y = world.start_coordinates.y
                world.start = True
            except:
                pass
        self.dx = 0
        self.dy = 0
        self.appear_tile = False
        self.check_map_scroll = False
        self.in_flying_platform = False
        self.dx_flying_platform = 0
    
    def action(self, animation):
        if animation == 'run' and self.jumped == False:
            self.count += 1
            if self.count >= self.walk_cooldown:
                self.count = 0
                if immortal.state == False:
                    self.index += 1
                    if self.index > 2: self.index = 0
                else:
                    if self.index % 2 != 0: self.index = 0
                    self.index += 4
                    if self.index >= 10: self.index = 0
                    elif self.index == 8: self.index = 2

        elif self.animation == 'shoot':
            self.count += 1
            if immortal.state == False:
                self.index = 2
            else:
                if self.count >= self.walk_cooldown:
                    self.count = 0
                    self.index += 2
                    if self.index > 4: 
                        self.index = 2

        # animation == ''
        elif self.jumped == False: 
            self.count += 1
            if immortal.state == False:
                self.index = 0
            else:
                if self.count >= self.walk_cooldown:
                    self.count = 0
                    self.index += 6
                    if self.index > 6: self.index = 0

        # animation == 'jump'
        if self.jumped or self.shot:
            self.count += 1
            if immortal.state == False:
                self.index = 3
            else:
                if self.count >= self.walk_cooldown:
                    self.count = 0
                    self.index += 2
                    if self.index > 5: 
                        self.index = 3

        if animation == "die":
            self.index = 7

        self.img = self.img_list[self.index]

    # check for collision
    def check_collide(self):
        # if the player is shot
        if self.shot == False:
            self.recoil_count = 0
        if self.shot == True:
            self.dx = -self.direction
            if self.recoil_count == 0:
                self.vel = -4
                self.dy = -10
            if self.recoil_count >= self.recoil:
                self.shot = False
            self.recoil_count += 1
            
        # start
        try:
            if world.start_coordinates.colliderect(self):
                self.dx = 1
                world.start = True
            else:
                if world.start:
                    world.start_coordinates.x -= 10
                    world.start = False
        except:
            pass

        # exit
        try:
            if world.exit_coordinates.colliderect(self):
                self.dx = 1
                self.exit = True
            else:
                if self.exit:
                    if game.Win == False:
                        world.level += 1 
                    if world.level <= limited_level:
                        game.reset()
                        self.exit = False
        except:
            pass

        # check if player runs out of the world
        if self.exit == False and world.start == False:
            if self.rect.left < 0: self.rect.left = 0
            elif self.rect.right > screen_width: self.rect.right = screen_width

        if self.died == False:
            # check for collision with platform
            for tile in world.platform_list:
                #check for collision in x direction
                if tile[1].colliderect(self.rect.x + self.dx, self.rect.y, self.rect.width, self.rect.height):
                    self.dx = 0
                #check for collision in y direction
                if tile[1].colliderect(self.rect.x, self.rect.y + self.dy, self.rect.width, self.rect.height):
                    if self.vel < 0:
                        self.dy = tile[1].bottom - self.rect.top
                        self.vel = 0
                    else: 
                        self.dy = tile[1].top - self.rect.bottom
                        self.vel = 0
                        self.jumped = False

            # check for collision with hidden tile
            for tile in world.hidden_list:
                self.appear_tile = False
                for check in appear_group:
                    if check.rect == tile[1]:
                        self.appear_tile = True
                #check for collision in x direction
                if tile[1].colliderect(self.rect.x + self.dx, self.rect.y, self.rect.width, self.rect.height):
                    self.dx = 0
                    if self.appear_tile == False:
                        appear = Appear(tile[1].x, tile[1].y, tile[0])
                        appear_group.add(appear)
                # check for collision in y direction
                if tile[1].colliderect(self.rect.x, self.rect.y + self.dy, self.rect.width, self.rect.height):
                    if self.dy >= 0:
                        self.vel = 0
                        self.dy = tile[1].top - self.rect.bottom
                        self.jumped = False
                    else:
                        self.vel = 0
                        self.dy = tile[1].bottom - self.rect.top
                    if self.appear_tile == False:
                        appear = Appear(tile[1].x, tile[1].y, tile[0])
                        appear_group.add(appear)
        
            # check for collision with brick
            for tile in brick_group:
                if tile.rect.colliderect(self.rect.x + self.dx, self.rect.y, self.rect.width, self.rect.height):
                    self.dx = 0
                if tile.rect.colliderect(self.rect.x, self.rect.y + self.dy, self.rect.width, self.rect.height):
                    if self.vel <= 0:
                        self.vel = 0
                        self.dy = tile.rect.bottom - self.rect.top
                    else:
                        self.vel = 0
                        self.dy = tile.rect.top - self.rect.bottom
                        self.jumped = False
                        
            # check if the player is standing on flying platform
            self.in_flying_platform = False
            for platform in flying_platform_group:
                #check for collision in y direction
                if platform.rect.colliderect(self.rect.x, self.rect.y + self.dy + 2, self.rect.width, self.rect.height):
                    if self.vel > 0 and self.rect.bottom - 1 <= platform.rect.top: 
                        self.dy = platform.rect.top - self.rect.bottom
                        self.vel = 0
                        self.jumped = False
                        if platform.switch_1 == False and platform.switch_2 == False:
                            platform.switch_0 = not platform.switch_0
                            platform.switch_1 = True
                        platform.switch_2 = True

                        if platform.left_right:
                            self.rect.x += platform.dx
                    self.in_flying_platform = True
                    self.dx_flying_platform = platform.dx
                
                else:
                    if platform.switch_2 == False:
                        platform.switch_1 = False
                
                    
            # get in
            if self.get_in:
                if pygame.sprite.spritecollide(self, get_in_group, False):
                    self.dy = 1
                    self.got_in = True
                else:
                    self.get_in = False
                    if self.got_in:
                        if world.Original_world == False:
                            world.curtain -= 1
                        elif world.Original_world == True:
                            world.curtain += 1
                            self.col_count = 0
                        game.reset()
                        self.got_out = True
            # get out
            for tile in get_out_group:
                if self.got_out:
                    if world.Original_world == False and self.got_in:
                        self.col_count = tile.rect.x - frontier - self.rect.width
                        if self.col_count < 0: self.col_count = 0
                        world.x_when_returning = self.col_count
                        game.reset()
                        # get_in_group.empty()
                        if self.col_count != 0: tile.rect.x = frontier + self.rect.width
                    if self.got_in:
                        self.rect.center = tile.rect.center
                        self.got_in = False
                        world.Original_world = False
                    if tile.rect.colliderect(self):
                        if tile.tile == 0:
                            self.dy = -1
                        elif tile.tile == 1:
                            self.dy = 1
                    else:
                        self.got_out = False
                        # tile.kill() 
                 
    # update handle
    def update(self):
        self.dx = 0
        self.dy = 0

        # change height of jumping, weight, speed
        if self.giant == True:
            self.height_of_jumping = -18
            self.weight = 25
            self.speed = 4
            self.walk_cooldown = 4
        else:
            self.height_of_jumping = -15
            self.weight = 10
            self.speed = 3
            self.walk_cooldown = 5

        # check if player is underwater
        if pygame.sprite.spritecollide(player, still_water_group, False):
            self.under_the_water = True
        if self.under_the_water:
            self.speed -= 2
            if self.giant:
                self.height_of_jumping = -14
            else:
                self.height_of_jumping = -11
            self.walk_cooldown = 7

        # check giant state
        if self.giant == True:
            self.img_list.clear()
            for i in range(10):
                try:
                    img = pygame.image.load(f"images/player/mario_{i}.png").convert_alpha()
                    img = pygame.transform.scale(img, giant_player_size)
                    self.img_list.append(img)
                except:
                    pass
            (self.rect.width, self.rect.height) = giant_player_size
        else:
            self.img_list.clear()
            for i in range(10):
                try:
                    img = pygame.image.load(f"images/player/mario_{i}.png").convert_alpha()
                    img = pygame.transform.scale(img, player_size)
                    self.img_list.append(img)
                except:
                    pass
            (self.rect.width, self.rect.height) = player_size

        # get keypresses
        key = pygame.key.get_pressed()
        if key[pygame.K_UP] and self.jumped == False: 
            self.vel = self.height_of_jumping
            self.jumped = True
            self.animation = 'jump'
            jump_music.play()
        elif key[pygame.K_LEFT]: 
            self.dx = -self.speed
            self.flip = True
            self.direction = -1
            self.animation = 'run'
        elif key[pygame.K_RIGHT]: 
            self.dx = self.speed
            self.flip = False
            self.direction = 1
            self.animation = 'run'
        elif key[pygame.K_DOWN]: 
            self.get_in = True
            self.animation = ''
        else: self.animation = ''

        if key[pygame.K_SPACE] and self.shooting_ability:
            self.animation = 'shoot'
            if self.shoot_count >= self.shoot_cooldown:
                plaer_bullet = Player_bullet(self.rect.centerx + self.direction *10, self.rect.centery, self.direction)
                player_bullet_group.add(plaer_bullet)
                self.shoot_count = -1
            self.shoot_count += 1
        elif key[pygame.K_SPACE] == False:
            self.shoot_count = self.shoot_cooldown

        # set gravity 
        self.vel += 1
        if self.vel > self.weight: self.vel = self.weight
        self.dy = self.vel

        self.check_collide()
        
        if self.dy >= 2: self.jumped = True
        if game.gameover: 
            if self.died == False:
                self.vel = -10
            if self.rect.y > screen_height and self.died == False:
                self.vel = -15
            if self.rect.y > screen_height + 30:
                self.dy = 0
            self.dx = 0
            self.died = True
            self.animation = 'die'
            if self.died_music == False:
                self.died_music = True
                died_music.play()
                music.stop()
        else:
            self.died = False

        # animation
        self.action(self.animation)

        # if player under the water
        if self.jumped == False:
            self.under_the_water = False

        # update player coordinates
        self.rect.x += self.dx
        self.rect.y += self.dy

        # scroll map
        # pygame.draw.line(screen,(255,255,255), (frontier,0), (frontier, screen_height))
        # pygame.draw.line(screen,(255,255,255), (screen_width - frontier,0), (screen_width - frontier, screen_height))
        if (self.rect.right > screen_width - frontier and self.col_count < world.col * pixel_width - screen_width) or (self.rect.left < frontier and self.col_count > abs(self.dx)):
        # if self.rect.right > screen_width - frontier and self.col_count < world.col * pixel_width - screen_width:
            if self.in_flying_platform:
                self.dx += self.dx_flying_platform
            self.rect.x -= self.dx
            self.col_count += self.dx
            self.check_map_scroll = True
        else: self.check_map_scroll = False

    #draw player
    def draw(self):
        # pygame.draw.rect(screen,(255,255,255), self.rect, 1)
        screen.blit(pygame.transform.flip(self.img, self.flip, False), self.rect)

class Player_head():
    def __init__(self):
        self.rect = pygame.Rect(player.rect.centerx - player.rect.width // 4, player.rect.top - 1, player.rect.width // 2, 1)

    def update(self):
        self.rect = pygame.Rect(player.rect.centerx - player.rect.width // 4, player.rect.top - 1, player.rect.width // 2, 1)


immortal_time = 30 # Time invulnerability when taking damage
# immortality, not being able to die
class Immortal():
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.immortal_time = immortal_time
        self.count = self.immortal_time
        self.shot = False
        self.hit_by_shell = False
        self.state = False

    def check(self): 
        if player.died == False:
            if immortal.state == False:
                self.immortal_time = immortal_time
            if self.shot == False and self.hit_by_shell == False: 
                self.count = -1
                self.state = False
            if self.count == 0 and (self.shot or self.hit_by_shell): 
                if self.state == False and player.giant == False: 
                    player.shooting_ability = False
                    health_group.remove(health_group.sprites()[-1])
                if self.state == False and player.giant:
                    player.shooting_ability = False
                    player.giant = False
                self.state = True
            if self.count >= self.immortal_time:
                self.state = False
                self.shot = False
                self.hit_by_shell = False
                self.count = -1
            self.count += 1

# player's bullet
class Player_bullet(pygame.sprite.Sprite):
    
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/bullet.png")
        self.image = pygame.transform.scale(self.image, (pixel_width // 2, pixel_height // 2))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction
        self.bounces = 0
        self.vel = -9
    
    def update(self):
        # bullet speed
        dx = self.direction*6

        number_of_bounces = 5

        self.vel += 1
        if self.vel > 15:
            self.vel = 15

        # check if map scrolls
        if player.check_map_scroll: dx -= player.dx

        self.rect.x += dx
        self.rect.y += self.vel

        #check for colliision with turtle
        if pygame.sprite.spritecollide(self, enermy_group, False):
            self.bounces += 1
            self.vel = -9 + self.bounces * 2
            sword_music.play()

        #check for collision with flower
        if pygame.sprite.spritecollide(self,carnivorous_plant_group, True):
            shot_music.play()

        #check for collision between world and bullet
        if self.rect.right <= 0 or self.rect.left >= screen_width:
            self.kill()

        # platform
        for tile in world.platform_list:
            # check for collision with platform in y direction
            if tile[1].colliderect(self.rect.x, self.rect.y + self.vel, self.rect.width, self.rect.height):
                self.bounces += 1
                if self.vel >= 0:
                    self.vel = -9 + self.bounces * 2
                else:
                    self.vel = 0
            # check for collision with platform in x direction
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.rect.width, self.rect.height):
                self.bounces += 1
                self.direction *= -1

        # hidden list
        for tile in world.hidden_list:
            appear_tile = False
            # check for collision with hidden in y direction
            if tile[1].colliderect(self.rect.x, self.rect.y + self.vel, self.rect.width, self.rect.height):
                self.bounces += 1
                if self.vel >= 0:
                    self.vel = -13 + self.bounces * 2
                else:
                    self.vel = 0
                # appear hidden
                for check in appear_group:
                    if check.rect == tile[1]:
                        appear_tile = True
                if appear_tile == False:
                        appear = Appear(tile[1].x, tile[1].y, tile[0])
                        appear_group.add(appear)
            # check for collision with hidden in x direction
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.rect.width, self.rect.height):
                self.bounces += 1
                self.direction *= -1
                # appear hidden
                for check in appear_group:
                    if check.rect == tile[1]:
                        appear_tile = True
                if appear_tile == False:
                        appear = Appear(tile[1].x, tile[1].y, tile[0])
                        appear_group.add(appear)

        if self.bounces >= number_of_bounces:
            self.kill()
        
# enermy's bullet
class Enermy_bullet(pygame.sprite.Sprite):
    
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/bullet.png")
        self.image = pygame.transform.scale(self.image, (pixel_width // 2, pixel_height // 2))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction
    
    def update(self):
        # bullet speed
        dx = self.direction*8

        # check if map scrolls
        if player.check_map_scroll: 
            dx -= player.dx
        self.rect.x += dx

        #check for collision between world and bullet
        if self.rect.right <= 0 or self.rect.left >= screen_width:
            self.kill()
        for tile in world.platform_list:
            if tile[1].colliderect(self.rect.x - dx*3, self.rect.y, self.rect.width, self.rect.height):
                self.kill()
                
        # check collision between player and bullet
        if pygame.sprite.spritecollide(player, enermy_bullet_group,True) and immortal.shot == False and game.gameover == False:
            immortal.shot = True
            player.shot = True
            shot_music.play()
        
# create enermy
class Enermy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.img_list = []
        for i in range(4):
            img = pygame.image.load(f'images/enermy/turtle_{i}.png')
            if i == 2 or i == 3:
                img = pygame.transform.scale(img, (pixel_width, pixel_height))
            else:
                img = pygame.transform.scale(img, (pixel_width // 0.7, pixel_height // 0.7))
            self.img_list.append(img)
        self.image = self.img_list[0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = 1
        self.direction = False
        self.count = 0
        self.index = 0
        self.detected = False
        self.shell = False
        self.stomp = False
        # limited movement area
        self.limited_movement_area = pixel_width * 7
        self.left_limit = self.rect.centerx - self.limited_movement_area
        self.right_limit = self.rect.centerx + self.limited_movement_area

        self.vel = 0
        self.freezing_time = 30
        self.shell_cooldown = 100
        self.sliding_shell_speed = 6
        self.collision_check = False
        self.shoot_cooldown = 40
        self.shoot = self.shoot_cooldown

        self.vision_range = 7
        self.vision_max = pixel_width * self.vision_range * 2
        self.vision_min = self.vision_max
        self.vision = pygame.Rect(0, 0, pixel_width * self.vision_range * 2, 2)

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
        elif action == 'stop':
            self.index = 1
            self.image = self.img_list[self.index]
            self.image = pygame.transform.flip(self.image, self.direction, False)
            if self.shoot >= self.shoot_cooldown:
                self.shoot = 0
                enermy_bullet = Enermy_bullet(self.rect.centerx + self.move_direction * pixel_width //2, self.rect.centery, self.move_direction)
                enermy_bullet_group.add(enermy_bullet)
            self.shoot += 1
        elif action == 'shell':
            self.index = 3
            self.image = self.img_list[self.index]
            self.image = pygame.transform.flip(self.image, self.direction, False)
        rect = self.image.get_rect()
        rect.center = self.rect.center
        self.rect = rect


        # set vision
        self.vision.center = (self.rect.centerx + int(self.vision_min  * self.move_direction / 2), self.rect.centery)
        
        #draw vision rect
        # pygame.draw.rect(screen, (255,0,0), self.vision, 1)

    def update(self):
        dx = 0
        dy = 0  
        # set gravity
        self.vel += 1
        if self.vel > 10: 
            self.vel = 10
        if self.stomp:
            dx = self.move_direction * self.sliding_shell_speed
        else:
            dx = self.move_direction
        dy = self.vel

        # check for collision with platform
        for tile in world.platform_list:
            # in x direction
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.rect.width, self.rect.height):
                self.move_direction *= -1
                self.direction = not self.direction
                dx = 0
                self.collision_check = True
            # in y direction
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.rect.width, self.rect.height):
                dy = tile[1].top - self.rect.bottom

        # check for collision between bullet's player and enermy
        if pygame.sprite.spritecollide(self, player_bullet_group,False):
            self.shell = True

        # check collision between player and enermy
        if player.dy > 0 and self.shell == False:
            if self.rect.collidepoint(player.rect.right, player.rect.bottom + player.dy + player.recoil) \
                or self.rect.collidepoint(player.rect.left, player.rect.bottom + player.dy + player.recoil) \
                or self.rect.collidepoint(player.rect.centerx, player.rect.bottom + player.dy + player.recoil):
                player.vel = -15
                self.vel = -4
                self.shell = True
                self.stomp = False
                self.count = 0

        # if turtle goes into its shell
        if self.shell == True:
            if self.count >= self.shell_cooldown:
                self.shell = False
                self.count = -1
                self.stomp = False
            dx = 0
            self.count += 1
            self.update_action('shell')

            #stomp on the shell
            if self.stomp == False:
                # check for collision with player in y direction
                if self.rect.collidepoint(player.rect.right, player.rect.bottom + player.dy + player.recoil) \
                or self.rect.collidepoint(player.rect.left, player.rect.bottom + player.dy + player.recoil) \
                or self.rect.collidepoint(player.rect.centerx, player.rect.bottom + player.dy + player.recoil):
                    player.vel = -15
                    self.stomp = True
                    self.count = -1
                #check for collision with player in x direction
                elif self.rect.colliderect(player.rect.x + player.dx, player.rect.y, player.rect.width, player.rect.height):
                    if player.dx > 0:
                        self.move_direction = 1
                        self.direction = False
                    else:
                        self.move_direction = -1
                        self.direction = True
                    self.stomp = True
                    self.count = -1
            if self.stomp:
                # if stomp
                dx += self.move_direction * self.sliding_shell_speed
                self.left_limit += dx
                self.right_limit += dx

                # check for collision between turtle's shell and player
                if pygame.sprite.spritecollide(player, enermy_group, False) and immortal.hit_by_shell == False:
                    immortal.hit_by_shell = True
              
        if self.shell == False:
            # limited movement area
            if self.rect.x >= self.right_limit or self.rect.x <= self.left_limit:
                self.move_direction *= -1
                self.rect.x += self.move_direction*2
                self.direction = not self.direction

            # the vision is blocked by the wall
            self.vision_min = self.vision_max
            for tile in world.platform_list:
                if tile[1].colliderect(self.vision):
                    if abs(tile[1].x - self.rect.x) < self.vision_min:
                        self.vision_min = abs(tile[1].centerx - self.rect.centerx - 5 * self.move_direction)
            self.vision.width = self.vision_min
            
            # vision checks the player
            if self.vision.colliderect(player.rect): 
                dx = 0
                self.detected = True
                if self.collision_check:
                    self.shoot = self.shoot_cooldown // 1.5
                    self.collision_check = False
                self.update_action('stop')
                self.count = 0
            else:
                self.shoot = self.shoot_cooldown
            
                if self.detected:
                    if self.count >= self.freezing_time:
                        self.detected = False
                        self.count = -1
                    self.count += 1
                    dx = 0
                else: 
                    # random move
                    if random.randint(0,400) == 1:
                        self.move_direction *= -1
                        self.direction = not self.direction
                    self.update_action('run')
  
        # move
            #check map scroll
        if player.check_map_scroll == True: 
            self.left_limit -= player.dx
            self.right_limit -= player.dx
            dx -= player.dx
        self.rect.x += dx
        self.rect.y += dy

# create health
class Health(pygame.sprite.Sprite):
    def __init__(self, x, y, tile):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(f"images/background/heart_{tile}.png")
        self.image = pygame.transform.scale(self.image,(pixel_height//1.3, pixel_height // 0.8))
        self.rect = self.image.get_rect()
        self.rect.x = x - pixel_height * int(tile) //1.66
        self.rect.y = y

# Secret box
class Secret_box(pygame.sprite.Sprite):
    def __init__(self, x, y, tile):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/background/secret.png")
        self.image = pygame.transform.scale(self.image, (pixel_width, pixel_height + 1))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.tile = tile

    def update(self):
        if pygame.sprite.collide_rect(self, player_head):
            item = Item(self.rect.x, self.rect.y, int(self.tile))
            item_group.add(item)
            self.kill()

        if player.check_map_scroll:
            self.rect.x -= player.dx

#Appear tile
class Appear(pygame.sprite.Sprite):
    def __init__(self, x, y, img):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        if player.check_map_scroll:
            self.rect.x -= player.dx

immortal_img = pygame.image.load("images/items/immortal.png")
giant_img = pygame.image.load("images/items/giant.png")
shooting_ability_img = pygame.image.load("images/items/shooting_ability.png")

item_box = (immortal_img, giant_img, shooting_ability_img)

class Item(pygame.sprite.Sprite):
    def __init__(self, x, y, tile):
        pygame.sprite.Sprite.__init__(self)
        self.type = tile
        if self.type == 3:
            self.type = random.randint(0, 2)
        self.image = item_box[self.type]
        self.image = pygame.transform.scale(self.image, (pixel_width, pixel_height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.tile = tile
        self.direction = 1
        self.Iy = 0
        self.freeze_item = 10
        self.item_came_out = False
        self.count = 0
        self.immortal_item = False

    def update(self):
        dx = 0
        dy = 5
        if self.item_came_out:
            if self.count >= self.freeze_item:
                dx = self.direction 
            else:
                self.count += 1

        for tile in world.platform_list:
            # check for collision in y direction
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.rect.width, self.rect.height):
                if self.Iy <= pixel_height / 2:
                    dy = -1
                    self.Iy += -dy
                else:
                    dy = tile[1].top - self.rect.bottom
            
            # check for collision in x direction
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.rect.width, self.rect.height):
                if self.Iy <= pixel_height / 2:
                    self.count = 0
                    self.item_came_out = False
                else:
                    self.item_came_out = True
                    dx = 0
                    self.direction *= -1

        for tile in world.hidden_list:
            # check for collision in y direction
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.rect.width, self.rect.height):
                if self.Iy <= pixel_height / 2:
                    dy = -1
                    self.Iy += -dy
                else:
                    dy = tile[1].top - self.rect.bottom
            
            # check for collision in x direction
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.rect.width, self.rect.height):
                if self.Iy <= pixel_height / 2:
                    self.count = 0
                    self.item_came_out = False
                else:
                    self.item_came_out = True
                    dx = 0
                    self.direction *= -1

        for tile in brick_group:
            # check for collision in y direction
            if tile.rect.colliderect(self.rect.x, self.rect.y + dy, self.rect.width, self.rect.height):
                if self.Iy <= pixel_height / 2:
                    dy = -1
                    self.Iy += -dy
                else:
                    dy = tile.rect.top - self.rect.bottom
            
            # check for collision in x direction
            if tile.rect.colliderect(self.rect.x + dx, self.rect.y, self.rect.width, self.rect.height):
                if self.Iy <= pixel_height / 2:
                    self.count = 0
                    self.item_came_out = False
                else:
                    self.item_came_out = True
                    dx = 0
                    self.direction *= -1

        self.rect.x += dx           
        self.rect.y += dy

        # check for items thrown off the screen
        if self.rect.y > screen_height:
            self.kill()

        # check if the player has picked up the item
        if pygame.sprite.collide_rect(self, player):
            # check what kind of box it was
            if self.type == 0:
                immortal.state = True
                immortal.shot = True
                self.immortal_item = True
            if self.type == 1:
                player.giant = True
            if self.type == 2:
                player.shooting_ability = True
            self.kill()

        if self.immortal_item and immortal.state:
            immortal.immortal_time = 400

        if player.check_map_scroll:
            self.rect.x -= player.dx

class Brick(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/background/21-brick.png")
        self.image = pygame.transform.scale(self.image, (pixel_width, pixel_height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        # check for collision with player
        if pygame.sprite.collide_rect(self, player_head) and player.giant:
            player.vel = 0
            for _ in range(4):
                break_brick = Break_brick(self.rect.centerx, self.rect.centery)
                break_brick_group.add(break_brick)
            self.kill()

        # check if map scrolls
        if player.check_map_scroll:
            self.rect.x -= player.dx

# break brick
class Break_brick(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/background/21-brick.png")
        self.image = pygame.transform.scale(self.image, (pixel_width // 4, pixel_width // 4))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.dx = 0
        self.dy = -3
        self.direction = 1
        self.count = 0

    def update(self):
        self.dy += 1
        for brick in break_brick_group:
            if self.count % 2 == 0:
                self.dx = 0
            else:
                self.direction *= -1
                self.dx = 1

            if self.dy > 10: 
                self.dy = 10
            brick.rect.x += self.dx * self.direction
            brick.rect.y += self.dy
            self.count += 1
        if self.count >= 9 * len(break_brick_group):
            self.kill()

        # check if map scrolls
        if player.check_map_scroll:
            self.rect.x -= player.dx

# Trap
class Spike_trap(pygame.sprite.Sprite):
    def __init__(self, x, y, move):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/background/50,51-spike_trap.png")
        self.image = pygame.transform.scale(self.image, (pixel_width, pixel_height))
        flip = False
        if move == -1: flip = True
        self.image = pygame.transform.flip(self.image, False, flip)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y + pixel_height * move  + move
        self.move = move
        self.count = 0
        self.cooldown = 0

    def update(self):
        warning_time = 100
        trap_time = 10
        dx = self.move * 5

        if self.move == 0:
            if immortal.state == False:
                # check for collision with spike trap
                if pygame.sprite.collide_rect(self, player):
                    player.shot = True
                    immortal.shot = True
        else:
            # check move
            if self.count == 0:
                self.rect.y -= dx
                self.cooldown = random.randint(30,200)
            if self.count >= warning_time and self.count < warning_time + int(self.rect.height - abs(dx)) / 5:
                self.rect.y -= self.move * 5
                if immortal.state == False:
                    # check for collision with spike trap
                    if pygame.sprite.collide_rect(self, player):
                        player.shot = True
                        immortal.shot = True
            if self.count >= warning_time + int(self.rect.height - abs(dx)) / 5 + trap_time and self.count < warning_time + int(self.rect.height - abs(dx)) / 5 + trap_time + self.rect.height:
                self.rect.y += self.move
                if immortal.state == False:
                    # check for collision with spike trap
                    if pygame.sprite.collide_rect(self, player):
                        player.shot = True
                        immortal.shot = True
            if self.count > warning_time + int(self.rect.height - abs(dx)) / 5 + trap_time + self.rect.height + self.cooldown:
                self.count = -1
            self.count += 1
        
        # check if map scrolls
        if player.check_map_scroll:
            self.rect.x -= player.dx

# Carnivorous plants
class Carnivorous_plant(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.index = 0
        self.img_list = []
        random_img = random.randint(1,2)
        if random_img == 1:
            for i in range(2):
                image = pygame.image.load(f"images/enermy/flower_{i}.png")
                image = pygame.transform.scale(image, (pixel_width + 4, pixel_height + 4))
                self.img_list.append(image)
        else:
            for i in range(2,4):
                image = pygame.image.load(f"images/enermy/flower_{i}.png")
                image = pygame.transform.scale(image, (pixel_width + 4, pixel_height + 4))
                self.img_list.append(image)
        self.image = self.img_list[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = x + pixel_width // 2 - 2
        self.rect.y = y + pixel_height + 1
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

        # check move
        if self.count == 0:
            self.cooldown = random.randint(30,150)
        if self.count >= 0 and self.count < self.rect.height:
            self.rect.y -= 1
            if immortal.state == False:
                # check for collision with spike trap
                if pygame.sprite.collide_rect(self, player):
                    player.shot = True
                    immortal.shot = True
        if self.count >= self.rect.height + trap_time and self.count < self.rect.height * 2 + trap_time:
            self.rect.y += 1
            if immortal.state == False:
                # check for collision with spike trap
                if pygame.sprite.collide_rect(self, player):
                    player.shot = True
                    immortal.shot = True
        if self.count > self.rect.height * 2 + trap_time + self.cooldown:
            self.count = -1
        self.count += 1
        
        # check if map scrolls
        if player.check_map_scroll:
            self.rect.x -= player.dx

# water
class Waterfall(pygame.sprite.Sprite):
    def __init__(self, x, y, tile):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(f"images/background/{tile}-waterfall.png")
        self.image = pygame.transform.scale(self.image, (pixel_width, pixel_height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.count = 0

    def update(self):
        if self.count >= pixel_height:
            self.rect.y -= self.count
            self.count = 0

        self.rect.y += 1
        self.count += 1

        # check if map scrolls
        if player.check_map_scroll:
            self.rect.x -= player.dx

# water 
class Still_water(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.img_list = []
        self.index = 0
        for i in range(5):
            image = pygame.image.load(f"images/background/stillwater_{i}.png")
            image = pygame.transform.scale(image, (pixel_width, pixel_height -2))
            image.set_alpha(150)
            self.img_list.append(image)
        self.image = self.img_list[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y + 4
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

        # check if map scrolls
        if player.check_map_scroll:
            self.rect.x -= player.dx

# lava
class Lava_waterfall(pygame.sprite.Sprite):
    def __init__(self, x, y, tile):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(f"images/background/{tile}-lava_waterfall.png")
        self.image = pygame.transform.scale(self.image, (pixel_width, pixel_height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.count = 0

    def update(self):
        if self.count >= pixel_height:
            self.rect.y -= self.count
            self.count = 0

        self.rect.y += 1
        self.count += 1

        # check if map scrolls
        if player.check_map_scroll:
            self.rect.x -= player.dx

# lava 
class Lava(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.img_list = []
        self.index = 0
        for i in range(4):
            image = pygame.image.load(f"images/background/lava_{i}.png")
            image = pygame.transform.scale(image, (pixel_width, pixel_height))
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

        # if player falls into lava
        if pygame.sprite.spritecollide(player, lava_group, False):
            health_group.empty()

        # check if map scrolls
        if player.check_map_scroll:
            self.rect.x -= player.dx

# flying platform 
class Flying_platform(pygame.sprite.Sprite):
    def __init__(self, x, y, up_down, left_right, limited_distance, auto):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/background/15,16,17,18,19,20-flying_platform.png")
        self.image = pygame.transform.scale(self.image, (pixel_width * 3, pixel_height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.x = self.rect.x
        self.y = self.rect.y
        self.direction = 1
        self.up_down = up_down # up:1 , down:-1
        self.left_right = left_right # right:1 , left:-1 
        self.limited_distance = limited_distance
        self.count = 0
        self.auto = auto # True or False
        self.switch_0 = False
        self.switch_1 = False
        self.switch_2 = False

        self.dx = 0
        self.dy = 0

    def update(self):
        self.dx = 0
        self.dy = 0

        if self.auto == False:
            if self.count > self.limited_distance:
                self.count = -1
                self.direction *= -1
            self.count += 1
            self.dx = self.direction * self.left_right
            self.dy = -self.direction * self.up_down
        else:
            if (((abs(self.rect.x - self.x) > 0 and abs(self.rect.x - self.x) <= self.limited_distance and self.left_right != 0) or (abs(self.rect.y - self.y) > 0 and abs(self.rect.y - self.y) <= self.limited_distance and self.up_down != 0)) and self.switch_0 == False and self.switch_2):
                self.direction = -1
                self.dx = self.direction * self.left_right
                self.dy = -self.direction * self.up_down
            if (((abs(self.rect.x - self.x) >= 0 and abs(self.rect.x - self.x) < self.limited_distance and self.left_right != 0) or (abs(self.rect.y - self.y) >= 0 and abs(self.rect.y - self.y) < self.limited_distance and self.up_down != 0)) and self.switch_0 == True and self.switch_2):
                self.direction = 1
                self.dx = self.direction * self.left_right
                self.dy = -self.direction * self.up_down

            if (self.rect.x == self.x and self.rect.y == self.y) or (self.rect.x == self.x + self.limited_distance * self.left_right and self.rect.y == self.y - self.limited_distance * self.up_down):
                self.switch_2 = False

        self.rect.x += self.dx
        self.rect.y += self.dy

        # check if map scrolls
        if player.check_map_scroll:
            self.rect.x -= player.dx
            self.x -= player.dx

# get into the pipe
class GetIn(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(x + pixel_width - 1, y - pixel_height, 2, pixel_height * 2)
        self.count = 0

    def update(self):
        # pygame.draw.rect(screen, (255,0,0), self.rect, 1)
        if player.check_map_scroll:
            self.rect.x -= player.dx

# get into the pipe
class GetOut(pygame.sprite.Sprite):
    def __init__(self, x, y, tile):
        pygame.sprite.Sprite.__init__(self)
        if tile == 0: #up
            direction = 1
        else: # down
            direction = -2
        self.rect = pygame.Rect(x - 1, y + direction * (pixel_height - 2), 2, pixel_height * 2)
        self.tile = tile

    def update(self):
        # pygame.draw.rect(screen, (255,0,0), self.rect, 1)
        if player.check_map_scroll:
            self.rect.x -= player.dx

#start game
class Start(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(x, y, pixel_width, pixel_height * 2)

    def update(self):
        if player.check_map_scroll:
            self.rect.x -= player.dx

# coin 
class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.img_list = []
        self.index = 0
        for i in range(3):
            image = pygame.image.load(f"images/coin/coin_{i}.png")
            image = pygame.transform.scale(image, (pixel_height, pixel_height))
            self.img_list.append(image)
        self.image = self.img_list[self.index]
        self.rect = self.image.get_rect()
        self.rect.centerx = x + pixel_width // 2
        self.rect.centery = y + pixel_height // 2
        self.count = 0
        self.delay = 10

    def update(self):
        if self.count > self.delay:
            self.count = -1
            self.index += 1
            if self.index > 2:
                self.index = 0
            self.image = self.img_list[self.index]
        self.count += 1
        if pygame.sprite.collide_rect(self, player):
            game.score += 1
            self.kill()
            collect_music.play()
        if player.check_map_scroll:
            self.rect.x -= player.dx

# button
class Button():
    def __init__(self, path, width, height):
        self.img = pygame.image.load(path)
        self.img = pygame.transform.scale(self.img,(width, height))
        self.rect = self.img.get_rect()
        self.clicked = False

    def draw(self, x, y):
        self.rect.center = (x, y)
        screen.blit(self.img, self.rect)

    def check_click(self):
        mouse = pygame.mouse.get_pos()
        pressed = pygame.mouse.get_pressed()[0]
        if pressed == False: 
            self.clicked = False

        if self.rect.collidepoint(mouse):
            if pressed == True and self.clicked == False:
                self.clicked = True
        return self.clicked

# background 
class Background():
    def __init__(self):
        self.reset()
    
    # reset
    def reset(self):
        self.img = pygame.image.load("images/bgr_1.jpg")
        self.img = pygame.transform.scale(self.img, (screen_width * 2, screen_height + 60))
        self.rect = self.img.get_rect()
    
    # check if map scrolls
    def update(self):
        if player.check_map_scroll:
            self.rect.x -= int(player.dx / 2)

        screen.blit(self.img,self.rect)

def set_health():
    for i in range(1,7):
        if i % 2 == 1:
            stt = 0
        else:
            stt = 1
        health = Health(i * pixel_width, pixel_height, stt)
        health_group.add(health)

# screen
class Game():
    def __init__(self):
        # player's initial position
        self.original_x_coordinate = pixel_width *0
        self.gameover = False
        self.Win = False
        self.transparency_time = 128
        self.score = 0

    def draw_score(self):
        score_img = font.render(f"x {str(self.score)}", True, (255,255,255))
        score_rect = score_img.get_rect()
        score_rect.x = pixel_width * 2
        score_rect.y = pixel_height * 3 - 4

        coin_img = pygame.image.load("images/coin/coin_1.png")
        coin_img = pygame.transform.scale(coin_img, (pixel_height, pixel_height))
        coin_rect = coin_img.get_rect()
        coin_rect.x = pixel_width
        coin_rect.y = pixel_height * 3

        screen.blit(coin_img, coin_rect)
        screen.blit(score_img, score_rect)

    #draw and update screen  
    def draw_screen(self):
        # background.update()
        world.draw_detail()

        waterfall_group.draw(screen)
        waterfall_group.update()

        lava_waterfall_group.draw(screen)
        lava_waterfall_group.update()

        enermy_bullet_group.draw(screen)
        enermy_bullet_group.update()
        
        player_bullet_group.draw(screen)
        player_bullet_group.update()

        item_group.draw(screen)
        item_group.update()

        coin_group.draw(screen)
        coin_group.update()

        player.update()
        player.draw()
        enermy_group.draw(screen)
        enermy_group.update()

        player_head.update()
        immortal.check()

        still_water_group.draw(screen)
        still_water_group.update()

        lava_group.draw(screen)
        lava_group.update()

        spike_trap_group.draw(screen)
        spike_trap_group.update()
        carnivorous_plant_group.draw(screen)
        carnivorous_plant_group.update()

        world.draw_platform()

        flying_platform_group.draw(screen)
        flying_platform_group.update()

        secret_box_group.draw(screen)
        secret_box_group.update()
        appear_group.draw(screen)
        appear_group.update()

        get_in_group.update()
        get_out_group.update()

        break_brick_group.draw(screen)
        break_brick_group.update()
        
        brick_group.draw(screen)
        brick_group.update()

        health_group.draw(screen)
        self.draw_score()

    # reset
    def reset(self):
        enermy_group.empty()
        secret_box_group.empty()
        appear_group.empty()
        brick_group.empty()
        item_group.empty()
        waterfall_group.empty()
        still_water_group.empty()
        lava_waterfall_group.empty()
        lava_group.empty()
        spike_trap_group.empty()
        get_in_group.empty()
        get_out_group.empty()
        flying_platform_group.empty()
        coin_group.empty()
        player_bullet_group.empty()
        enermy_bullet_group.empty()
        carnivorous_plant_group.empty()
        world.reset()
        player.reset()
        if player.died or self.Win:
            health_group.empty()
            immortal.reset()
            set_health()
        # background.reset()
        
    # gameover image
    def gameover_img(self, x, y):
        img = pygame.image.load("images/gameover.png")
        img = pygame.transform.scale(img, (screen_width // 1.5, screen_height // 1.5))
        rect = img.get_rect()
        rect.center = (x, y)

        screen.blit(img, rect)

    def win(self, x, y):
        img = pygame.image.load("images/win.png")
        img = pygame.transform.scale(img, (screen_width // 1.5, screen_height // 1.5))
        rect = img.get_rect()
        rect.center = (x, y)

        screen.blit(img, rect)

        
    def check_limited_level(self):
        level = os.listdir("level")
        count = 1
        for lev in level:
            if lev[6] == str(count):
                count += 1
        return count - 1


# Group
waterfall_group = pygame.sprite.Group()
still_water_group = pygame.sprite.Group()
lava_waterfall_group = pygame.sprite.Group()
lava_group = pygame.sprite.Group()
spike_trap_group = pygame.sprite.Group()
enermy_group = pygame.sprite.Group()
player_bullet_group = pygame.sprite.Group()
enermy_bullet_group = pygame.sprite.Group()
health_group = pygame.sprite.Group()
secret_box_group = pygame.sprite.Group()
appear_group = pygame.sprite.Group()
item_group = pygame.sprite.Group()
break_brick_group = pygame.sprite.Group()
brick_group = pygame.sprite.Group()
get_in_group = pygame.sprite.Group()
get_out_group = pygame.sprite.Group()
flying_platform_group = pygame.sprite.Group()
coin_group = pygame.sprite.Group()
carnivorous_plant_group = pygame.sprite.Group()

# initialization
game = Game()
background = Background()
world = World()  
player = Player()  
player_head = Player_head()  
immortal = Immortal()  

# play again button
playagain_button = Button("images/play_again.png", pixel_width * 8, pixel_height * 3)

music = pygame.mixer.Sound("sound/mario_music.wav")
music.set_volume(1.5)
collect_music = pygame.mixer.Sound("sound/collect_item.wav")
collect_music.set_volume(0.7)
died_music = pygame.mixer.Sound("sound/died.wav")
died_music.set_volume(1.5)
jump_music = pygame.mixer.Sound("sound/jump.wav")
jump_music.set_volume(0.5)
shot_music = pygame.mixer.Sound("sound/shot.wav")
shot_music.set_volume(1)
sword_music = pygame.mixer.Sound("sound/sword.wav")
sword_music.set_volume(0.8)


#==================================================== Loop =========================================================

set_health()
limited_level = game.check_limited_level()
running = True
music.play(-1)
while running:
    key = pygame.key.get_pressed()
    screen.fill((137, 137, 137))
    # draw_grid()
    if player.rect.top > screen_height: health_group.empty()
    if len(health_group) == 0: game.gameover = True

    game.draw_screen()
    transparency.fill((0,0,0))
    transparency.set_alpha(game.transparency_time)
    screen.blit(transparency,(0,0))

    # Winnnnn

    if world.level > limited_level:
        game.Win = True
        if game.transparency_time < 200:
            game.transparency_time += 5
        game.win(screen_width // 2, screen_height // 2)
        playagain_button.draw(screen_width // 2, screen_height //2 + 130)
        if playagain_button.check_click():
            world.level = 1
            world.current_level = 0
            world.curtain = 1
            game.score = 0
            game.reset()
            game.gameover = False
    
    else:
        game.Win = False
        # Gameover
        if game.gameover == True:
            if game.transparency_time < 200:
                game.transparency_time += 5
            game.gameover_img(screen_width // 2, screen_height // 2)
            playagain_button.draw(screen_width // 2, screen_height //2 + 80)
            if playagain_button.check_click():
                world.level = 1
                world.current_level = 0
                world.curtain = 1
                game.score = 0
                game.reset()
                game.gameover = False
                music.play(-1)
        else:
            if game.transparency_time > 0:
                game.transparency_time -= 10

    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False

    clock.tick(fps)
    pygame.display.update()