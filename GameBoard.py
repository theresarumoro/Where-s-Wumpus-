'''
Caroline Canfield, Theresa Rumoro, Emily Walden
Where's Wumpus?

GameBoard creates the board and playes the Wumpus, pit, stench, and breeze.
'''


# Import libraries and other classes
from GameCell import GameCell
from fpdf import FPDF
import random
import pygame


# Set board dimension to 4
board_dimension = 4


class GameBoard:
    

    # Constructor
    def __init__(self):
        self.game_board = []


    # Creates a board based off the board_dimenstion attribute and calls the class
    # constructor to initialize the class
    def initialize(self):
        # Call global variable
        global board_dimension
        # Declare variable
        board = []
        # Create the columns of the board
        x = 1
        while x <= board_dimension:
            # Empty array to hold an array that will comprise a row
            row = []
            # Traverse through the current array to put a cell in it
            i = 1
            while i <= board_dimension:
                # Create a cell
                cell = GameCell()
                # Push that cell onto the current row
                row.append(cell)
                i += 1
            x += 1
            # Once all all indexes of that row have had cells placed in them
            # push that row onto the game board
            board.append(row)
        # Set the board created to the game_board attribute of the class
        self.game_board = board
    

    # Get the cell
    def getGameCell(self, col, row):
        gameCell = self.game_board[col][row]
        return gameCell


    # Get the board
    def getGameBoard(self):
        return self.game_board


    # Will check if the given coordinates on the board are empty from any obstacle
    # returns true if there is not an obstacle present
    def is_spot_empty(self, col, row):
        # Get the spot in question
        my_spot = self.game_board[col][row]
        # Check if the wumpus is in that spot
        if my_spot.get_wumpus():
            return False
        # Check if a pit is in the spot
        if my_spot.get_pit():
            return False
        # Check if a gold is in the spot
        if my_spot.get_gold():
            return False
        # Check if a wind is in the spot
        if my_spot.get_breeze():
            return False
        # Check if a stench is in the spot
        if my_spot.get_stench():
            return False
        # If neither are present, return true
        else:
            return True


    # Checks to see if a given number is in the index of the array that
    # comprises the board
    def in_index(self, num):
        if num > board_dimension - 1:
            return False
        if num < 0:
            return False
        else:
            return True


    # Places stench from the wumpus in the four spots surrounding the given coordinate
    def set_stench(self, col, row):
        # Set variables
        top = row + 1
        bottom = row - 1
        left = col + 1
        right = col - 1
        # Place warnings in the surrounding spots
        if self.in_index(top):
            self.game_board[col][top].set_stench()
        if self.in_index(bottom):
            self.game_board[col][bottom].set_stench()
        if self.in_index(left):
            self.game_board[left][row].set_stench()
        if self.in_index(right):
            self.game_board[right][row].set_stench()


    # Places breeze from pits in the four spots surrounding the given coordinate
    def set_breeze(self, col, row):
        # Set variables
        top = row + 1
        bottom = row - 1
        left = col + 1
        right = col - 1
        # Place warnings in the surrounding spots
        if self.in_index(top):
            self.game_board[col][top].set_breeze()
        if self.in_index(bottom):
            self.game_board[col][bottom].set_breeze()
        if self.in_index(left):
            self.game_board[left][row].set_breeze()
        if self.in_index(right):
            self.game_board[right][row].set_breeze()


    # Will generate random coordinates that correspond with the board size
    def generate_coordinate(self):
        # Call global variable
        global board_dimension
        # Set variable
        available = []
        # Set to 1 so that nothing is placed in initial spot
        x = 1
        while x < board_dimension:
            # Set to 1 so that nothing is placed in initial spot
            y = 1
            while y < board_dimension:
                if(self.is_spot_empty(x,y)):
                    available.append([x,y])
                y+=1
            x+=1
        # Choose a random variable
        coord_choice = random.choice(available)
        col = coord_choice[0]
        row = coord_choice[1]
        # Return the values
        return col, row


    # Places the wumpus and a stench in the surrounding spots
    def place_wumpus(self):
        # Generate a coordinate
        col, row = self.generate_coordinate()
        # Check if there is an obstacle already in that spot
        if self.is_spot_empty(col, row):
            # If it is, set the wumpus there
            self.game_board[col][row].set_wumpus()
            # Set the stench in the spots around there
            self.set_stench(col, row)
        # If the spot is not empty, call the function again to try again with a new coordinate
        else:
            self.place_wumpus()


    # Places the pit and a breeze in the surrounding spots
    def place_pit(self):
        # Generate a coordinate
        col, row = self.generate_coordinate()
        # Check if there is an obstacle already in that spot
        if self.is_spot_empty(col, row):
            # If it is, set the pit there
            self.game_board[col][row].set_pit()
            # Set the breeze in the spots around there
            self.set_breeze(col, row)
        # If the spot is not empty, call the function again to try again with a new coordinate
        else:
            self.place_pit()


    # Places gold by generating a random coordinate
    def set_gold(self):
        # Generate a random coordiante
        col, row = self.generate_coordinate()
        # Check if that spot is empty
        if self.is_spot_empty(col, row):
            # If spot is empty, set the gold to the coordinate generated
            self.game_board[col][row].set_gold()
        # If the spot is not empty call the function again
        else:
            self.set_gold()


    # Prints the board
    def print_board(self, outFile):
        pygame.init()
        # Load and scale images
        screen = pygame.display.set_mode((400,400),pygame.HIDDEN)
        gold = pygame.image.load('gold.jpg')
        gold =pygame.transform.scale(gold,(60,60))
        breeze = pygame.image.load('breeze.jpg')
        breeze =pygame.transform.scale(breeze,(80,80))
        wumpus = pygame.image.load('wumpus.png')
        wumpus =pygame.transform.scale(wumpus,(80,80))
        stench = pygame.image.load('stench.jpg')
        stench =pygame.transform.scale(stench,(80,80))
        pit = pygame.image.load('pit.jpg')
        pit =pygame.transform.scale(pit,(80,80))
        
        x = 0
        while x < board_dimension:
            y = 0
            while y < board_dimension:
                #in each game cell
                pygame.draw.rect(screen, "white", (x*100, y*100, 100, 100), 0)
                pygame.draw.rect(screen, "black", (x*100, y*100, 100, 100), 1)
                cell=pygame.Surface((x*100,y*100))                
                
                if (self.game_board[x][y].get_stench()):
                    screen.blit(stench,(x*100+5,y*100+10))
                    
                if (self.game_board[x][y].get_wumpus()):
                    screen.blit(wumpus,(x*100+5,y*100+10))
                    
                if (self.game_board[x][y].get_pit()):
                    screen.blit(pit,(x*100+5,y*100+10))  
                    
                if (self.game_board[x][y].get_gold()):
                    screen.blit(gold,(x*100+12,y*100+15))
                    
                if (self.game_board[x][y].get_breeze()):
                    screen.blit(breeze,(x*100+5,y*100+10)) 
                    
                y+=1
            x += 1

        # Save cheat sheet screen as image
        pygame.image.save(screen, "CheatSheet.png")
        
        outFile.add_page()

        outFile.image("CheatSheet.png")

