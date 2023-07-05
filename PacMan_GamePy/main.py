import pygame
import random
import time
import sys
import area
import math
pygame.init()

dirs = ["up", "down", "right", "left"] # Ուղղություններ
screen = pygame.display.set_mode((1200, 1200))# Խաղի պատուհանի չափ
clock = pygame.time.Clock() # Ղեկավարում է կադրերի մաքրությունը FPS
running = True # Խաղային ցիկլի կառավարում
col = "black" # Background գույն
puth = "images" # Ճանապարհ դեպի նկարներ
speed = 50 # Pacman-ի արագությունը
dino_speed = 50 # Dino-ի արագությունը
status = "menu" # Խաղի սկզբնական վիճակ
var = 1
score = 0 # Սկզբնական միավոր
count = 1 # Հաշվիչ
pos = [550, 500] # Pacman-ի սկզբնական դիրքը
pos_mat = [10, 11] # Դիրքը մատրիցի վրա
last_direction = "" # Վերջին ուղղությունը
k = 0 # Dino-ի համար սկզբնական միավոր
board = area.board1 # Խաղատախտակ
area_color = "blue"

# Դինոյի տվյալները
dino = {
    "pos": [[50, 50], [50, 950], [950, 950], [950, 50]],
    "pos_mat": [[1, 1], [1, 19], [19, 19], [19, 1]],
    "color": ["Blue", "Orange", "Pink", "Red"],
    "dir_dino": ["up", "down", "left", "right"],
}
# Խաղախտակի վրա դինոյի դիրքն է թարմացնում
def regul(dino: dict):
    for i in range(4):
        dino["pos_mat"][i][0] = dino["pos"][i][0] // 50
        dino["pos_mat"][i][1] = dino["pos"][i][1] // 50

# Դինոյի համար պատահական ուղղություն է ընտրելում
def rand_dir():
    global dino
    dir = [] # Դատարկ ցուցակ՝ առկա ուղղությունները պահելու համար
    for i in range(4):
        if board[dino["pos_mat"][i][0]][dino["pos_mat"][i][1] - 1] != 0:
            dir.append("up") # Շարշում վերև, եթե առկա է
        if board[dino["pos_mat"][i][0]][dino["pos_mat"][i][1] + 1] != 0:
            dir.append("down") # Շարշում ներքև, եթե առկա է
        if board[dino["pos_mat"][i][0] + 1][dino["pos_mat"][i][1]] != 0:
            dir.append("right")  # Շարշում աջ, եթե առկա է
        if board[dino["pos_mat"][i][0] - 1][dino["pos_mat"][i][1]] != 0:
            dir.append("left")   # Շարշում ձախ, եթե առկա է
    # Պատահական ուղղություն յուրաքանչյուր Dino-ի համար
    for i in range(4):
        dino["dir_dino"][i] = (dir[random.randint(0, len(dir) - 1)])

# Մենյու էկրանն է նկարում
def drow_menu(scereen):
    global icon, copyright, new_game, about, maps, slaq
    screen.fill("black")
    icon = pygame.image.load(puth + f"/pacman.png")
    copyright = pygame.image.load(puth + f"/copyright.png")
    new_game = pygame.image.load(puth + f"/New Game/newgame.png")
    about = pygame.image.load(puth + f"/About/about.png")
    maps = pygame.image.load(puth + f"/Maps/maps.png")

# Խաղի տարածքը նկարելու ֆունկցիա
def draw_area(screen):
    for i in range(len(board)):
        for j in range(len(board[0])):
            # Եթե ընթացիկ բջիջը խոչընդոտ չի պարունակում
            if (board[i][j] != 0):
                # Ստեղծում է ուղղանկյուն կոորդինատներով և չափսերով՝ ելնելով բջջի դիրքից
                rec = pygame.Rect(i * 50, j * 50, 50, 50)
                pygame.draw.rect(screen, area_color, rec) # Էկրանի վրա ուղղանկյուն նկարում ընթացիկ գույնով

