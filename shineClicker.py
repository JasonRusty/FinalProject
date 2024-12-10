import pygame
import sys
import tkinter as tk #used for endGame function - quits out and displays pop up window
from tkinter import messagebox

class Game:
    def __init__(self):
        #Player's shine count and how many shine's they earn per click
        self.shines = 0
        self.shinesPerClick = 1
        self.clicked = False

        #Buttons for upgrading the shine button and purchasing the multishine
        self.upgradeButton = pygame.Rect(10,50,175,75)
        self.upgrade1Cost = 5
        self.upgradeClicked = False

        self.multishineButton = pygame.Rect(200, 50, 175, 75)
        self.multishineCost = 30
        self.multishineCount = 0
        self.multishineClicked = False
        
        self.gameFont = pygame.font.Font(None, 15)

        #load the shine image and put it in the center of the screen
        self.shine = pygame.image.load('shine3.png').convert_alpha()
        self.shine = pygame.transform.scale(self.shine, (150,150))
        self.shineRect = self.shine.get_rect(center=(400, 300))

        #setting up the game timing
        self.updateTime = pygame.time.get_ticks()
        self.startTime = pygame.time.get_ticks()
        self.totalTime = 120 #total time to play the game


    def upgrade(self):
        #render the upgrade buttons and their descriptions
        self.upgrade1Description = self.gameFont.render(f"+{self.shinesPerClick} Shine per click.", True, "#ffffff")
        self.displayCost = text_font.render(f"Cost: {self.upgrade1Cost}", True, "#ffffff")

        pygame.draw.rect(screen, "#488ebd", self.upgradeButton, border_radius = 15)
        screen.blit(self.displayCost, (15,85))
        screen.blit(self.upgrade1Description, (15,55))

        self.multishineDescription = self.gameFont.render(f"+1 Shine Per Second", True, "#ffffff")
        self.multishineDisplayCost = text_font.render(f"Cost: {self.multishineCost}", True, "#ffffff")

        pygame.draw.rect(screen, "#488ebd", self.multishineButton, border_radius=15)
        screen.blit(self.multishineDisplayCost, (205, 85))
        screen.blit(self.multishineDescription, (205, 55))
        
    def drawScore(self):
        #display the score and shines per second to the screen
        self.display_shines = text_font.render(f"Shines: {str(self.shines)}", True, "#ffffff")
        screen.blit(self.display_shines, (0,565))

        self.displayMultishines = text_font.render(f"Shines Per Second: {str(self.multishineCount)}", True, "#ffffff")
        screen.blit(self.displayMultishines, (0, 535))

    def drawTimer(self):
        #render the timer and update the remaining time
        self.currentTime = pygame.time.get_ticks()
        elapsedTime = (self.currentTime - self.startTime) // 1000
        remainingTime = self.totalTime - elapsedTime
        timeDisplay = text_font.render(f"Time remaining: {remainingTime} seconds", True, "#ffffff")
        screen.blit(timeDisplay, (0,505))
        return remainingTime
    
    def clickButton(self):
        #checks for mouse click interactions
        self.mousePosition = pygame.mouse.get_pos()
        #check if player clicked the shine image
        if self.shineRect.collidepoint(self.mousePosition):
            if pygame.mouse.get_pressed()[0]:
                self.clicked = True
            else:
                if self.clicked:
                    self.shines += self.shinesPerClick
                    clickSound.play()
                    self.clicked= False #ensures that multiple clicks do not happen erroneously

        #check if the upgrade button was clicked
        if self.upgradeButton.collidepoint(self.mousePosition):
            if pygame.mouse.get_pressed()[0]:
                self.upgradeClicked = True
            else:
                if self.upgradeClicked:
                    if self.shines >= self.upgrade1Cost:
                        self.shines -= self.upgrade1Cost
                        self.upgrade1Cost *= 2 #double the cost of the next upgrade
                        self.shinesPerClick += 1
                        upgradeSound.play()
                    self.upgradeClicked = False

        #checks if the multishine button was clicked
        if self.multishineButton.collidepoint(self.mousePosition):
            if pygame.mouse.get_pressed()[0]:
                self.multishineClicked = True
            else:
                if self.multishineClicked:
                    if self.shines >= self.multishineCost:
                        self.shines -= self.multishineCost
                        self.multishineCost *= 2 #doubles the cost of the next multishine purchase
                        self.multishineCount += 1
                        multishineSound.play()
                    self.multishineClicked = False

    def updateShines(self):
        #checks the time and increments up based on how many multishines the player bought
        currentTime = pygame.time.get_ticks()
        if currentTime - self.updateTime >= 1000:
            self.shines += self.multishineCount
            if self.multishineCount > 0:
                clickSound.play()
            self.updateTime = currentTime

    def endGame(self):
        #ends the game and displays player's final score
        root = tk.Tk()
        root.withdraw()
        messagebox.showinfo("Game Over", f"Your score was {self.shines} shines")
        pygame.quit()
        sys.exit()
        
    def render(self):
        #main game rendering and updating
        self.updateShines()
        self.clickButton()
        self.drawScore()
        self.upgrade()

        screen.blit(self.shine, self.shineRect)
        remaining_time = self.drawTimer()
        
        pygame.display.update()

        if remaining_time <= 0:
            self.endGame()

#initializing pygame and setting up the window
pygame.init()
width = 800
height = 600

screen = pygame.display.set_mode(size=(width,height))
pygame.display.set_caption('Shine Clicker')

#loading background image and sounds
backgroundImage = pygame.image.load('backgroundImage.jpg')
backgroundImage = pygame.transform.scale(backgroundImage, (width, height))

clickSound = pygame.mixer.Sound('shine.wav')
upgradeSound = pygame.mixer.Sound('toryah.wav')
multishineSound = pygame.mixer.Sound('taunt.wav')

#plays background music in a loop
pygame.mixer.music.load('corneria.mp3')
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1)

#creates font and sets window title
text_font = pygame.font.Font(None, 50)
title = text_font.render("Shine Clicker!", True, "#ffffff")

#creates game object and clock
clock = pygame.time.Clock()
game = Game()

#main game loop:
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    #updates the game screen to render title and background
    screen.blit(backgroundImage, (0,0))
    screen.blit(title, (50,15))

    #calls the render function
    game.render()

    #updates display and sets frame rate
    pygame.display.update()
    clock.tick(60)
