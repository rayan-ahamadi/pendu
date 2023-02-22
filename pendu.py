import pygame
from pygame.locals import *
import random
import pygame_gui

motsList = []
with open("mots.txt") as fl:
    for mot in fl:
        motsList.append(mot.rstrip("\n"))


def nouveauMot():
    global motsList
    mot = random.choice(motsList)
    return mot

GREEN = (123,236,17)
GREY = (150,153,148)
YELLOW = (255,255,0)
RED = (255,0,0)
BLACK = (0,0,0)

pygame.init()



size = (640,480)
width, height = size
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Le Pendu")

MANAGER = pygame_gui.UIManager(size,)
CLOCK = pygame.time.Clock()

screen.fill(GREEN)

######ECRAN DU MENU DU JEU#####
def menu():
    screen.fill(GREEN)
    font = pygame.font.SysFont("arial", 35)
    running = True


    screen.blit(font.render("Le Pendu",True,RED),[255,40])
    #Ajout des Boutons
    playButton = Rect(220,150,200,60)
    addWordsButton = Rect(220,240,200,60)
    pygame.draw.rect(screen,GREY,playButton)
    pygame.draw.rect(screen,GREY,addWordsButton)
    
    #Ajout du texte sur les boutons
    playText = font.render("Play",True,BLACK)
    AddWordsText = font.render("Ajout De Mots",True,BLACK)
    screen.blit(playText,playText.get_rect(center=playButton.center))
    screen.blit(AddWordsText,[230,250])


    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                

            #position x et y de la souris     
            hoverPlay = playButton.collidepoint(pygame.mouse.get_pos())
            hoverAdd = addWordsButton.collidepoint(pygame.mouse.get_pos())
            if hoverPlay: 
                pygame.draw.rect(screen,RED,Rect(220,150,200,60),3)
                if event.type == pygame.MOUSEBUTTONUP: 
                    jeu()
            else: 
                pygame.draw.rect(screen,GREY,playButton)
                screen.blit(playText,playText.get_rect(center=playButton.center))

            if hoverAdd: 
                pygame.draw.rect(screen,RED,Rect(220,240,200,60),3)
                if event.type == pygame.MOUSEBUTTONUP: 
                    ajoutDeMot()
            else : 
                pygame.draw.rect(screen,GREY,addWordsButton)
                screen.blit(AddWordsText,[230,250])
            
            pygame.display.update()


def convertList(liste): 
    mot = ""
    for letter in range(0,len(liste)):
        mot = mot + liste[letter]
    
    return mot




