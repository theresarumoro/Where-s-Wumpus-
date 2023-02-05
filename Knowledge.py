'''
Caroline Canfield, Theresa Rumoro, Emily Walden
Where's Wumpus?

Knowledge uses the information that the agent gets to try to find the Wumpus, pit, and safe spots.
'''


# Import other classes
from GameCell import GameCell
from GameBoard import GameBoard


# Set global variables
board_dimension = 4
knowledge_board = []
safe_array = []
stench_array = []
breeze_array = [] 
visited_array = []
warning_array = []
wumpus = []
pit = []
game = GameCell()


class Knowledge:


    # Constructor for knowledge
    def __init__(self):
        self.knowledge_board = []
        self.goldFound = False


    # Creates a list of coordinates of the game board
    def create_coordinates(self):
        # Set variable x equal to zero
        x = 0
        # While x is less than the board dimensions
        while x < board_dimension:
            # Set variable y equal to zero
            y = 0
            # While y is less than the board dimensions
            while y < board_dimension:
                # Append the x, y pair to knowledge_board
                knowledge_board.append([x,y])
                # Increment y
                y += 1
            # Increment x
            x += 1


    # Finds the index of a coordinate in the knowledge board
    def find_index(self, col, row):
        # Create a list variable for the coordinate
        my_spot = [col, row]
        # Find the index and set it equal to the index variable
        index = knowledge_board.index(my_spot)
        return index


    # If the agent finds the stench, it will be added to the array for the potential
    # declaration of the location of the Wumpus
    def update_stench_danger(self, col, row):
        # If the stench_array is empty, append the coordinate to the array and return
        if len(stench_array) == 0:
            stench_array.append([col, row])
        # Else, the stench_array is not empty
        else:
            # If the coordinate is not in the stench_array, append the coordinate to the array and return
            if [col, row] not in stench_array:
                stench_array.append([col, row])


    # If the agent finds the breeze, it will be added to the array for the potential
    # declaration of the location of the pit
    def update_breeze_danger(self, col, row):
        # If the breeze_array is empty, append the coordinate to the array and return
        if len(breeze_array) == 0:
            breeze_array.append([col, row])
        # Else, the breeze_array is not empty
        else:
            # If the coordinate is not in the breeze_array, append the coordinate to the array and return
            if [col, row] not in breeze_array:
                breeze_array.append([col, row])


    # Checks to see if the spot is safe to move. If a stench or a breeze is present, the 
    # agent can still move there.
    def is_safe(self, col, row):
        # If the coordinate is in the safe_array, return True
        if [col, row] in safe_array:
            return True
        # If the coordinate is not in the safe_array, return False
        else:
            return False


    # Determines what direction the next spot is for printing purposes
    def direction(self, my_spot, new_spot):
        # Assign variables to string values
        left = "left"
        right = "right"
        top = "top"
        bottom = "bottom"
        # If the new spot is to the left, return left
        if (new_spot[0]+1 == my_spot[0]):
            return left
        # Else if the new spot is to the right, return right
        elif (new_spot[0]-1 == my_spot[0]):
            return right
        # Else if the new spot is to the bottom, return bottom
        elif (new_spot[1]+1 == my_spot[0]):
            return bottom
        # Else if the new spot is to the top, return top
        elif (new_spot[1]-1 == my_spot[0]):
            return top


    # Returns array of the surrounding coordinates of the agent's position
    def surrounding_spots(self, col, row):
        # Assign variables to empty arrays
        top = []
        bottom = []
        left = []
        right = []
        spots = []
        # Find the surrounding coordinates
        if (row + 1 < board_dimension):
            top.append(col)
            top.append(row + 1)
            spots.append(top)
        if (row - 1 > -1):
            bottom.append(col)
            bottom.append(row - 1)
            spots.append(bottom)
        if (col - 1 > - 1):
            left.append(col - 1)
            left.append(row)
            spots.append(left)
        if (col + 1 < board_dimension):
            right.append(col + 1)
            right.append(row)
            spots.append(right)
        return spots


    # If a spot is declared safe, it will be added to the safe_array.
    def update_safe_array(self, col, row):
        # Call global variable
        global safe_array
        global wumpus
        global pit
        # Create variable
        my_spot = [col, row]
        # If boths pits and the Wumpus is found, the rest of the board is safe
        if ((len(wumpus) == 1) and (len(pit) == 1)):
            # Iterate through knowledge_board
            for item in knowledge_board:
                # If the spot is not the Wumpus or pit locations, append the coordinate to safe_array
                if ((item not in wumpus) and (item not in pit)):
                    safe_array.append(item)
        # If there is a Wumpus spotted, call surrounding_coordinates
        elif (len(wumpus) != 0):
            self.surrounding_coordinates(wumpus[0])
        # If there is a pit spotted, call surrounding_coordinates
        elif (len(pit) != 0):
            self.surrounding_coordinates(pit[0])
        # If the Wumpus or pit is not on the spot, the spot is safe
        elif ((wumpus[0] != my_spot) and (pit[0] != my_spot)):
            # Append the safe coordinate to safe_array
            safe_array.append(my_spot)
        # Else if the Wumpus is located, call surrounding_coordinates
        elif (wumpus[0] != None):
            wumpus.append(wumpus)
            self.surrounding_coordinates(wumpus)
        # Else if the pit is located, call surrounding_coordinates
        elif (pit != None):
            pit.append(pit)
            self.surrounding_coordinates(pit)
        temp_safe_array = safe_array.copy()
        # Iterate through temporary_safe_array
        for item in temp_safe_array:
            # If the item is not in safe_array, append the value to safe_array
            if (item not in safe_array):
                safe_array.append(item)


    # Given a coordinate, the surrounding coordinates will be found with this function
    def surrounding_coordinates(self, my_spot):
        # Call global variable
        global safe_array
        # Set variable
        temporary_safe_array = []
        # Set x and y to the col and row variables
        x = my_spot[0]
        y = my_spot[1]
        # If the coordinate is the top left corner
        if ((x == 0) and (y == board_dimension-1)):
            # Append the surrounding coordinates to temporary_safe_array
            temporary_safe_array.append([1, board_dimension-1])
            temporary_safe_array.append([0, board_dimension-2])
        # Else if the coordinate is the top right corner
        elif ((x == board_dimension-1) and (y == board_dimension-1)):
            # Append the surrounding coordinates to temporary_safe_array
            temporary_safe_array.append([board_dimension-2, board_dimension-1])
            temporary_safe_array.append([board_dimension-1, board_dimension-2])
        # Else if the coordinate is the lower right corner
        elif ((x == board_dimension-1) and (y == 0)):
            # Append the surrounding coordinates to temporary_safe_array
            temporary_safe_array.append([board_dimension-1, 1])
            temporary_safe_array.append([board_dimension-2, 0])
        # Else if the coordinate is on the left side
        elif (x == 0):
            # Append the surrounding coordinates to temporary_safe_array
            temporary_safe_array.append([0, y+1])
            temporary_safe_array.append([0, y-1])
            temporary_safe_array.append([1, y])
        # Else if the coordinate is on the top
        elif (y == board_dimension-1):
            # Append the surrounding coordinates to temporary_safe_array
            temporary_safe_array.append([x-1, board_dimension-1])
            temporary_safe_array.append([x+1, board_dimension-1])
            temporary_safe_array.append([x, board_dimension-2])
        # Else if the coordinate is on the right side
        elif (x == board_dimension-1):
            # Append the surrounding coordinates to temporary_safe_array
            temporary_safe_array.append([board_dimension-1, y+1])
            temporary_safe_array.append([board_dimension-1, y-1])
            temporary_safe_array.append([board_dimension-2, y])
        # Else if the coordinate is on the bottom
        elif (y == 0):
            # Append the surrounding coordinates to temporary_safe_array
            temporary_safe_array.append([x-1, 0])
            temporary_safe_array.append([x+1, 0])
            temporary_safe_array.append([x, 1])
        # Else if the coordinate is in the middle of the board
        elif ((x <= board_dimension-2) and (y <= board_dimension-2)):
            # Append the surrounding coordinates to temporary_safe_array
            temporary_safe_array.append([x+1, y])
            temporary_safe_array.append([x, y+1])
            temporary_safe_array.append([x-1, y])
            temporary_safe_array.append([x, y-1])
        # If safe_array is empty
        if (len(safe_array) == 0):
            # Iterate through temporary_safe_array and append the values to safe_array
            for i in temporary_safe_array:
                safe_array.append(i)
        # Else the safe_array is not empty
        else:
            # Iterate through temporary_safe_array
            for item in temporary_safe_array:
                # If the item is not in safe_array, append the value to safe_array
                if (item not in safe_array):
                    safe_array.append(item)
        

    # If there is a stench or breeze along two sides of the agent, the danger can be located
    # in the diagonal location
    def danger_located_diagonal(self, col, row):
        # Create variables
        wumpus_located = "wumpus"
        pit_located = "pit"
        # Call global variables
        global safe_array
        global stench_array
        global breeze_array
        global wumpus
        global pit
        # Variable my_spot for the coordinates
        my_spot = [col, row]
        # Variables to hold the x and y values of the coordinates
        x = my_spot[0]
        y = my_spot[1]
        # If the Wumpus has not been found yet and there is enough information to declare the location
        if (len(wumpus) == 0) and (len(stench_array) >= 2):
            # Iterate through the stench_array
            for item in stench_array:
                # Create a temporary stench array from the stench_array
                temp_stench_array = stench_array.copy()
                # If the spot to the right of the agent has a stench
                if ((item[0] == x+1) and (item[1] == y)):
                    # Remove that value from the temporary stench array
                    temp_stench_array.remove(item)
                    # Iterate through the temporary stench array
                    for item_two in temp_stench_array:
                        # If the spot above the agent has a stench
                        if ((item_two[0] == x) and (item_two[1] == y+1)):
                            # The Wumpus is found in the upper right diagonal, so add coordinate to Wumpus and return that the Wumpus was found
                            wumpus.append([(my_spot[0]+1), (my_spot[1]+1)])
                            self.update_safe_array((my_spot[0]+1), (my_spot[1]+1))
                            return wumpus_located
                        # Else if the spot below the agent has a stench
                        elif ((item_two[0] == x) and (item_two[1] == y-1)):
                            # The Wumpus is found in the lower right diagonal, so add coordinate to Wumpus and return that the Wumpus was found
                            wumpus.append([(my_spot[0]+1), (my_spot[1]-1)])
                            self.update_safe_array((my_spot[0]+1), (my_spot[1]-1))
                            return wumpus_located
                # Else if the spot to the left of the agent has a stench
                elif ((item[0] == x-1) and (item[1] == y)):
                    # Remove that value from the temporary stench array
                    temp_stench_array.remove(item)
                    # Iterate through the temporary stench array
                    for item_two in temp_stench_array:
                        # If the spot above the agent has a stench
                        if ((item_two[0] == x) and (item_two[1] == y+1)):
                            # The Wumpus is found in the upper left diagonal, so add coordinate to Wumpus and return that the Wumpus was found
                            wumpus.append([(my_spot[0]-1), (my_spot[1]+1)])
                            self.update_safe_array((my_spot[0]-1), (my_spot[1]+1))
                            return wumpus_located
                        # Else if the spot below the agent has a stench
                        elif ((item_two[0] == x) and (item_two[1] == y-1)):
                            # The Wumpus is found in the lower left diagonal, so add coordinate to Wumpus and return that the Wumpus was found
                            wumpus.append([(my_spot[0]-1), (my_spot[1]-1)])
                            self.update_safe_array((my_spot[0]-1), (my_spot[1]-1))
                            return wumpus_located
        # If the pit has not been found yet and there is enough information to declare the location
        elif (len(pit) == 0) and (len(breeze_array) >= 2):
            # Iterate through the breeze_array
            for item in breeze_array:
                # Create a temporary breeze array from the breeze_array
                temp_breeze_array = breeze_array.copy()
                # If the spot to the right of the agent has a breeze
                if ((item[0] == x+1) and (item[1] == y)):
                    # Remove that value from the temporary breeze array
                    temp_breeze_array.remove(item)
                    # Iterate through the temporary breeze array
                    for item_two in temp_breeze_array:
                        # If the spot above the agent has a breeze
                        if ((item_two[0] == x) and (item_two[1] == y+1)):
                            # The pit is found in the upper right diagonal, so add coordinate to pit and return that the pit was found
                            pit.append([(my_spot[0]+1), (my_spot[1]+1)])
                            self.update_safe_array((my_spot[0]+1), (my_spot[1]+1))
                            return pit_located
                        # Else if the spot below the agent has a breeze
                        elif ((item_two[0] == x) and (item_two[1] == y-1)):
                            # The pit is found in the lower right diagonal, so add coordinate to pit and return that the pit was found
                            pit.append([(my_spot[0]+1), (my_spot[1]-1)])
                            self.update_safe_array((my_spot[0]+1), (my_spot[1]-1))
                            return pit_located
                # Else if the spot to the left of the agent has a breeze
                elif ((item[0] == x-1) and (item[1] == y)):
                    # Remove that value from the temporary breeze array
                    temp_breeze_array.remove(item)
                    # Iterate through the temporary breeze array
                    for item_two in temp_breeze_array:
                        # If the spot above the agent has a breeze
                        if ((item_two[0] == x) and (item_two[1] == y+1)):
                            # The pit is found in the upper left diagonal, so add coordinate to pit and return that the pit was found
                            pit.append([(my_spot[0]-1), (my_spot[1]+1)])
                            self.update_safe_array((my_spot[0]-1), (my_spot[1]+1))
                            return pit_located
                        # Else if the spot below the agent has a breeze
                        elif ((item_two[0] == x) and (item_two[1] == y-1)):
                            # The pit is found in the lower left diagonal, so add coordinate to pit and return that the pit was found
                            pit.append([(my_spot[0]-1), (my_spot[1]-1)])
                            self.update_safe_array((my_spot[0]-1), (my_spot[1]-1))
                            return pit_located


    # Using the stench locations, this function will determine if the Wumpus can be located by
    # looking at which coordinates have the stench.
    def wumpus_located(self, col, row):
        # Call global variables
        global wumpus
        global safe_array
        # Variable my_spot for the coordinates
        my_spot = [col, row]
        # Variables to hold the x and y values of the coordinates
        x = my_spot[0]
        y = my_spot[1]
        # Iterate through the stench_array
        for item in stench_array:
            # If the upper right of the original coordinate has a stench
            if ((item[0] == x+1) and (item[1] == y+1)):
                # Iterate through the stench_array
                for item in stench_array:
                    # If the box two higher of the original coordinate has a stench
                    if ((item[0] == x) and (item[1] == y+2)):
                        # Set and return the coordinates of the middle coordinate to the variable
                        wumpus_located = [x, y+1]
                        # Find surrounding coordinates that will be safe
                        self.surrounding_coordinates(wumpus_located)
                        return wumpus_located
                    # Else if the upper left of the original coordinate has a stench
                    elif ((item[0] == x-1) and (item[1] == y+1)):
                        # Set and return the coordinates of the middle coordinate to the variable
                        wumpus_located = [x, y+1]
                        # Find surrounding coordinates that will be safe
                        self.surrounding_coordinates(wumpus_located)
                        return wumpus_located
                    # Else if the lower right diagonal of the previous checkpoint has a stench
                    elif ((item[0] == x+2) and (item[1] == y)):
                        # Set and return the coordinates of the middle coordinate to the variable
                        wumpus_located = [x+1, y]
                        # Find surrounding coordinates that will be safe
                        self.surrounding_coordinates(wumpus_located)
                        return wumpus_located
                    # Else if lower right diagonal of the previous checkpoint has a stench
                    elif ((item[0] == x+1) and (item[1] == y-1)):
                        # Set and return the coordinates of the middle coordinate to the variable
                        wumpus_located = [x+1, y]
                        # Find surrounding coordinates that will be safe
                        self.surrounding_coordinates(wumpus_located)
                        return wumpus_located
            # Else if the upper left of the original coordinate has a stench
            elif ((item[0] == x-1) and (item[1] == y+1)):
                # Iterate through the stench_array
                for item in stench_array:
                    # If the box two higher of the original coordinate has a stench
                    if ((item[0] == x) and (item[1] == y+2)):
                        # Set and return the coordinates of the middle coordinate to the variable
                        wumpus_located = [x, y+1]
                        # Find surrounding coordinates that will be safe
                        self.surrounding_coordinates(wumpus_located)
                        return wumpus_located
                    # Else if the upper right diagonal of the original coordinate has a stench
                    elif ((item[0] == x+1) and (item[1] == y+1)):
                        # Set and return the coordinates of the middle coordinate to the variable
                        wumpus_located = [x, y+1]
                        # Find surrounding coordinates that will be safe
                        self.surrounding_coordinates(wumpus_located)
                        return wumpus_located
                    # Else if the lower right diagonal of the previous checkpoint has a stench
                    elif ((item[0] == x-2) and (item[1] == y)):
                        # Set and return the coordinates of the middle coordinate to the variable
                        wumpus_located = [x-1, y]
                        # Find surrounding coordinates that will be safe
                        self.surrounding_coordinates(wumpus_located)
                        return wumpus_located
                    # Else if the lower left diagonal of the original coordinate has a stench
                    elif ((item[0] == x-1) and (item[1] == y-1)):
                        # Set and return the coordinates of the middle coordinate to the variable
                        wumpus_located = [x-1, y]
                        # Find surrounding coordinates that will be safe
                        self.surrounding_coordinates(wumpus_located)
                        return wumpus_located
            # Else if the lower left diagonal of the original coordinate has a stench
            elif ((item[0] == x-1) and (item[1] == y-1)):
                # Iterate through the stench_array
                for item in stench_array:
                    # If the box two lower than the previous checkpoint has a stench
                    if ((item[0] == x) and (item[1] == y-2)):
                        # Set and return the coordinates of the middle coordinate to the variable
                        wumpus_located = [x, y-1]
                        # Find surrounding coordinates that will be safe
                        self.surrounding_coordinates(wumpus_located)
                        return wumpus_located
                    # Else if the lower right diagonal of the original coordinate has a stench
                    elif ((item[0] == x+1) and (item[1] == y-1)):
                        # Set and return the coordinates of the middle coordinate to the variable
                        wumpus_located = [x, y-1]
                        # Find surrounding coordinates that will be safe
                        self.surrounding_coordinates(wumpus_located)
                        return wumpus_located
                    # Else if the box two left than the previous checkpoint has a stench
                    elif ((item[0] == x-2) and (item[1] == y)):
                        # Set and return the coordinates of the middle coordinate to the variable
                        wumpus_located = [x-1, y]
                        # Find surrounding coordinates that will be safe
                        self.surrounding_coordinates(wumpus_located)
                        return wumpus_located
                    # Else if the upper left diagonal of the original coordinate has a stench
                    elif ((item[0] == x-1) and (item[1] == y+1)):
                        # Set and return the coordinates of the middle coordinate to the variable
                        wumpus_located = [x-1, y]
                        # Find surrounding coordinates that will be safe
                        self.surrounding_coordinates(wumpus_located)
                        return wumpus_located
            # Else if the lower right diagonal of the original coordinate has a stench
            elif ((item[0] == x+1) and (item[1] == y-1)):
                # Iterate through the stench_array
                for item in stench_array:
                    # If the box two lower than the original coordinate has a stench
                    if ((item[0] == x) and (item[1] == y-2)):
                        # Set and return the coordinates of the middle coordinate to the variable
                        wumpus_located = [x, y-1]
                        # Find surrounding coordinates that will be safe
                        self.surrounding_coordinates(wumpus_located)
                        return wumpus_located
                    # Else if the lower left diagonal of the original coordinate has a stench
                    elif ((item[0] == x-1) and (item[1] == y-1)):
                        # Set and return the coordinates of the middle coordinate to the variable
                        wumpus_located = [x, y-1]
                        # Find surrounding coordinates that will be safe
                        self.surrounding_coordinates(wumpus_located)
                        return wumpus_located
                    # Else if the box two right than the original coordinate has a stench
                    elif ((item[0] == x+2) and (item[1] == y)):
                        # Set and return the coordinates of the middle coordinate to the variable
                        wumpus_located = [x+1, y]
                        # Find surrounding coordinates that will be safe
                        self.surrounding_coordinates(wumpus_located)
                        return wumpus_located
                    # Else if the upper right of the original coordinate has a stench
                    elif ((item[0] == x+1) and (item[1] == y+1)):
                        # Set and return the coordinates of the middle coordinate to the variable
                        wumpus_located = [x+1, y]
                        # Find surrounding coordinates that will be safe
                        self.surrounding_coordinates(wumpus_located)
                        return wumpus_located
            # Else if there is a stench on the left side
            elif (item[0] == 0):
                # Iterate from 0 to board_dimension
                for i in range(board_dimension):
                    # If there is a coordinate on the left side
                    if ((item[0] == 0) and item[1] == i):
                        # Create a temporary stench array with the stench array contents
                        temporary_stench_array = stench_array.copy()
                        # Remove the previous value from the temporaty stench array
                        temporary_stench_array.remove([0, i])
                        # Iterate through the temporary stench array
                        for item in temporary_stench_array:
                            # Iterate from 0 to board_dimension
                            for i in range(board_dimension):
                                # If there is a stench two below the previous coordinate
                                if ((item[0] == 0) and (item[1] == i-2)):
                                    # Set and return the coordinates of the middle coordinate to the variable
                                    wumpus_located = [0, i-1]
                                    # Find surrounding coordinates that will be safe
                                    self.surrounding_coordinates(wumpus_located)
                                    return wumpus_located
                                # If there is a stench two above the previous coordinate
                                elif ((item[0] == 0) and (item[1] == i+2)):
                                    # Set and return the coordinates of the middle coordinate to the variable
                                    wumpus_located = [0, i+1]
                                    # Find surrounding coordinates that will be safe
                                    self.surrounding_coordinates(wumpus_located)
                                    return wumpus_located
            # Else if there is a stench on the right side
            elif (item[0] == board_dimension-1):
                # Iterate from 0 to board_dimension
                for i in range(board_dimension):
                    # If there is a coordinate on the right side
                    if ((item[0] == board_dimension-1) and item[1] == i):
                        # Create a temporary stench array with the stench array contents
                        temporary_stench_array = stench_array.copy()
                        # Remove the previous value from the temporaty stench array
                        temporary_stench_array.remove([board_dimension-1, i])
                        # Iterate through the temporary stench array
                        for item in temporary_stench_array:
                            # Iterate from 0 to board_dimension
                            for i in range(board_dimension):
                                # If there is a stench two below the previous coordinate
                                if ((item[0] == board_dimension-1) and (item[1] == i-2)):
                                    # Set and return the coordinates of the middle coordinate to the variable
                                    wumpus_located = [board_dimension-1, i-1]
                                    # Find surrounding coordinates that will be safe
                                    self.surrounding_coordinates(wumpus_located)
                                    return wumpus_located
                                # If there is a stench two above the previous coordinate
                                elif ((item[0] == 0) and (item[1] == i+2)):
                                    # Set and return the coordinates of the middle coordinate to the variable
                                    wumpus_located = [board_dimension-1, i+1]
                                    # Find surrounding coordinates that will be safe
                                    self.surrounding_coordinates(wumpus_located)
                                    return wumpus_located
            # Else if there is a stench on the top
            elif (item[1] == board_dimension-1):
                # Iterate from 0 to board_dimension
                for i in range(board_dimension):
                    # If there is a coordinate on the left side
                    if ((item[0] == i) and (item[1] == board_dimension-1)):
                        # Create a temporary stench array with the stench array contents
                        temporary_stench_array = stench_array.copy()
                        # Remove the previous value from the temporaty stench array
                        temporary_stench_array.remove([i, board_dimension-1])
                        # Iterate through the temporary stench array
                        for item in temporary_stench_array:
                            # Iterate from 0 to board_dimension
                            for i in range(board_dimension):
                                # If there is a stench two below the previous coordinate
                                if ((item[0] == i-2) and (item[1] == board_dimension-1)):
                                    # Set and return the coordinates of the middle coordinate to the variable
                                    wumpus_located = [i-1, board_dimension-1]
                                    # Find surrounding coordinates that will be safe
                                    self.surrounding_coordinates(wumpus_located)
                                    return wumpus_located
                                # If there is a stench two above the previous coordinate
                                elif ((item[0] == i+2) and (item[1] == board_dimension-1)):
                                    # Set and return the coordinates of the middle coordinate to the variable
                                    wumpus_located = [i+1, board_dimension-1]
                                    # Find surrounding coordinates that will be safe
                                    self.surrounding_coordinates(wumpus_located)
                                    return wumpus_located
            # Else if there is a stench on the bottom
            elif (item[1] == 0):
                # Iterate from 0 to board_dimension
                for i in range(board_dimension):
                    # If there is a coordinate on the bottom
                    if ((item[0] == i) and (item[1] == 0)):
                        # Create a temporary stench array with the stench array contents
                        temporary_stench_array = stench_array.copy()
                        # Remove the previous value from the temporaty stench array
                        temporary_stench_array.remove([i, 0])
                        # Iterate through the temporary stench array
                        for item in temporary_stench_array:
                            # Iterate from 0 to board_dimension
                            for i in range(board_dimension):
                                # If there is a stench two below the previous coordinate
                                if ((item[0] == i-2) and (item[1] == 0)):
                                    # Set and return the coordinates of the middle coordinate to the variable
                                    wumpus_located = [i-1, 0]
                                    # Find surrounding coordinates that will be safe
                                    self.surrounding_coordinates(wumpus_located)
                                    return wumpus_located
                                # If there is a stench two above the previous coordinate
                                elif ((item[0] == i+2) and (item[1] == 0)):
                                    # Set and return the coordinates of the middle coordinate to the variable
                                    wumpus_located = [i+1, 0]
                                    # Find surrounding coordinates that will be safe
                                    self.surrounding_coordinates(wumpus_located)
                                    return wumpus_located
            # If the spot below of the upper left or upper right corner has a stench
            if (((item[0] == 0) and (item[1] == board_dimension-2)) or ((item[0] == board_dimension-1) and (item[1]) == board_dimension-2)):
                # Iterate through the stench_array
                for item in stench_array:
                    # If the spot to the right of the upper left corner has a stench
                    if ((item[0] == 1) and (item[1] == board_dimension-1)):
                        # Set and return the coordinates of the upper left corner coordinate to the variable
                        wumpus_located = [0, board_dimension-1]
                        # Find surrounding coordinates that will be safe
                        self.surrounding_coordinates(wumpus_located)
                        return wumpus_located
                    # Else if the spot to the left of the upper right corner has a stench
                    elif ((item[0] == board_dimension-2) and (item[1] == board_dimension-1)):
                        # Set and return the coordinates of the upper right corner coordinate to the variable
                        wumpus_located = [board_dimension-1, board_dimension-1]
                        # Find surrounding coordinates that will be safe
                        self.surrounding_coordinates(wumpus_located)
                        return wumpus_located
            # Else if the spot to the right of the upper left corner or the spot to the left of the upper right corner has a stench
            elif (((item[0] == 1) and (item[1] == board_dimension-1)) or ((item[0] == board_dimension-2) and (item[1]) == board_dimension-1)):
                # Iterate through the stench_array
                for item in stench_array:
                    # If the spot below the upper left corner has a stench
                    if ((item[0] == 0) and (item[1] == board_dimension-2)):
                        # Set and return the coordinates of the upper left corner coordinate to the variable
                        wumpus_located = [0, board_dimension-1]
                        # Find surrounding coordinates that will be safe
                        self.surrounding_coordinates(wumpus_located)
                        return wumpus_located
                    # Else if the spot below the upper right corner has a stench
                    elif ((item[0] == board_dimension-1) and (item[1] == board_dimension-2)):
                        # Set and return the coordinates of the upper right corner coordinate to the variable
                        wumpus_located = [board_dimension-1, board_dimension-1]
                        # Find surrounding coordinates that will be safe
                        self.surrounding_coordinates(wumpus_located)
                        return wumpus_located
            # Else if the spot to the left of the lower right corner has a stench
            elif ((item[0] == board_dimension-2) and (item[1] == 0)):
                # Iterate through the stench_array
                for item in stench_array:                
                # If the spot above the lower right corner has a stench
                    if ((item[0] == board_dimension-1) and (item[1] == 1)):
                        # Set and return the coordinates of the lower right corner coordinate to the variable
                        wumpus_located = [board_dimension-1, 0]
                        # Find surrounding coordinates that will be safe
                        self.surrounding_coordinates(wumpus_located)
                        return wumpus_located
            # Else if the spot above the lower right corner has a stench
            elif ((item [0] == board_dimension-1) and (item[1] == 1)):
                # Iterate through the stench_array
                for item in stench_array:
                    # If the spot to the left of the lower right corner has a stench
                    if ((item[0] == board_dimension-2) and (item[1] == 0)):
                        # Set and return the coordinates of the lower right corner coordinate to the variable
                        wumpus_located = [board_dimension-1, 0]
                        # Find surrounding coordinates that will be safe
                        self.surrounding_coordinates(wumpus_located)
                        return wumpus_located
            # Else if the lower right corner has a stench
            elif ((item[0] == board_dimension-1) and (item[1] == 0)):
                # Iterate through the stench_array
                for item in stench_array:
                    # If the upper left corner coordinate has a stench
                    if ((item[0] == x-1) and (item[1] == y+1)):
                        # Iterate through the safe_array
                        for safe_item in safe_array:
                            # If the spot to the right of the original coordinate is safe
                            if ((safe_item[0] == x-1) and (safe_item[1] == 0)):
                                # Set and return the coordinates of the coordinates above the original coordinate to the variable
                                wumpus_located = [x, y+1]
                                # Find surrounding coordinates that will be safe
                                self.surrounding_coordinates(wumpus_located)
                                return wumpus_located
                            # If the spot above the original coordinate is safe
                            elif ((safe_item[0] == x) and (safe_item[1] == y+1)):
                                # Set and return the coordinates of the coordinates to the left of the original coordinate to the variable
                                wumpus_located = [x-1, y]
                                # Find surrounding coordinates that will be safe
                                self.surrounding_coordinates(wumpus_located)
                                return wumpus_located
            # Else if the upper right corner has a stench
            elif ((item[0] == board_dimension-1) and (item[1] == board_dimension-1)):
                # Iterate through the stench_array
                for item in stench_array:
                    # If the lower left corner coordinate has a stench
                    if ((item[0] == x-1) and (item[1] == y-1)):
                        # Iterate through the safe_array
                        for safe_item in safe_array:
                            # If the spot to the left of the original coordinate is safe
                            if ((safe_item[0] == x-1) and (safe_item[1] == y)):
                                # Set and return the coordinates of the coordinates below the original coordinate to the variable
                                wumpus_located = [x, y-1]
                                # Find surrounding coordinates that will be safe
                                self.surrounding_coordinates(wumpus_located)
                                return wumpus_located
                            # If the spot below the original coordinate is safe
                            elif ((safe_item[0] == x) and (safe_item[1] == y-1)):
                                # Set and return the coordinates of the coordinates to the left of the original coordinate to the variable
                                wumpus_located = [x-1, y]
                                # Find surrounding coordinates that will be safe
                                self.surrounding_coordinates(wumpus_located)
                                return wumpus_located
            # Else if the upper left corner has a stench
            elif ((item[0] == board_dimension-1) and (item[1] == board_dimension-1)):
                # Iterate through the stench_array
                for item in stench_array:
                    # If the lower right corner coordinate has a stench
                    if ((item[0] == x+1) and (item[1] == y-1)):
                        # Iterate through the safe_array
                        for safe_item in safe_array:
                            # If the spot to the right of the original coordinate is safe
                            if ((safe_item[0] == x+1) and (safe_item[1] == y)):
                                # Set and return the coordinates of the coordinates below the original coordinate to the variable
                                wumpus_located = [x, y-1]
                                # Find surrounding coordinates that will be safe
                                self.surrounding_coordinates(wumpus_located)
                                return wumpus_located
                            # If the spot below the original coordinate is safe
                            elif ((safe_item[0] == x) and (safe_item[1] == y-1)):
                                # Set and return the coordinates of the coordinates to the right of the original coordinate to the variable
                                wumpus_located = [x+1, y]
                                # Find surrounding coordinates that will be safe
                                self.surrounding_coordinates(wumpus_located)
                                return wumpus_located

    
    # Using the breeze locations, this function will determine if the pits can be located by
    # looking at which coordinates have the breeze.
    def pit_located(self, col, row):
        # Call global variables
        global pit
        global safe_array
        # Variable my_spot for the coordinates
        my_spot = [col, row]
        # Variables to hold the x and y values of the coordinates
        x = my_spot[0]
        y = my_spot[1]

        # Iterate through the breeze_array
        for item in breeze_array:
            # If the upper right of the original coordinate has a breeze
            if ((item[0] == x+1) and (item[1] == y+1)):
                # Iterate through the breeze_array
                for item in breeze_array:
                    # If the box two higher of the original coordinate has a breeze
                    if ((item[0] == x) and (item[1] == y+2)):
                        # Set and return the coordinates of the middle coordinate to the variable
                        pit_located = [x, y+1]
                        # Find surrounding coordinates that will be safe
                        self.surrounding_coordinates(pit_located)
                        return pit_located
                    # Else if the upper left of the original coordinate has a breeze
                    elif ((item[0] == x-1) and (item[1] == y+1)):
                        # Set and return the coordinates of the middle coordinate to the variable
                        pit_located = [x, y+1]
                        # Find surrounding coordinates that will be safe
                        self.surrounding_coordinates(pit_located)
                        return pit_located
                    # Else if the lower right diagonal of the previous checkpoint has a breeze
                    elif ((item[0] == x+2) and (item[1] == y)):
                        # Set and return the coordinates of the middle coordinate to the variable
                        pit_located = [x+1, y]
                        # Find surrounding coordinates that will be safe
                        self.surrounding_coordinates(pit_located)
                        return pit_located
                    # Else if lower right of the original coordinate has a breeze
                    elif ((item[0] == x+1) and (item[1] == y-1)):
                        # Set and return the coordinates of the middle coordinate to the variable
                        pit_located = [x+1, y]
                        # Find surrounding coordinates that will be safe
                        self.surrounding_coordinates(pit_located)
                        return pit_located
            # Else if the upper left of the original coordinate has a breeze
            elif ((item[0] == x-1) and (item[1] == y+1)):
                # Iterate through the breeze_array
                for item in breeze_array:
                    # If the box two higher of the original coordinate has a breeze
                    if ((item[0] == x) and (item[1] == y+2)):
                        # Set and return the coordinates of the middle coordinate to the variable
                        pit_located = [x, y+1]
                        # Find surrounding coordinates that will be safe
                        self.surrounding_coordinates(pit_located)
                        return pit_located
                    # Else if the upper right diagonal of the original coordinate has a breeze
                    elif ((item[0] == x+1) and (item[1] == y+1)):
                        # Set and return the coordinates of the middle coordinate to the variable
                        pit_located = [x, y+1]
                        # Find surrounding coordinates that will be safe
                        self.surrounding_coordinates(pit_located)
                        return pit_located
                    # Else if the lower right diagonal of the previous checkpoint has a breeze
                    elif ((item[0] == x-2) and (item[1] == y)):
                        # Set and return the coordinates of the middle coordinate to the variable
                        pit_located = [x-1, y]
                        # Find surrounding coordinates that will be safe
                        self.surrounding_coordinates(pit_located)
                        return pit_located
                    # Else if the lower left diagonal of the original coordinate has a breeze
                    elif ((item[0] == x-1) and (item[1] == y-1)):
                        # Set and return the coordinates of the middle coordinate to the variable
                        pit_located = [x-1, y]
                        # Find surrounding coordinates that will be safe
                        self.surrounding_coordinates(pit_located)
                        return pit_located
            # Else if the lower left diagonal of the original coordinate has a breeze
            elif ((item[0] == x-1) and (item[1] == y-1)):
                # Iterate through the breeze_array
                for item in breeze_array:
                    # If the box two lower than the previous checkpoint has a breeze
                    if ((item[0] == x) and (item[1] == y-2)):
                        # Set and return the coordinates of the middle coordinate to the variable
                        pit_located = [x, y-1]
                        # Find surrounding coordinates that will be safe
                        self.surrounding_coordinates(pit_located)
                        return pit_located
                    # Else if the lower right diagonal of the original coordinate has a breeze
                    elif ((item[0] == x+1) and (item[1] == y-1)):
                        # Set and return the coordinates of the middle coordinate to the variable
                        pit_located = [x, y-1]
                        # Find surrounding coordinates that will be safe
                        self.surrounding_coordinates(pit_located)
                        return pit_located
                    # Else if the box two left than the previous checkpoint has a breeze
                    elif ((item[0] == x-2) and (item[1] == y)):
                        # Set and return the coordinates of the middle coordinate to the variable
                        pit_located = [x-1, y]
                        # Find surrounding coordinates that will be safe
                        self.surrounding_coordinates(pit_located)
                        return pit_located
                    # Else if the upper left diagonal of the original coordinate has a breeze
                    elif ((item[0] == x-1) and (item[1] == y+1)):
                        # Set and return the coordinates of the middle coordinate to the variable
                        pit_located = [x-1, y]
                        # Find surrounding coordinates that will be safe
                        self.surrounding_coordinates(pit_located)
                        return pit_located
            # Else if the lower right diagonal of the original coordinate has a breeze
            elif ((item[0] == x+1) and (item[1] == y-1)):
                # Iterate through the breeze_array
                for item in breeze_array:
                    # If the box two lower than the original coordinate has a breeze
                    if ((item[0] == x) and (item[1] == y-2)):
                        # Set and return the coordinates of the middle coordinate to the variable
                        pit_located = [x, y-1]
                        # Find surrounding coordinates that will be safe
                        self.surrounding_coordinates(pit_located)
                        return pit_located
                    # Else if the lower left diagonal of the original coordinate has a breeze
                    elif ((item[0] == x-1) and (item[1] == y-1)):
                        # Set and return the coordinates of the middle coordinate to the variable
                        pit_located = [x, y-1]
                        # Find surrounding coordinates that will be safe
                        self.surrounding_coordinates(pit_located)
                        return pit_located
                    # Else if the box two right than the original coordinate has a breeze
                    elif ((item[0] == x+2) and (item[1] == y)):
                        # Set and return the coordinates of the middle coordinate to the variable
                        pit_located = [x+1, y]
                        # Find surrounding coordinates that will be safe
                        self.surrounding_coordinates(pit_located)
                        return pit_located
                    # Else if the upper right of the original coordinate has a breeze
                    elif ((item[0] == x+1) and (item[1] == y+1)):
                        # Set and return the coordinates of the middle coordinate to the variable
                        pit_located = [x+1, y]
                        # Find surrounding coordinates that will be safe
                        self.surrounding_coordinates(pit_located)
                        return pit_located
            # Else if there is a breeze on the left side
            elif (item[0] == 0):
                # Iterate from 0 to board_dimension
                for i in range(board_dimension):
                    # If there is a coordinate on the left side
                    if ((item[0] == 0) and item[1] == i):
                        # Create a temporary breeze array with the breeze array contents
                        temporary_breeze_array = breeze_array.copy()
                        # Remove the previous value from the temporaty breeze array
                        temporary_breeze_array.remove([0, i])
                        # Iterate through the temporary breeze array
                        for item in temporary_breeze_array:
                            # Iterate from 0 to board_dimension
                            for i in range(board_dimension):
                                # If there is a breeze two below the previous coordinate
                                if ((item[0] == 0) and (item[1] == i-2)):
                                    # Set and return the coordinates of the middle coordinate to the variable
                                    pit_located = [0, i-1]
                                    # Find surrounding coordinates that will be safe
                                    self.surrounding_coordinates(pit_located)
                                    return pit_located
                                # If there is a breeze two above the previous coordinate
                                elif ((item[0] == 0) and (item[1] == i+2)):
                                    # Set and return the coordinates of the middle coordinate to the variable
                                    pit_located = [0, i+1]
                                    # Find surrounding coordinates that will be safe
                                    self.surrounding_coordinates(pit_located)
                                    return pit_located
            # Else if there is a breeze on the right side
            elif (item[0] == board_dimension-1):
                # Iterate from 0 to board_dimension
                for i in range(board_dimension):
                    # If there is a coordinate on the right side
                    if ((item[0] == board_dimension-1) and item[1] == i):
                        # Create a temporary breeze array with the breeze array contents
                        temporary_breeze_array = breeze_array.copy()
                        # Remove the previous value from the temporaty breeze array
                        temporary_breeze_array.remove([board_dimension-1, i])
                        # Iterate through the temporary breeze array
                        for item in temporary_breeze_array:
                            # Iterate from 0 to board_dimension
                            for i in range(board_dimension):
                                # If there is a breeze two below the previous coordinate
                                if ((item[0] == board_dimension-1) and (item[1] == i-2)):
                                    # Set and return the coordinates of the middle coordinate to the variable
                                    pit_located = [board_dimension-1, i-1]
                                    # Find surrounding coordinates that will be safe
                                    self.surrounding_coordinates(pit_located)
                                    return pit_located
                                # If there is a breeze two above the previous coordinate
                                elif ((item[0] == 0) and (item[1] == i+2)):
                                    # Set and return the coordinates of the middle coordinate to the variable
                                    pit_located = [board_dimension-1, i+1]
                                    # Find surrounding coordinates that will be safe
                                    self.surrounding_coordinates(pit_located)
                                    return pit_located
            # Else if there is a breeze on the top
            elif (item[1] == board_dimension-1):
                # Iterate from 0 to board_dimension
                for i in range(board_dimension):
                    # If there is a coordinate on the left side
                    if ((item[0] == i) and (item[1] == board_dimension-1)):
                        # Create a temporary breeze array with the breeze array contents
                        temporary_breeze_array = breeze_array.copy()
                        # Remove the previous value from the temporaty breeze array
                        temporary_breeze_array.remove([i, board_dimension-1])
                        # Iterate through the temporary breeze array
                        for item in temporary_breeze_array:
                            # Iterate from 0 to board_dimension
                            for i in range(board_dimension):
                                # If there is a breeze two below the previous coordinate
                                if ((item[0] == i-2) and (item[1] == board_dimension-1)):
                                    # Set and return the coordinates of the middle coordinate to the variable
                                    pit_located = [i-1, board_dimension-1]
                                    # Find surrounding coordinates that will be safe
                                    self.surrounding_coordinates(pit_located)
                                    return pit_located
                                # If there is a breeze two above the previous coordinate
                                elif ((item[0] == i+2) and (item[1] == board_dimension-1)):
                                    # Set and return the coordinates of the middle coordinate to the variable
                                    pit_located = [i+1, board_dimension-1]
                                    # Find surrounding coordinates that will be safe
                                    self.surrounding_coordinates(pit_located)
                                    return pit_located
            # Else if there is a breeze on the bottom
            elif (item[1] == 0):
                # Iterate from 0 to board_dimension
                for i in range(board_dimension):
                    # If there is a coordinate on the bottom
                    if ((item[0] == i) and (item[1] == 0)):
                        # Create a temporary breeze array with the breeze array contents
                        temporary_breeze_array = breeze_array.copy()
                        # Remove the previous value from the temporaty breeze array
                        temporary_breeze_array.remove([i, 0])
                        # Iterate through the temporary breeze array
                        for item in temporary_breeze_array:
                            # Iterate from 0 to board_dimension
                            for i in range(board_dimension):
                                # If there is a breeze two below the previous coordinate
                                if ((item[0] == i-2) and (item[1] == 0)):
                                    # Set and return the coordinates of the middle coordinate to the variable
                                    pit_located = [i-1, 0]
                                    # Find surrounding coordinates that will be safe
                                    self.surrounding_coordinates(pit_located)
                                    return pit_located
                                # If there is a breeze two above the previous coordinate
                                elif ((item[0] == i+2) and (item[1] == 0)):
                                    # Set and return the coordinates of the middle coordinate to the variable
                                    pit_located = [i+1, 0]
                                    # Find surrounding coordinates that will be safe
                                    self.surrounding_coordinates(pit_located)
                                    return pit_located
            # If the spot below of the upper left or upper right corner has a breeze
            if (((item[0] == 0) and (item[1] == board_dimension-2)) or ((item[0] == board_dimension-1) and (item[1]) == board_dimension-2)):
                # Iterate through the breeze_array
                for item in breeze_array:
                    # If the spot to the right of the upper left corner has a breeze
                    if ((item[0] == 1) and (item[1] == board_dimension-1)):
                        # Set and return the coordinates of the upper left corner coordinate to the variable
                        pit_located = [0, board_dimension-1]
                        # Find surrounding coordinates that will be safe
                        self.surrounding_coordinates(pit_located)
                        return pit_located
                    # Else if the spot to the left of the upper right corner has a breeze
                    elif ((item[0] == board_dimension-2) and (item[1] == board_dimension-1)):
                        # Set and return the coordinates of the upper right corner coordinate to the variable
                        pit_located = [board_dimension-1, board_dimension-1]
                        # Find surrounding coordinates that will be safe
                        self.surrounding_coordinates(pit_located)
                        return pit_located
            # Else if the spot to the right of the upper left corner or the spot to the left of the upper right corner has a breeze
            elif (((item[0] == 1) and (item[1] == board_dimension-1)) or ((item[0] == board_dimension-2) and (item[1]) == board_dimension-1)):
                # Iterate through the breeze_array
                for item in breeze_array:
                    # If the spot below the upper left corner has a breeze
                    if ((item[0] == 0) and (item[1] == board_dimension-2)):
                        # Set and return the coordinates of the upper left corner coordinate to the variable
                        pit_located = [0, board_dimension-1]
                        # Find surrounding coordinates that will be safe
                        self.surrounding_coordinates(pit_located)
                        return pit_located
                    # Else if the spot below the upper right corner has a breeze
                    elif ((item[0] == board_dimension-1) and (item[1] == board_dimension-2)):
                        # Set and return the coordinates of the upper right corner coordinate to the variable
                        pit_located = [board_dimension-1, board_dimension-1]
                        # Find surrounding coordinates that will be safe
                        self.surrounding_coordinates(pit_located)
                        return pit_located
            # Else if the spot to the left of the lower right corner has a breeze
            elif ((item[0] == board_dimension-2) and (item[1] == 0)):
                # Iterate through the breeze_array
                for item in breeze_array:                
                # If the spot above the lower right corner has a breeze
                    if ((item[0] == board_dimension-1) and (item[1] == 1)):
                        # Set and return the coordinates of the lower right corner coordinate to the variable
                        pit_located = [board_dimension-1, 0]
                        # Find surrounding coordinates that will be safe
                        self.surrounding_coordinates(pit_located)
                        return pit_located
            # Else if the spot above the lower right corner has a breeze
            elif ((item [0] == board_dimension-1) and (item[1] == 1)):
                # Iterate through the breeze_array
                for item in breeze_array:
                    # If the spot to the left of the lower right corner has a breeze
                    if ((item[0] == board_dimension-2) and (item[1] == 0)):
                        # Set and return the coordinates of the lower right corner coordinate to the variable
                        pit_located = [board_dimension-1, 0]
                        # Find surrounding coordinates that will be safe
                        self.surrounding_coordinates(pit_located)
                        return pit_located
            # Else if the lower right corner has a breeze
            elif ((item[0] == board_dimension-1) and (item[1] == 0)):
                # Iterate through the breeze_array
                for item in breeze_array:
                    # If the upper left corner coordinate has a breeze
                    if ((item[0] == x-1) and (item[1] == y+1)):
                        # Iterate through the safe_array
                        for safe_item in safe_array:
                            # If the spot to the right of the original coordinate is safe
                            if ((safe_item[0] == x-1) and (safe_item[1] == 0)):
                                # Set and return the coordinates of the coordinates above the original coordinate to the variable
                                pit_located = [x, y+1]
                                # Find surrounding coordinates that will be safe
                                self.surrounding_coordinates(pit_located)
                                return pit_located
                            # If the spot above the original coordinate is safe
                            elif ((safe_item[0] == x) and (safe_item[1] == y+1)):
                                # Set and return the coordinates of the coordinates to the left of the original coordinate to the variable
                                pit_located = [x-1, y]
                                # Find surrounding coordinates that will be safe
                                self.surrounding_coordinates(pit_located)
                                return pit_located
            # Else if the upper right corner has a breeze
            elif ((item[0] == board_dimension-1) and (item[1] == board_dimension-1)):
                # Iterate through the breeze_array
                for item in breeze_array:
                    # If the lower left corner coordinate has a breeze
                    if ((item[0] == x-1) and (item[1] == y-1)):
                        # Iterate through the safe_array
                        for safe_item in safe_array:
                            # If the spot to the left of the original coordinate is safe
                            if ((safe_item[0] == x-1) and (safe_item[1] == y)):
                                # Set and return the coordinates of the coordinates below the original coordinate to the variable
                                pit_located = [x, y-1]
                                # Find surrounding coordinates that will be safe
                                self.surrounding_coordinates(pit_located)
                                return pit_located
                            # If the spot below the original coordinate is safe
                            elif ((safe_item[0] == x) and (safe_item[1] == y-1)):
                                # Set and return the coordinates of the coordinates to the left of the original coordinate to the variable
                                pit_located = [x-1, y]
                                # Find surrounding coordinates that will be safe
                                self.surrounding_coordinates(pit_located)
                                return pit_located
            # Else if the upper left corner has a breeze
            elif ((item[0] == board_dimension-1) and (item[1] == board_dimension-1)):
                # Iterate through the breeze_array
                for item in breeze_array:
                    # If the lower right corner coordinate has a breeze
                    if ((item[0] == x+1) and (item[1] == y-1)):
                        # Iterate through the safe_array
                        for safe_item in safe_array:
                            # If the spot to the right of the original coordinate is safe
                            if ((safe_item[0] == x+1) and (safe_item[1] == y)):
                                # Set and return the coordinates of the coordinates below the original coordinate to the variable
                                pit_located = [x, y-1]
                                # Find surrounding coordinates that will be safe
                                self.surrounding_coordinates(pit_located)
                                return pit_located
                            # If the spot below the original coordinate is safe
                            elif ((safe_item[0] == x) and (safe_item[1] == y-1)):
                                # Set and return the coordinates of the coordinates to the right of the original coordinate to the variable
                                pit_located = [x+1, y]
                                # Find surrounding coordinates that will be safe
                                self.surrounding_coordinates(pit_located)
                                return pit_located


    # Locates the danger if there is enough information
    def locate_danger(self, col, row):
        # Call global variable
        global visited_array
        # Determine if a danger can be determined
        myDanger = self.danger_located_diagonal(col,row)
        # If danger is found, the variable will return a specific string
        if myDanger is not None:
            if (myDanger == 'wumpus'):
                myDanger = wumpus
            elif (myDanger == 'pit'):
                myDanger = pit
            if myDanger not in visited_array:
                # Add to the visited array
                visited_array.append(myDanger)
        return myDanger


    # Add visited spots to visited_array  
    def add_visited(self, spot):
        # Call global variable
        global visited_array
        if spot not in visited_array:
            # Add to the visited array
            visited_array.append(spot)


    # Set gold found
    def set_goldFound(self):
        self.goldFound=True


    # Get gold found
    def get_goldFound(self):
        return self.goldFound