# Էկրանի վրա pacman նկարելու ֆունկցիա
def draw_pacman(puth: str):
    global count, last_direction, var
    # Թարմացնում է հաշվարկի արժեքը մոդուլ 8-ով
    count = (count + 1) % 8
    # Եթե հաշվարկը 0-ից 3-ն է ներառյալ
    if count % 8 <= 3:
        if last_direction == "left":
            obj = pygame.image.load(puth + f"/pacs/pacman_left1.png")        
        else:
            obj = pygame.image.load(puth + f"/pacs/pacman_right1.png")
    else:
        # Եթե հաշվարկը 0-ից 3-ի սահմաններից դուրս է
        if last_direction == "left":
            obj = pygame.image.load(puth + f"/pacs/pacman_left-1.png")
        
        else:
            obj = pygame.image.load(puth + f"/pacs/pacman_right-1.png")
    if last_direction == "down":
        # Օբյեկտը պտտում է դեպի ձախ 90 աստիճանով
        obj = pygame.transform.rotate(obj, -90)
        # Պտտում է օբյեկտը աջ 90 աստիճանով
    elif last_direction == "up":
        obj = pygame.transform.rotate(obj, 90)
    elif last_direction == "left":
        # Պտտեցնում է օբյեկտը 0 աստիճանով (առանց ռոտացիայի)
        obj = pygame.transform.rotate(obj, 0)

    screen.blit(obj, (pos[0], pos[1]))

# Էկրանի վրա խնձոր(միավոր) նկարելու ֆունկցիա
def draw_apple(puth: str):
    global score
    for i in range(len(board)):  # Անցնում է խաղադաշտի գծերով
        for j in range(len(board[0])): # Անցնում է խաղադաշտի սյունակներով
            if (board[i][j] == 1): # Եթե ընթացիկ բջիջը պարունակում է խնձոր (արժեքը 1 է)
                obj = pygame.image.load(puth + f"/Apple/apple.png") # Վերբեռնում է խնձորի պատկերը
                screen.blit(obj, (i * 50, j * 50)) # Էկրանի վրա նկարում է խնձորի պատկերը՝ համապատասխան դիրքում

# Էկրանի վրա դինո(թշնամի) նկարելու ֆունկցիա
def draw_dino(dino: dict):
    global k
    k += 1
    if k % 10 == 0: # Ավելացնում է k արժեքը և վերականգնում այն 0-ի յուրաքանչյուր 10 թարմացումից հետո
        k = 0
        rand_dir() # Կանչում է ֆունկցիան՝ պատահականորեն Dino-ի ուղղություն ընտրելու համար
    for i in range(4): # Անցնում է Dino-ի բոլոր մասերով
        color = dino["color"][i] # Ստանում է ընթացիկ Dino-ի մասի գույնը
        name = dino["dir_dino"][i] # Ստանում է ընթացիկ Dino-ի մասի ուղղությունը
        obj = pygame.image.load(f"images/Eggs/{color}_{name}.png") # Վերբեռնում է Dino-ի պատկերը
        screen.blit(obj, (dino["pos"][i][0], dino["pos"][i][1])) # Dino-ին նկարում է էկրանին համապատասխան դիրքում

# Հիմնական խաղային ցիկլ
while running:

    # Խաղի վերահսկում
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # ստեղն esc
    if pygame.key.get_pressed()[pygame.K_ESCAPE]:
        pygame.mixer.stop()
        score = 0
        count = 1
        pos = [550, 500]
        pos_mat = [10, 11]
        last_direction = ""
        k = 0
        board = area.board1

        dino = {
        "pos": [[50, 50], [50, 950], [950, 950], [950, 50]], # Dino-ի կոորդինատները
        "pos_mat": [[1, 1], [1, 19], [19, 19], [19, 1]], # Dino-ի մատրիցայի կոորդինատները
        "color": ["Blue", "Orange", "Pink", "Red"], 
        "dir_dino": ["up","left", "down",  "right"] # Dino-ի շարժման ուղղությունը
        }
        for i in range(len(area.board1)):
            for j in range(len(area.board1[i])):
                if area.board1[i][j] != 0:
                    area.board1[i][j] = 1
                if area.board2[i][j] != 0:
                    area.board2[i][j] = 1
                if area.board3[i][j] != 0:
                    area.board3[i][j] = 1
        # Սկզբնական արժեքներ
        k = 0
        status = "menu"

    # Ստուգում է խաղի ընթացիկ վիճակը
    if status == "menu":
        pygame.mixer.stop() # Դադարեցնում է pygame-ի ձայնը
        score = 0 # Միավորները սկսվում է 0-ից
        count = 1 # Count-ը սկսվում է 1-ից
        pos = [550, 500]  # Տարածքը սկսվում է [550, 500]-ից
        pos_mat = [10, 11] # Մատրիցայի դիրքերը սկսվում են [10, 11]-ից
        last_direction = "" # Դադարեցվում է նախկին շարժանքը
        k = 0 
        board = area.board1 # Մնում է առաջին արեաում

        dino = {
        "pos": [[50, 50], [50, 950], [950, 950], [950, 50]], # Dino-ի կոորդինատները
        "pos_mat": [[1, 1], [1, 19], [19, 19], [19, 1]],  # Dino-ի մատրիցայի կոորդինատները
        "color": ["Blue", "Orange", "Pink", "Red"],
        "dir_dino": ["up","left", "down",  "right"] # Dino-ի շարժման ուղղությունը
        }
        for i in range(len(area.board1)):
            for j in range(len(area.board1[i])):
                if area.board1[i][j] != 0:
                    area.board1[i][j] = 1
                if area.board2[i][j] != 0:
                    area.board2[i][j] = 1
                if area.board3[i][j] != 0:
                    area.board3[i][j] = 1
