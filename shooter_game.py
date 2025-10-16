#Создай собственный Шутер
from time import time as timer
from pygame import *
from random import randint
font.init()
mixer.init()
window = display.set_mode((700, 500))
display.set_caption("Шутер")
galaxy = transform.scale(image.load("galaxy.jpg"), (700, 500))
font = font.Font(None, 36)
clock = time.Clock()
count = 0
# mixer.music.load("space.ogg")
# mixer.music.play()

class GameSprite(sprite.Sprite):
    def __init__(self, sprite_image, x, y, speed, width, height):
        super().__init__()
        self.image = transform.scale(image.load(sprite_image), (width, height))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
        
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < 620:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet("bullet.png", self.rect.centerx, self.rect.top, 5, 15, 20)
        bullets.add(bullet)

lost = 0 
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y >= 500:
            self.rect.y = 0
            self.rect.x = randint(50, 650)
            lost += 1
        
class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        global count
        if self.rect.y <= 0:
            self.kill()
        


bullets = sprite.Group()
monsters = sprite.Group()
asteroids = sprite.Group()

player = Player("rocket.png", 5, 400, 5, 80, 100)
for i in range(5):
    enemy = Enemy("ufo.png", randint(50, 650), -50, 3, 80, 50)
    monsters.add(enemy)
for i in range(3):
    asteroid = Enemy("asteroid.png", randint(50, 650), -50, 3, 80, 50)
    asteroids.add(asteroid)
life = 3
rel_time = False
num_fire = 0
finish = False
game = True
while game:
    if finish != True:
        text_lost = font.render("Пропущено:" + str(lost), 1, (255, 255, 255))
        text_count = font.render("Счет:" + str(count), 1, (255, 255, 255))
        text_life = font.render("Жизни:"+str(life), 1, (255, 255, 255))
        text_rel = font.render("Wait, reload...", 1, (245, 17, 17))
        window.blit(galaxy, (0, 0))
        player.update()
        player.reset()
        monsters.update()
        monsters.draw(window)
        asteroids.update()
        asteroids.draw(window)
        bullets.update()
        bullets.draw(window)
        window.blit(text_lost, (5, 0))
        window.blit(text_count, (5, 25))
        window.blit(text_life,(5, 50))
        
        sprites_list = sprite.groupcollide(monsters, bullets, True, True)
        for i in sprites_list:
            count += 1
            enemy = Enemy("ufo.png", randint(50, 650), -50, 3, 80, 50)
            monsters.add(enemy)
        if lost >= 3 or sprite.spritecollide(player, monsters, False) or life == 0:
            lose = font.render("ПРОИГРЫШ", 1, (255, 255, 255))
            window.blit(lose, (350, 250))
            finish = True
            
        if count == 10:
            win = font.render("ПОБЕДА", 1, (255, 255, 255))
            window.blit(win, (350, 250))
            finish = True
        if sprite.spritecollide(player, asteroids, True) or sprite.spritecollide(player, monsters, True):
            life -= 1
        if rel_time == True:
            end = timer()
            if end-start >= 3:
                num_fire = 0
                rel_time = False
            else:
               window.blit(text_rel, (500, 250)) 
    else:
        count = 0 
        lost = 0
        life = 3
        finish = False
        for i in monsters:
            i.kill()
        for i in bullets:
            i.kill()
        for i in asteroids:
            i.kill()
        time.delay(5000)
        for i in range(5):
            enemy = Enemy("ufo.png", randint(50, 650), -50, 3, 80, 50)
            monsters.add(enemy)
        for i in range(3):
            asteroid = Enemy("asteroid.png", randint(50, 650), -50, 3, 80, 50)
            asteroids.add(asteroid)
    for e in event.get():
        if e.type == QUIT:
            game =  False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:     
                if rel_time == False and num_fire < 5:
                    num_fire += 1
                    player.fire()
                else:
                    rel_time = True
                    start = timer()
                

    display.update()
    clock.tick(60)
    