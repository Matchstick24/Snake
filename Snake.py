import pygame
import random

class Snake():

    def __init__(self, Position, Grid, Speed : int, MaxApplesOnScreen : int):
        
        self.Position = Position
        self.Grid = Grid
        self.Segments = [Position]
        self.Direction = (1, 0)
        self.Speed = Speed
        self.Apples = 0
        self.ApplesOnScreen = 0
        self.IsDead = False
        self.MaxApplesOnScreen = MaxApplesOnScreen

    def _SpawnApples(self):

        Grid = self.Grid
        SizeX, SizeY = len(Grid), len(Grid[0])
        RandomPosition = (random.randint(0, SizeX - 1), random.randint(0, SizeY - 1))

        while self.ApplesOnScreen < self.MaxApplesOnScreen:

            if Grid[RandomPosition[0]][RandomPosition[1]] == 0: # Not On The Snake Or Another Apple

                self.ApplesOnScreen += 1
                self.Grid[RandomPosition[0]][RandomPosition[1]] = 2

            RandomPosition = (random.randint(0, SizeX - 1), random.randint(0, SizeY - 1))

    def _Move(self):

        Position = self.Position
        Speed = self.Speed
        Direction = self.Direction
        Grid = self.Grid
        Segments = self.Segments

        NewPosition = (Position[0] + (Direction[0] * Speed), Position[1] + (Direction[1] * Speed))
        SizeX, SizeY = len(Grid), len(Grid[0])

        RemoveTail = True

        if NewPosition[0] > SizeX - 1 or NewPosition[0] <= -1:
            self.IsDead = True
        elif NewPosition[1] > SizeY - 1 or NewPosition[1] <= -1:
            self.IsDead = True

        if not self.IsDead:

            if Grid[NewPosition[0]][NewPosition[1]] == 1: # If It Is Going On Itself
                self.IsDead = True
                return

            if Grid[NewPosition[0]][NewPosition[1]] == 2: # Is An Apple

                self.Apples += 1
                self.ApplesOnScreen -= 1
                RemoveTail = False

            # Updating Snake

            if RemoveTail:

                TailPos = self.Segments[len(Segments) - 1]
                self.Grid[TailPos[0]][TailPos[1]] = 0
        
                del self.Segments[len(Segments) - 1]
        
            self.Segments.insert(0, NewPosition)
            self.Grid[NewPosition[0]][NewPosition[1]] = 1
            self.Position = NewPosition

    def _Control(self):

        Keys = pygame.key.get_pressed()
        Direction = self.Direction

        if Keys[pygame.K_w] and Direction[1] != 1: # Forward
            self.Direction = (0, -1)
        elif Keys[pygame.K_s] and Direction[1] != -1: # Backward
            self.Direction = (0, 1)
        if Keys[pygame.K_d] and Direction[0] != -1: # Right
            self.Direction = (1, 0)
        elif Keys[pygame.K_a] and Direction[0] != 1: # Left
            self.Direction = (-1, 0)

    def Update(self):

        self._Control()
        self._Move()

        if self.ApplesOnScreen < self.MaxApplesOnScreen:
            self._SpawnApples()