#___Նկարում է մենյուն___________________________________________________________________________
        drow_menu(screen)
        if pygame.mouse.get_pos()[1] < 440 and pygame.mouse.get_pos()[1] > 335:

            new_game = pygame.image.load(puth + f"/New Game/newgame_shadow.png")  # Մկնիկի շարժումով բեռնում է "New Game Shadow" կոճակի պատկերը
            if pygame.mouse.get_pressed()[0]:
                score = 0
                status = "new game"

        elif pygame.mouse.get_pos()[1] > 515 and pygame.mouse.get_pos()[1] <  620:
            maps = pygame.image.load(puth + f"/Maps/maps_shadow.png")  # Մկնիկի շարժումով բեռնում է "Maps Shadow" կոճակի պատկերը
            if pygame.mouse.get_pressed()[0]:
                status = "maps"
        elif pygame.mouse.get_pos()[1] > 680 and pygame.mouse.get_pos()[1] <  780:
            about = pygame.image.load(puth+ f"/About/about_shadow.png")  # Մկնիկի շարժումով բեռնում է "About Shadow" կոճակի պատկերը
            if pygame.mouse.get_pressed()[0]:
                status = "about"

        screen.blit(icon, (275, 50)) # Icon-ի դիրքը
        screen.blit(copyright, (375, 950)) # Copyright-ի դիրքը
        screen.blit(new_game, (190, 330))  # New Game-ի դիրքը
        screen.blit(maps, (415, 510))  # Maps-ի դիրքը
        screen.blit(about, (350, 675))  # About-ի դիրքը
    #________________________________________________________________________________

    if status == "new game":
        # Մշակում է երաժշտություն խաղի համար
        pygame.mixer.music.load("music/dino.mp3")  # Բեռնում է "dino.mp3" ֆայլը
        pygame.mixer.music.play(1)  # Սկսում է երաժշտական ֆայլը
        screen.fill("black") # Էկրանը ներկում է սև
        draw_area(screen) 
        draw_apple(puth)
        draw_pacman(puth)
        draw_dino(dino)
        font = pygame.font.Font('freesansbold.ttf', 75) # Թեքստի ֆոնտը
        text = font.render(f"{score - 1}", True, "white", "black")
        textRect = text.get_rect()
        textRect.center = (750, 180) # Տեքստի դիրքը
        screen.blit(text, textRect) # Տեղադրում է տեքստը
        sco = pygame.image.load(puth + f"/Score/score.png") # Բեռնում է "Score" նկարը
        screen.blit(sco, (420, 150))
        for i in range(4):
            if math.sqrt((pos[0] - dino["pos"][i][0]) ** 2 + (pos[1] - dino["pos"][i][1]) ** 2)  < 50:
                pygame.mixer.music.load("music/game_over.mp3")
                pygame.mixer.music.play(0)
                status = "game_over"
        if pos_mat in dino["pos_mat"] or pos in dino["pos"]:
            pygame.mixer.music.load("music/game_over.mp3")
            pygame.mixer.music.play(0)
            status = "game_over"
        if True:
            if True:
                if pygame.key.get_pressed()[pygame.K_UP]:
                    if board[pos_mat[0]][pos_mat[1] - 1] != 0:
                        last_direction = "up" # Ստեղնը սեղմելուց վերև
                elif pygame.key.get_pressed()[pygame.K_DOWN]:
                    if board[pos_mat[0]][pos_mat[1] + 1]:
                        last_direction = "down" # Ստեղնը սեղմելուց ներքև
                elif pygame.key.get_pressed()[pygame.K_RIGHT]:
                    if board[pos_mat[0] + 1][pos_mat[1]] != 0:
                        last_direction = "right" # Ստեղնը սեղմելուց աջ
                elif pygame.key.get_pressed()[pygame.K_LEFT]:
                    if board[pos_mat[0] - 1][pos_mat[1]] != 0:
                        last_direction = "left" # Ստեղնը սեղմելուց ձախ
