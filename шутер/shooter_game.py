from pygame import *
from time import time as timer
mixer.init()
font.init()
from random import *

lost = 0
score = 0
font1 = font.SysFont('Arial',36)
font2 = font.SysFont('Arial',36)
font5 = font.SysFont('Arial',50)
font3 = font.SysFont('Arial',80)
font4 = font.SysFont('Arial',80)
fire = mixer.Sound('mario-fireball.ogg')
shot = mixer.Sound('shot.ogg')
gameover = mixer.Sound('проиграл.ogg')
winer = mixer.Sound('победа.ogg')
loh = mixer.Sound('пропал.ogg')
mixer.music.load('3-underground.ogg')
mixer.music.play()
window = display.set_mode((700,500))
display.set_caption('Шутер')
background = transform.scale(image.load('forest.png'),(700,500))
game = True
finish = False
rel_time = False
rel_time2 = False
num_fire2 = 0
num_fire = 0


class GameSprite(sprite.Sprite):
    def __init__(self,player_image,player_x,player_y,player_speed,shir,vis):
        super().__init__()
        self.image = transform.scale(image.load(player_image),(shir,vis))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
    

class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys_pressed[K_d] and self.rect.x < 620:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('fireball.png',self.rect.centerx,self.rect.top,15,50,50)
        bullets.add(bullet)
    def shot(self):
        hammer = Hammer('hammer.png',self.rect.centerx,self.rect.top,15,70,70)
        hammers.add(hammer)

class Enemy(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y > 500:   
            self.rect.x = randint(80,650)
            self.rect.y = 30
            self.speed = randint(3,6)
            lost += 1
class Knight(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y > 500:   
            self.rect.x = randint(80,650)
            self.rect.y = 30
            self.speed = 2
            lost += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0: 
            self.kill()
class Hammer(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0: 
            self.kill()
        


        
hero = Player('mario.png', 320, 400, 10, 80, 80)
knights = sprite.Group()
enemies = sprite.Group()
bullets = sprite.Group()
hammers = sprite.Group()
for i in range(5):
    raz = randint(40,100)
    enemy = Enemy('boo.png',randint(80,650),30,5,raz,raz)
    enemies.add(enemy)
for i in range(2):
    knight = Knight('knight.png',randint(80,650),30,2,80,95)
    knights.add(knight)

while game: 
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    hero.fire()
                    fire.play()
                    num_fire += 1
                elif num_fire == 5 and rel_time == False:
                    last_time = timer()
                    rel_time = True


            elif e.key == K_e:
                if num_fire2 < 2 and rel_time2 == False: 
                    hero.shot()
                    shot.play()
                    num_fire2 +=1
                elif num_fire2 == 2  and rel_time2 == False:
                    last_time2 = timer()
                    rel_time2 = True   

            elif e.key == K_r:
                if finish == True:
                    finish = False
                    lost = 0
                    score = 0
                    num_fire = 0
                    num_fire2 = 0
                    rel_time = False
                    rel_time2 = False
                    for e in enemies:
                        e.kill()
                    for k in knights:
                        k.kill()
                    for i in range(5):
                        raz = randint(40,100)
                        enemy = Enemy('boo.png',randint(80,650),30,5,raz,raz)
                        enemies.add(enemy)
                    for i in range(2):
                        knight = Knight('knight.png',randint(80,650),30,2,80,95)
                        knights.add(knight)
                    mixer.music.unpause()

            


    if finish != True:
        window.blit(background,(0,0))
        hero.update()
        hero.reset()
        bullets.update()
        bullets.draw(window)
        hammers.update()
        hammers.draw(window)
        if rel_time == True:
            new_time = timer()
            if new_time - last_time < 3:
                reload = font5.render('Перезарядка 1',1,(10,250,250))
                window.blit(reload,(235,450))
            else:
                num_fire = 0
                rel_time = False
        if rel_time2 == True:
            new_time2 = timer()
            if new_time2 - last_time2 < 3:
                reload2 = font5.render('Перезарядка 2',1,(150,50,50))
                window.blit(reload2,(235,400))
            else:
                num_fire2 = 0
                rel_time2 = False
        sprite_list = sprite.groupcollide(enemies,bullets,True,True)
        for sp in sprite_list:
            score += 1
            raz = randint(40,100)
            enemy = Enemy('boo.png',randint(80,650),30,5,raz,raz)
            enemies.add(enemy)
        sprite_list2 = sprite.groupcollide(knights,hammers,True,True)
        for sp in sprite_list2:
            score += 1
            knight = Knight('knight.png',randint(80,650),30,2,80,80)
            knights.add(knight)
        enemies.update()
        enemies.draw(window)
        knights.update()
        knights.draw(window)
        proigral = font3.render('Поражение, нажми r', True, (51,51,255))
        viigral = font4.render('Победа, нажми r', True, (255,255,0))
        text_lose = font1.render('Пропущено:' + str(lost),1, (51,51,255))
        window.blit(text_lose, (10, 10))
        text_win = font2.render('Убито:' + str(score),1, (255,255,0))
        window.blit(text_win, (10, 40))
        if lost > 19:
            window.blit(proigral,(50,200))
            finish = True
            mixer.music.pause()
            gameover.play()
        if score > 29:
            window.blit(viigral,(80,200))
            finish = True
            mixer.music.pause()
            winer.play()



        display.update()
    time.delay(40)