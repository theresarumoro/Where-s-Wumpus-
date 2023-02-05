'''
Caroline Canfield, Theresa Rumoro, Emily Walden
Where's Wumpus?

Main connects all the classes and lets the agent play the game.
'''


# Import libraries and classes
import numpy as np
from GameBoard import GameBoard
from Agent import Agent
from fpdf import FPDF
from Knowledge import Knowledge


if __name__ == '__main__':
    # Get the board ready to play
    game = GameBoard()
    game.initialize()
    game.place_wumpus()
    game.place_pit()
    game.set_gold()

    # Create output file where we will send cheat sheet and game progress information 
    outFile = FPDF(orientation = "L")
    outFile.set_font('helvetica', size=12)
    
    #print game board cheat sheet on first page of playwumpus pdf file
    game.print_board(outFile)
    
    # Call Agent class
    agent= Agent()
    # Initial spot, upper left corner
    agent.set_current_spot([0,0])
    # Set starting position as visited
    agent.set_visited(game,0,0)
    moveNum = 1
    # Game while loop
    while (not(agent.goldStatus())):
        agent.explore(game, outFile, moveNum)
        moveNum+=1

    outFile.output("PlayWumpus.pdf")

