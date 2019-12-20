from deneme1 import *

size = (1000, 600)
screen = pygame.display.set_mode(size, 32)

ship = Ship(size)
shot_L = []
explosion_L = []
enemy_L = []
star_L = []

shot_s = pygame.mixer.Sound("shot.wav")

wait = 0
time = 0

gameover = pygame.image.load("game-over.png")

gameover_r = gameover.get_rect()
gameover_r = gameover_r.move([size[0] / 2 - gameover_r.width / 2, size[1] / 2 - gameover_r.height / 2])

score = 0

pygame.mouse.set_visible(False)

song = pygame.mixer.Sound("starwars.wav")
song.play(-1)

for star in range(100):
    star_L.append(Star(size))

    # oyun başlıyor

while 1:
    time += 1
    keys = pygame.key.get_pressed()

    if keys[K_SPACE] and not wait and ship != None:
        shot_L.append(Shot(ship.rect.center, 'right'))
        shot_s.play()
        wait = True

    if not keys[K_SPACE]: wait = False

    # düşman oluşturma
    if time % (1000000 / (score + 1) + 1) == 0:
        if random.randint(0, 1) == 0:
            enemy_L.append(Enemy2(list((size[0] + 100, random.randint(50, size[1] - 50)))))
        else:
            enemy_L.append(Enemy1([size[0] + 100, random.randint(50, size[1] - 50)]))
    if time % 100 == 0: enemy_L.append(Enemy1([size[0] + 100, random.randint(50, size[1] - 50)]))

    # ateş etmek
    for shot in shot_L:
        shot.update(screen)
        if shot.rect[0] > size[0]:
            shot_L.remove(shot)

            # patlama efekti update
    for patlama in explosion_L:
        patlama.update(screen)
        if patlama.life <= 0:
            explosion_L.remove(patlama)

            # düşman update
    for enemy in enemy_L:

        enemy.update(screen, time, ship)

        # düşmana çarpınca ölüm
        if ship != None and enemy.rect.colliderect(ship.rect):
            pygame.time.wait(50)
            screen.fill([255, 0, 0])

            explosion_L.append(Patlama(ship_pos))
            ship = None
            enemy_L.remove(enemy)

            # ekrandan çıkanı sil ve skoru azalt
        if enemy.rect.left < -50:
            enemy_L.remove(enemy)
            if ship != None: score -= 10

            # ateş edince öldür ve skor ekle
        for shot in shot_L:
            if shot.rect.colliderect(enemy.rect):
                explosion_L.append(Patlama(enemy.rect.center))

                try:
                    enemy_L.remove(enemy)
                except:
                    pass
                shot_L.remove(shot)

                if ship != None: score += 30

                # gemi çarparsa update
    if ship != None:
        ship.update(screen, keys, size)
        ship_pos = ship.rect.topleft
    else:
        screen.blit(gameover, gameover_r)
        song.stop()

        # arkaplan yıldız
    for star in star_L:
        star.update(screen)

        # skor
    score = max(0, score)

    score_t = pygame.font.SysFont("arial", 30).render('score - ' + str(score), False, (255, 255, 255))
    score_t_r = score_t.get_rect()
    score_t_r = score_t_r.move([size[0] / 2 - score_t_r.width / 2, size[1] - size[1] / 10])

    screen.blit(score_t, score_t_r)

    # screen update
    pygame.display.flip()
    screen.fill([0, 0, 0])

    for event in pygame.event.get():
        if event.type == QUIT or keys[K_ESCAPE]:
            pygame.quit();
            sys.exit()


