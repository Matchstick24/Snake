import pygame
import json

pygame.init()

# Colours

Green = (0, 255, 0)
Black = (0, 0, 0)
Red = (255, 0, 0)

# Settings

ScreenX, ScreenY = (1000, 600)
Fps = 11
Name = "Snake"

CellSize = 10
Cols = 80
Rows = 60
StartPosition = (50, 25)
MaxApples = 80

BackgroundScale = (180, 500)
BackgroundPos = (800, 50)

CellColours = {

    1 : Green, # Snake
    2 : Red, # Apples

}

Font = pygame.font.SysFont("Arial", 30)

# Variables

Clock = pygame.time.Clock()
Running = True
Grid = {}
Time = 0

import Snake as SnakeModule

# Main

Screen = pygame.display.set_mode((ScreenX, ScreenY))
pygame.display.set_caption(Name)

# Functions

def DrawText(Text, TextFont, Colour, x, y):

    Image = TextFont.render(str(Text), True, Colour)
    Screen.blit(Image, (x, y))

def Setup_Grid(Grid):

    for x in range(0, Cols + 1):
        Grid[x] = {}
        for y in range(0, Rows + 1):
            Grid[x][y] = 0

def Render_Grid():

    for x in range(0, Cols + 1):
        for y in range(0, Rows + 1):

            # Draw To Screen

            if Grid[x][y] == 0: continue # If It Is Nothing

            Colour = CellColours[Grid[x][y]]
            Rect = pygame.Rect(x * CellSize, y * CellSize, CellSize, CellSize)
            
            pygame.draw.rect(Screen, Colour, Rect)

def Render_Text():

    Background = pygame.transform.scale(pygame.image.load("Background.bmp").convert_alpha(), BackgroundScale)
    Screen.blit(Background, BackgroundPos)
    DrawText(f"Apples : {str(Snake.Apples)}", Font, (0, 0, 0), 810, 130)
    DrawText(f"Time : {str(int(Time))}", Font, (0, 0, 0), 810, 180)

    with open("Score", "r") as File:
        
        Data = json.load(File)

        DrawText("HI_Apples : " + str(Data["HI_Apples"]), Font, (0, 0, 0), 810, 230)
        DrawText("HI_Time : " + str(int(Data["HI_Time"])), Font, (0, 0, 0), 810, 280)

# Loop

Setup_Grid(Grid)
Snake = SnakeModule.Snake(StartPosition, Grid, 1, MaxApples)

while Running:

    # Controls

    for Event in pygame.event.get():
        if Event.type == pygame.QUIT:
            Running = False

    # Render

    Screen.fill(Black)

    if Snake.IsDead:

        Grid = {}

        Image = pygame.image.load("Restart.bmp").convert_alpha()
        Screen.blit(Image, (300, 100))

        Keys = pygame.key.get_pressed()
        Data = False

        with open("Score", "r") as File:
            Data = json.load(File)

        if Keys[pygame.K_e]:

            # Save

            with open("Score", "w") as File:

                ToWrite = {
                    
                    "HI_Apples" : Data["HI_Apples"],
                    "HI_Time" : Data["HI_Time"]
                    
                }

                if Snake.Apples > Data["HI_Apples"]: 
                    ToWrite["HI_Apples"] = Snake.Apples
                if Time > Data["HI_Time"]: 
                    ToWrite["HI_Time"] = Time

                json.dump(ToWrite, File)

            Setup_Grid(Grid)
            Snake = SnakeModule.Snake(StartPosition, Grid, 1, MaxApples)
            Time = 0
                
    else:
        
        Render_Grid()
        Snake.Update()
        Time += (1 / Fps)

    Render_Text()

    pygame.display.flip()
    Clock.tick(Fps)

pygame.quit()    