import pygame
import sys
import tkinter as tk
from tkinter import messagebox

class Game:
    def __init__(self):
        self.shines = 0
        self.shinesPerClick = 1
        self.clicked = False

        self.upgradeButton = pygame.Rect(10,50,175,75)
        self.upgrade1Cost = 5
        self.upgradeClicked = False

        self.multishineButton = pygame.Rect(200, 50, 175, 75)
        self.multishineCost = 30
        self.multishineCount = 0
        self.multishineClicked = False
        
        self.gameFont = pygame.font.Font(None, 15)

        self.shine = pygame.image.load('shine3.png').convert_alpha()
        self.shine = pygame.transform.scale(self.shine, (150,150))
        self.shineRect = self.shine.get_rect(center=(400, 300))

        self.updateTime = pygame.time.get_ticks()
        self.startTime = pygame.time.get_ticks()
        self.totalTime = 120


    def upgrade(self):
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
        self.display_shines = text_font.render(f"Shines: {str(self.shines)}", True, "#ffffff")
        screen.blit(self.display_shines, (0,565))

        self.displayMultishines = text_font.render(f"Shines Per Second: {str(self.multishineCount)}", True, "#ffffff")
        screen.blit(self.displayMultishines, (0, 535))

    def drawTimer(self):
        self.currentTime = pygame.time.get_ticks()
        elapsedTime = (self.currentTime - self.startTime) // 1000
        remainingTime = self.totalTime - elapsedTime
        timeDisplay = text_font.render(f"Time remaining: {remainingTime} seconds", True, "#ffffff")
        screen.blit(timeDisplay, (0,505))
        return remainingTime
    
    def clickButton(self):
        self.mousePosition = pygame.mouse.get_pos()
        if self.shineRect.collidepoint(self.mousePosition):
            if pygame.mouse.get_pressed()[0]:
                self.clicked = True
            else:
                if self.clicked:
                    self.shines += self.shinesPerClick
                    clickSound.play()
                    self.clicked= False

        if self.upgradeButton.collidepoint(self.mousePosition):
            if pygame.mouse.get_pressed()[0]:
                self.upgradeClicked = True
            else:
                if self.upgradeClicked:
                    if self.shines >= self.upgrade1Cost:
                        self.shines -= self.upgrade1Cost
                        self.upgrade1Cost *= 2
                        self.shinesPerClick += 1
                        upgradeSound.play()
                    self.upgradeClicked = False

        if self.multishineButton.collidepoint(self.mousePosition):
            if pygame.mouse.get_pressed()[0]:
                self.multishineClicked = True
            else:
                if self.multishineClicked:
                    if self.shines >= self.multishineCost:
                        self.shines -= self.multishineCost
                        self.multishineCost *= 2
                        self.multishineCount += 1
                        multishineSound.play()
                    self.multishineClicked = False

    def updateShines(self):
        currentTime = pygame.time.get_ticks()
        if currentTime - self.updateTime >= 1000:
            self.shines += self.multishineCount
            if self.multishineCount > 0:
                clickSound.play()
            self.updateTime = currentTime

    def endGame(self):
        root = tk.Tk()
        root.withdraw()
        messagebox.showinfo("Game Over", f"Your score was {self.shines} shines")
        pygame.quit()
        sys.exit()
        
    def render(self):
        self.updateShines()
        self.clickButton()
        self.drawScore()
        self.upgrade()

        screen.blit(self.shine, self.shineRect)
        remaining_time = self.drawTimer()
        
        pygame.display.update()

        if remaining_time <= 0:
            self.endGame()
        
pygame.init()
width = 800
height = 600

screen = pygame.display.set_mode(size=(width,height))
pygame.display.set_caption('Shine Clicker')

backgroundImage = pygame.image.load('backgroundImage.jpg')
backgroundImage = pygame.transform.scale(backgroundImage, (width, height))

clickSound = pygame.mixer.Sound('shine.wav')
upgradeSound = pygame.mixer.Sound('toryah.wav')
multishineSound = pygame.mixer.Sound('taunt.wav')

pygame.mixer.music.load('corneria.mp3')
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1)

text_font = pygame.font.Font(None, 50)
title = text_font.render("Shine Clicker!", True, "#ffffff")

clock = pygame.time.Clock()
game = Game()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.blit(backgroundImage, (0,0))
    screen.blit(title, (50,15))

    game.render()
    
    pygame.display.update()
    clock.tick(60)
