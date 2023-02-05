'''
Caroline Canfield, Theresa Rumoro, Emily Walden
Where's Wumpus?

Agent moves along the GameBoard and finds new information to find the gold and win.
'''

# Import other classes and libraries
from GameBoard import GameBoard
from GameCell import GameCell
from Knowledge import Knowledge
from Knowledge import safe_array
from Knowledge import visited_array
from Knowledge import stench_array
from Knowledge import breeze_array
from Knowledge import wumpus
from Knowledge import pit
from Knowledge import board_dimension
from fpdf import FPDF
import random
import pygame
import os


class Agent:


    # Constructor
    def __init__(self):
        self.current_spot = []
        self.surrounding_spots = []
        self.my_knowledge = Knowledge()
        self.previous_spot = []


    # Setters
    def set_current_spot(self, spot):
        self.current_spot = spot     
    def set_surrounding_spots(self, array):
        self.surrounding_spots = array
    def set_previous_spot(self):
        self.previous_spot = self.current_spot

    # Getters
    def get_current_spot(self):
        return self.current_spot
    def get_surrounding_spots(self):
        return self.surrounding_spots
    def get_previous_spot(self):
        return self.previous_spot


    # Will return true if the agent's current spot contains a warning
    def found_warning(self):
        # Variables for the collumn and row of the agent's current spot
        col = self.current_spot[0]
        row = self.current_spot[1]
        # Varibale for the board's data of the current spot of the agent
        board_spot = GameBoard.game_board[col][row]
        # If the current spot of the agent on the board holds a breeze or a stench
        if board_spot.get_breeze() or board_spot.get_stench():
            return True
        else:
            return False


    # If the current spot is not a warning, should return true
    def should_explore(self):
        if self.found_warning:
            return False
        else:
            return True


    # Updates and sets surrounding spots
    def update_surrounding_coords(self):
        # Call surrounding spots from the knowledge base to update the surrounding coordinates
        surrounding_coords = self.my_knowledge.surrounding_spots(self.current_spot[0], self.current_spot[1])
        self.set_surrounding_spots(surrounding_coords)


    # Returns array of the spots that have yet to be explored out of the surrounding coordinates
    def near_unexplored(self):
        # Check to see if the visited array is empty
        if len(visited_array) == 0:
            return self.surrounding_spots
        # Lenth of the surrounding spots array
        surrounding_length = len(self.surrounding_spots)
        # Array to store the spots that have not been explored
        unexplored = []
        x = 0
        # Begin indexing through the surrounding array
        while x < surrounding_length:
            #i = 0
            if len(visited_array) == 1:
                # Return the unexplored spots as the surrounding spots
                unexplored=self.surrounding_spots
                x+=1
            # Check if you have reached the end of the visited array
            # and the last spot in the visited array is not the same as
            # the current spot in the surrounding spots array
            elif (not(self.surrounding_spots[x] in visited_array)):
                unexplored.append(self.surrounding_spots[x])
                x+=1
            else:
                x+=1
        # If the Wumpus and pit have been found, remove them from unexplored
        if (((len(wumpus) != 0) and (wumpus[0] in unexplored)) and ((len(pit) != 0) and (pit[0] in unexplored))):
            unexplored.remove(wumpus[0])
            unexplored.remove(pit[0])
        # Else if the pit has been found, remove it from unexplored
        elif ((len(pit) != 0) and (pit[0] in unexplored)):
            unexplored.remove(pit[0])
        # Else if the Wumpus has been found, remove it from unexplored
        elif ((len(wumpus) != 0) and (wumpus[0] in unexplored)):
            unexplored.remove(wumpus[0])            
        return unexplored


    # Will return array of surrounding spots that are confirmed safe based on the knowledge base
    def near_safe(self):
        # Call global variable
        global safe_array
        # Create variables
        safe_spots = []
        surrounding_length = len(self.surrounding_spots)
        # Check to see if there are any spots in the safe array
        if len(safe_array) == 1:
            # If so, return an empty array
            return safe_spots
        # Else, append surrounding spots to safe_spots
        else:
            for i in range(surrounding_length):
                if self.surrounding_spots[i] in safe_array:
                    safe_spots.append(self.surrounding_spots[i])
        return safe_spots


    # Updates all arrays
    def update_arrays(self, boardSpot, col, row):
        # Call global variables
        global stench_array
        global breeze_array
        global visited_array
        global safe_array
        # Create variables
        coord = []
        coord.append(col)
        coord.append(row)
        # If not in the array
        if coord not in visited_array:
            # Update the visited array
            visited_array.append(coord)
            boardSpot.set_visited()
        # If not in the array
        if coord not in stench_array:
            # If the board spot has a stench
            if(boardSpot.get_stench()):
                # Append to array
                stench_array.append(coord)
        # If not in the array
        if coord not in breeze_array:
            # If the board spot has a breeze
            if(boardSpot.get_breeze()):
                # Append to array
                breeze_array.append(coord)
        # If not in the array
        if coord not in safe_array:
            # If the board spot is a safe space
            if(boardSpot.get_wumpus() == False & boardSpot.get_pit() == False):
                # Append to array
                safe_array.append(coord)
                boardSpot.set_safe_space()


    # Chooses random spot based on the array inputed
    def randoSpot(self, array):
        limit = len(array)
        index = random.randint(0, limit-1)
        spot = array[index]
        return spot


    # Explore and examine the board
    def explore(self, game, outFile,num):
        # Call global variables
        global visited_array
        global wumpus
        global pit
        # Declare variable for the spot selected
        mySpot = []
        # Get the coordinate of the current spot
        spot = self.get_current_spot()
        xCol = spot[0]
        yRow = spot[1]
        print("\nMove ", num, ":")
        print("\tCurrent Spot: ", xCol, ", ", yRow)
        # Update the current surrounding coordinates
        self.update_surrounding_coords()
        # Get data of the current spot of the game board
        board_spot = game.getGameCell(xCol, yRow)
        # Set this spot as visited and print current board
        self.set_visited(game, xCol, yRow)
        self.print_board(outFile, game, num)
        # Update the knowledge base arrays
        self.update_arrays(board_spot, xCol, yRow)
        # If the gold was found, the agent won
        if board_spot.get_gold():
            print("\n\tCongrats! The gold was found in spot ", spot, "!", "\n")
            self.my_knowledge.set_goldFound()
        # If the Wumpus was found, the agent lost
        elif board_spot.get_wumpus():
            print("\n\tBetter luck next time! You got attacked by the Wumpus in spot ", spot, "!", "\n")
            exit(0)
        # If the pit was found, the agent lost
        elif board_spot.get_pit():
            print("\n\tBetter luck next time! You fell in the pit in spot ", spot, "!", "\n")
            exit(0)
        # Else, the agent needs to explore
        else:
            # Check if the current spot has a warning and the pit or Wumpus were not found yet
            if ((board_spot.get_breeze() and len(pit) == 0) or (board_spot.get_stench() and len(wumpus) == 0)):
                # Check to see if a danger can be identified
                myDanger = self.my_knowledge.locate_danger(xCol, yRow)
                # Check to make sure myDanger is not noneType
                if myDanger is not None:
                    myDanger = game.getGameCell(xCol, yRow)
                    # Set visited, BUT not safe!
                    myDanger.set_visited()
                # Since the agent is in a warning spot, it should try to explore a safe spot
                # if there are spots that are determined safe surrounding the current spot
                # array for spots surrounding the current spot that have been deamed safe by the KB
                safeSpots = self.near_safe()
                if len(safeSpots) > 0:
                    # Choose a random spot
                    mySpot = self.randoSpot(safeSpots)
                # If there are no safe spots
                else:
                    # Set the next spot to the spot previous
                    mySpot = self.get_previous_spot()
            else:
                myDanger = self.my_knowledge.locate_danger(xCol, yRow)
                # Array for surrounding spots that have yet to be explored
                unexploredSpots = self.near_unexplored()
                # If the current spot is not a warning, we want to explore the board
                # if there are spots surrounding that have not been explored
                if len(unexploredSpots) > 0:
                    # Randomly choose one to explore
                    mySpot = self.randoSpot(unexploredSpots)
                else:
                    # Array for spots surrounding the current spot that have been deamed safe by the KB
                    safeSpots = self.near_safe()
                    if len(safeSpots) > 0:
                        # Randomly choose one from the array
                        mySpot = self.randoSpot(safeSpots)
                    # Otherwise, choose a spot from the random spots array
                    else:
                        mySpot = self.randoSpot(self.surrounding_spots)
        # Set the previous spot as the current
        self.set_previous_spot()
        # Set the current coordinate as the one choosen
        self.set_current_spot(mySpot)
        print("\tHere is what we know and what we don't know in coordinates: ")
        print("\t\tStench: ", stench_array)
        print("\t\tWumpus: ", wumpus)
        print("\t\tBreeze: ", breeze_array)
        print("\t\tPit: ", pit)


    # Updates game cell and knowledge base visited array
    def set_visited(self,game, xcor, ycor):
        game.getGameCell(xcor,ycor).set_visited()
        board_spot= game.getGameCell(xcor, ycor)
        self.my_knowledge.add_visited(board_spot)


    # Finds the gold status
    def goldStatus(self):
        return self.my_knowledge.get_goldFound()


    # Prints the board
    def print_board(self, outFile, game,num):
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
        # Get the coordinates of the current spot
        spot = self.get_current_spot()
        xCol = spot[0]
        yRow = spot[1]
        x = 0
        while x < board_dimension:
            y = 0
            while y < board_dimension:
                #in each game cell
                board_spot = game.getGameCell(x, y)
                if (board_spot.get_visited()):
                    if (xCol==x) and  (yRow==y): # if it is the current position, highlight on screen
                        pygame.draw.rect(screen, "yellow", (x*100, y*100, 100, 100), 0)
                        pygame.draw.rect(screen, "black", (x*100, y*100, 100, 100), 1)
                        cell=pygame.Surface((x*100,y*100))
                        # Print obstacles, if any in cell
                        if (board_spot.get_stench()):
                            screen.blit(stench,(x*100+5,y*100+10))
                        
                        if (board_spot.get_wumpus()):
                            screen.blit(wumpus,(x*100+5,y*100+10))
                        
                        if (board_spot.get_pit()):
                            screen.blit(pit,(x*100+5,y*100+10))  
                        
                        if (board_spot.get_gold()):
                            screen.blit(gold,(x*100+12,y*100+15))
                        
                        if (board_spot.get_breeze()):
                            screen.blit(breeze,(x*100+5,y*100+10))
                    # Shade visited squares on screen
                    else:
                        pygame.draw.rect(screen, "grey", (x*100, y*100, 100, 100), 0)
                        pygame.draw.rect(screen, "black", (x*100, y*100, 100, 100), 1)
                        cell=pygame.Surface((x*100,y*100))
                        # Print obstacles, if any in cell
                        if (board_spot.get_stench()):
                            screen.blit(stench,(x*100+5,y*100+10))
                        
                        if (board_spot.get_wumpus()):
                            screen.blit(wumpus,(x*100+5,y*100+10))
                        
                        if (board_spot.get_pit()):
                            screen.blit(pit,(x*100+5,y*100+10))  
                        
                        if (board_spot.get_gold()):
                            screen.blit(gold,(x*100+12,y*100+15))
                        
                        if (board_spot.get_breeze()):
                            screen.blit(breeze,(x*100+5,y*100+10)) 
                
                else:
                    pygame.draw.rect(screen, "white", (x*100, y*100, 100, 100), 0)
                    pygame.draw.rect(screen, "black", (x*100, y*100, 100, 100), 1)
                    cell=pygame.Surface((x*100,y*100))
                              
                y+=1
            x += 1
   
        # Add page on output file
        outFile.add_page()
        # Save current  screen as image
        imgName= "CurrentPos"+str(num)+".png"
        pygame.image.save(screen, imgName)
        outFile.image(imgName)