# ______Մշակում Pacman-ի շարժումը_________________________________________________________________
            if True:
                if last_direction == "up":
                    if board[pos_mat[0]][pos_mat[1] - 1] != 0 or pos[1] % 50 != 0:
                        pos[1] -= speed # Ստեղնը սեղմելուց վերև

                elif last_direction == "right":
                    if board[pos_mat[0] + 1][pos_mat[1]] != 0 or pos[0] % 50 != 0:
                        pos[0] += speed # Ստեղնը սեղմելուց աջ

                elif last_direction == "down":
                    if board[pos_mat[0]][pos_mat[1] + 1] != 0 or pos[1] % 50 != 0:
                        pos[1] += speed # Ստեղնը սեղմելուց ներքև

                elif last_direction == "left":
                    if board[pos_mat[0] - 1][pos_mat[1]] != 0 or pos[0] % 50 != 0:
                        pos[0] -= speed # Ստեղնը սեղմելուց ձախ
# ______Մշակում Dino-ի շարժումը___________________________________________________________________
            if True:
                for i in range(4):
                    if dino["dir_dino"][i] == "up":
                        if board[dino["pos_mat"][i][0]][dino["pos_mat"][i][1] - 1] != 0 or dino["pos"][i][1] % 50 != 0:
                            dino["pos"][i][1] -= dino_speed

                    elif dino["dir_dino"][i] == "right":
                        if board[dino["pos_mat"][i][0] + 1][dino["pos_mat"][i][1]] != 0 or dino["pos"][i][0] % 50 != 0:
                            dino["pos"][i][0] +=  dino_speed

                    elif dino["dir_dino"][i] == "down":
                        if board[dino["pos_mat"][i][0]][dino["pos_mat"][i][1] + 1] != 0 or dino["pos"][i][1] % 50 != 0:
                            dino["pos"][i][1] +=  dino_speed

                    elif dino["dir_dino"][i] == "left":
                        if board[dino["pos_mat"][i][0] - 1][dino["pos_mat"][i][1]] != 0 or dino["pos"][i][0] % 50 != 0:
                            dino["pos"][i][0] -=  dino_speed