####ECRAN DU JEU####
nbErreur = 0
def jeu(): 
    global nbErreur
    mot = str(nouveauMot())
    lettresDeviné = []
    lettreUtilisé = []
    nbErreur = 0
    haveWin = False
    font = pygame.font.SysFont("arial", 25)
    

    def verifLettre(lettre): 
        global nbErreur
        
        if lettre not in mot: 
            nbErreur += 1
            match nbErreur:
                case 1: 
                    pygame.draw.circle(screen,BLACK,[350,100],16)
                case 2: 
                    pygame.draw.line(screen,BLACK,[350,116],[350,170])
                case 3: 
                    pygame.draw.line(screen,BLACK,[350,170],[330,200])
                case 4: 
                    pygame.draw.line(screen,BLACK,[350,170],[380,200])
                case 5: 
                    pygame.draw.line(screen,BLACK,[350,125],[380,150])
                case 6:
                    pygame.draw.line(screen,BLACK,[350,125],[330,150])
                    screen.blit(font.render("Vous avez perdu",True,RED),(380,100))
        else :
            ######### à refaire ########## 
            for lettres in range(0,len(mot)): 
                if mot[lettres] == lettre:
                    lettresDeviné[lettres] = lettre

            x = 123
            for letter in range(0,len(lettresDeviné)):
                lettres = font.render(lettresDeviné[letter],True,BLACK)
                screen.blit(lettres, [x,270])
                x+=30
            pygame.display.update
        
        word = convertList(lettresDeviné)
        if word == mot : 
            screen.blit(font.render("Vous avez gagné",True,YELLOW),(380,100))

    for lettres in mot: 
        lettresDeviné.append("_")

    
    screen.fill(GREEN)
    
    motDevinés = Rect(110,260,410,65)
    pygame.draw.rect(screen,BLACK,motDevinés,5)

    x = 123
    for letter in range(0,len(lettresDeviné)):
        lettres = font.render(lettresDeviné[letter],True,BLACK)
        screen.blit(lettres, [x,270])
        x+=30

    txt = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((290,350),(50,50)),manager=MANAGER,object_id="#text_entry") 

    
    screen.blit(font.render("Lettres utilisées : ",True,BLACK),((110,400)))
    retourMenu = screen.blit(font.render("Retour au Menu",True,BLACK),((110,430)))

    pygame.draw.line(screen,BLACK,(110,240),(515,240))
    pygame.draw.line(screen,BLACK,(220,240),(220,50))
    pygame.draw.line(screen,BLACK,(220,50),(350,50))
    pygame.draw.line(screen,BLACK,(350,50),(350,100))
    

    running = True
    while running:
        UI_REFRESH_RATE = CLOCK.tick(60)/1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
            if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == "#text_entry":
                if nbErreur < 6 and haveWin is not True: 
                    verifLettre(event.text)
                    lettreUtilisé.append(event.text)
                    txtLettreUtilisé = "Lettres utilisées : " + ' - '.join(lettreUtilisé)
                    screen.blit(font.render(txtLettreUtilisé,True,BLACK),((110,400)))
                    txt.clear()
                    pygame.display.update

            if "_" not in lettresDeviné:
            #l'utilisateur a gagné, il peut plus mettre d'autres coups
                haveWin = True
                rejouer = screen.blit(font.render("Rejouer",True,BLACK),((500,430)))
                txt.disable()
                if rejouer.collidepoint(pygame.mouse.get_pos()):
                    rejouer = screen.blit(font.render("Rejouer",True,RED),((500,430)))
                    if event.type == MOUSEBUTTONUP: 
                        nbErreur = 0 
                        txt.hide()
                        jeu()
                else: 
                    rejouer = screen.blit(font.render("Rejouer",True,BLACK),((500,430)))
            elif nbErreur == 6: 
                rejouer = screen.blit(font.render("Rejouer",True,BLACK),((500,430)))
                txt.disable()
                if rejouer.collidepoint(pygame.mouse.get_pos()):
                    rejouer = screen.blit(font.render("Rejouer",True,RED),((500,430)))
                    if event.type == MOUSEBUTTONUP: 
                        nbErreur = 0
                        txt.hide()
                        jeu()
                else: 
                    rejouer = screen.blit(font.render("Rejouer",True,BLACK),((500,430)))

                
                
                     
            if retourMenu.collidepoint(pygame.mouse.get_pos()):
                retourMenu = screen.blit(font.render("Retour au Menu",True,RED),((110,430)))
                if event.type == MOUSEBUTTONUP: 
                    nbErreur = 0
                    menu()
            else: 
                retourMenu = screen.blit(font.render("Retour au Menu",True,BLACK),((110,430)))
    

            MANAGER.process_events(event)
        MANAGER.update(UI_REFRESH_RATE)    
        MANAGER.draw_ui(screen)
        pygame.display.update()
        
        
            

######ECRAN DU CHOIX DE MOTS########
def ajoutDeMot(): 
    screen.fill(GREEN)
    font = pygame.font.SysFont("arial", 50)
    font2 = pygame.font.SysFont("arial", 35)

    TEXT_INPUT = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((width/3.8,height/2),(300,50)),manager=MANAGER,object_id="#text_entry")
    screen.blit(font.render("Ajoutez un mot",True,BLACK),((width/3.5,150)))
    retourMenu = screen.blit(font2.render("Retour au Menu",True,BLACK),((width/3,400)))

    running = True
    pygame.display.update()
    while running:
        UI_REFRESH_RATE = CLOCK.tick(60)/1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
            if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == "#text_entry":
                texte = "\n" + TEXT_INPUT.get_text()
                with open("mots.txt","a") as fl:
                    fl.write(str(texte))
                    fl.close()
                TEXT_INPUT.clear()
                screen.blit(font2.render("Mot ajouté avec succès",True,YELLOW),((width/3.8,50)))
            if retourMenu.collidepoint(pygame.mouse.get_pos()):
                retourMenu = screen.blit(font2.render("Retour au Menu",True,RED),((width/3,400)))
                if event.type == MOUSEBUTTONUP: 
                    menu()
            else: 
                retourMenu = screen.blit(font2.render("Retour au Menu",True,BLACK),((width/3,400)))

            MANAGER.process_events(event)
        MANAGER.update(UI_REFRESH_RATE)    
        MANAGER.draw_ui(screen)
        pygame.display.update()
        
                    
menu()