# _____________________________________________________________________________

        # Հաշվարկվում են տախտակի մատրիցայի ինդեքսները, 
        # որոնք համապատասխանում են pacman-ի ընթացիկ դիրքին: 
        # Pacman-ի կոորդինատները բաժանվում են 50-ի` մատրիցում 
        # համապատասխան ինդեքս ստանալու համար:
        pos_mat[0] = pos[0] // 50
        pos_mat[1] = pos[1] // 50

        #Կանչվում է regul(dino) ֆունկցիան,
        # որը թարմացնում է դինոզավրի դիրքի մատրիցայի կոորդինատները՝
        # ըստ իրենց ընթացիկ կոորդինատների։
        regul(dino) 
        # Այն ստուգում է, թե արդյոք pacman-ի տախտակի մատրիցայի բջիջը (pos_mat) 
        # պարունակում է խնձոր (արժեք 1): Եթե ​​այո, ապա միավորը ավելանում է 1-ով, 
        # իսկ բջջի արժեքը փոխվում է 2-ի՝ ցույց տալու, որ խնձորը կերել է:
        if board[pos_mat[0]][pos_mat[1]] == 1:
            score += 1
            board[pos_mat[0]][pos_mat[1]] = 2 
        # Ստուգվում է՝ արդյո՞ք առավելագույն միավորը (144) հասել է։
        # Եթե ​​այո, ապա խաղի կարգավիճակը սահմանվում է «հաղթել»՝ հաղթանակի 
        # էկրանը ցուցադրելու համար:
        if score == 144:
            status = "win"
    
    if status == "maps":
        # Ցուցադրում է քարտեզի էկրանը
        screen.fill("Black")
        # Բեռնում է պատկերներ և տեքստ    
        copyright = pygame.image.load(puth + f"/copyright.png")
        back = pygame.image.load(puth + f"/back.png")
        screen.blit(copyright, (375, 950))
        icon = pygame.image.load(puth + f"/pacman.png")
        screen.blit(icon, (275, 100))
        area1 = pygame.image.load(puth + f"/Area/area1.png")
        area2 = pygame.image.load(puth + f"/Area/area2.png")
        area3 = pygame.image.load(puth + f"/Area/area3.png")
        # Կախված մկնիկի դիրքից փոխում է նկարը
        if pygame.mouse.get_pos()[1] > 400 and  pygame.mouse.get_pos()[1] < 600 and pygame.mouse.get_pos()[0] > 200  and pygame.mouse.get_pos()[0] < 400:
            if pygame.mouse.get_pressed():
                area_color = "blue"
            area1 = pygame.image.load(puth + f"/Area/area1_shadow.png")
        if pygame.mouse.get_pos()[1] > 400 and  pygame.mouse.get_pos()[1] < 600 and pygame.mouse.get_pos()[0] > 450  and pygame.mouse.get_pos()[0] < 650:
            if pygame.mouse.get_pressed():
                area_color = "green"
            area2 = pygame.image.load(puth + f"/Area/area2_shadow.png")
        if pygame.mouse.get_pos()[1] > 400 and  pygame.mouse.get_pos()[1] < 600 and pygame.mouse.get_pos()[0] > 700  and pygame.mouse.get_pos()[0] < 900:
            if pygame.mouse.get_pressed():
                area_color = "gray"
            area3 = pygame.image.load(puth + f"/Area/area3_shadow.png")
        # Ցուցադրում է ընտրված տարածքները
        screen.blit(area1, (200, 400))
        screen.blit(area2, (450, 400))
        screen.blit(area3, (700, 400))
        if pygame.mouse.get_pos()[1] > 800 and pygame.mouse.get_pos()[0] < 200:
            back = pygame.image.load(puth + f"/back_shadow.png")
        # Ետ է տանում Մենյու
            if pygame.mouse.get_pressed()[0]:
                status = "menu"
        screen.blit(back, (20, 900))

        
        
    if status == "about":
        # About Էկրանի ցուցադրություն
        screen.fill("black")
        # Բեռնում է պատկերներ և տեքստ    
        copyright = pygame.image.load(puth + f"/copyright.png")
        about_text = pygame.image.load(puth + f"/About/about_text.png")
        screen.blit(about_text, (180,150))
        screen.blit(copyright, (375, 975))
        icon = pygame.image.load(puth + f"/pacman.png")
        screen.blit(icon, (275, 30))
        back = pygame.image.load(puth + f"/back.png")
        if pygame.mouse.get_pos()[1] > 800 and pygame.mouse.get_pos()[0] < 200:
            back = pygame.image.load(puth + f"/back_shadow.png")
            # Ետ է վերադարձնում Մենյու
            if pygame.mouse.get_pressed()[0]:
                status = "menu"
        screen.blit(back, (20, 900))
    
    if status == "win":
        # You Win էկրանի ցուցադրություն
        win = pygame.image.load(puth + f"/youwin.png")
        back = pygame.image.load(puth + f"/back.png")
        time.sleep(1)
        screen.fill("black")
        screen.blit(win, (280, 400))
        #Ետ է վերադարձնում Մենյու
        if pygame.mouse.get_pos()[1] > 800 and pygame.mouse.get_pos()[0] < 200:
            back = pygame.image.load(puth + f"/back_shadow.png")

            if pygame.mouse.get_pressed()[0]:
                status = "menu"
        screen.blit(back, (20, 900))
    # Game Over էկրանի ցուցադրություն
    if status == "game_over":
        screen.fill("black")
        back = pygame.image.load(puth + f"/back.png")
        game_over = pygame.image.load(puth + f"/gameover.png")
        screen.blit(game_over, (200, 400))
        if pygame.mouse.get_pos()[1] > 800 and pygame.mouse.get_pos()[0] < 200:
            back = pygame.image.load(puth + f"/back_shadow.png")
        #Ետ է վերադարձնում Մենյու
        if pygame.mouse.get_pressed()[0]:
            status = "menu"
        screen.blit(back, (20,900))
    
    # Էկրանի ցուցադրումը թարմացվում է, 
    # բուֆերները փոխվում են և ուշացում է սահմանվում մինչև հաջորդ թարմացումը՝ 
    # օգտագործելով clock.tick()
    pygame.display.update()
    pygame.display.flip()
    clock.tick(10) 

# Դուրս է գալիս խաղից
pygame.quit()
