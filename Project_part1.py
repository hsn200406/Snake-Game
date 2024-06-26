# Group#:
# Student Names:

"""
    This program implements a variety of the snake 
    game (https://en.wikipedia.org/wiki/Snake_(video_game_genre))
"""

import threading
import queue        #the thread-safe queue from Python standard library

from tkinter import Tk, Canvas, Button
import random, time

class Gui():
    """
        This class takes care of the game's graphic user interface (gui)
        creation and termination.
    """
    def __init__(self):
        """        
            The initializer instantiates the main window and 
            creates the starting icons for the snake and the prey,
            and displays the initial gamer score.
        """
        #some GUI constants
        scoreTextXLocation = 60
        scoreTextYLocation = 15
        textColour = "white"
        #instantiate and create gui
        self.root = Tk()
        self.canvas = Canvas(self.root, width = WINDOW_WIDTH, 
            height = WINDOW_HEIGHT, bg = BACKGROUND_COLOUR)
        self.canvas.pack()
        #create starting game icons for snake and the prey
        self.snakeIcon = self.canvas.create_line(
            (0, 0), (0, 0), fill=ICON_COLOUR, width=SNAKE_ICON_WIDTH)
        self.preyIcon = self.canvas.create_rectangle(
            0, 0, 0, 0, fill=ICON_COLOUR, outline=ICON_COLOUR)
        #display starting score of 0
        self.score = self.canvas.create_text(
            scoreTextXLocation, scoreTextYLocation, fill=textColour, 
            text='Your Score: 0', font=("Helvetica","11","bold"))
        #binding the arrow keys to be able to control the snake
        for key in ("Left", "Right", "Up", "Down"):
            self.root.bind(f"<Key-{key}>", game.whenAnArrowKeyIsPressed)

    def gameOver(self):
        """
            This method is used at the end to display a
            game over button.
        """
        gameOverButton = Button(self.canvas, text="Game Over!", 
            height = 3, width = 10, font=("Helvetica","14","bold"), 
            command=self.root.destroy)
        self.canvas.create_window(200, 100, anchor="nw", window=gameOverButton)
    

class QueueHandler():
    """
        This class implements the queue handler for the game.
    """
    def __init__(self):
        self.queue = gameQueue
        self.gui = gui
        self.queueHandler()
    
    def queueHandler(self):
        '''
            This method handles the queue by constantly retrieving
            tasks from it and accordingly taking the corresponding
            action.
            A task could be: game_over, move, prey, score.
            Each item in the queue is a dictionary whose key is
            the task type (for example, "move") and its value is
            the corresponding task value.
            If the queue.empty exception happens, it schedules 
            to call itself after a short delay.
        '''
        try:
            while True:
                task = self.queue.get_nowait()
                if "game_over" in task:
                    gui.gameOver()
                elif "move" in task:
                    points = [x for point in task["move"] for x in point]
                    gui.canvas.coords(gui.snakeIcon, *points)
                elif "prey" in task:
                    gui.canvas.coords(gui.preyIcon, *task["prey"])
                elif "score" in task:
                    gui.canvas.itemconfigure(
                        gui.score, text=f"Your Score: {task['score']}")
                self.queue.task_done()
        except queue.Empty:
            gui.root.after(100, self.queueHandler)


class Game():
    '''
        This class implements most of the game functionalities.
    '''
    def __init__(self):
        """
           This initializer sets the initial snake coordinate list, movement
           direction, and arranges for the first prey to be created.
        """
        self.queue = gameQueue
        self.score = 0
        #starting length and location of the snake
        #note that it is a list of tuples, each being an
        # (x, y) tuple. Initially its size is 5 tuples.       
        self.snakeCoordinates = [(495, 55), (485, 55), (475, 55),
                                 (465, 55), (455, 55)]
        #initial direction of the snake
        self.direction = "Left"
        self.gameNotOver = True
        self.createNewPrey()

    def superloop(self) -> None:
        """
            This method implements a main loop
            of the game. It constantly generates "move" 
            tasks to cause the constant movement of the snake.
            Use the SPEED constant to set how often the move tasks
            are generated.
        """
        SPEED = 0.15     #speed of snake updates (sec)
        while self.gameNotOver:
            #complete the method implementation below
            self.move()
            time.sleep(0.15)

    def whenAnArrowKeyIsPressed(self, e) -> None:
        """ 
            This method is bound to the arrow keys
            and is called when one of those is clicked.
            It sets the movement direction based on 
            the key that was pressed by the gamer.
            Use as is.
        """
        currentDirection = self.direction
        #ignore invalid keys
        if (currentDirection == "Left" and e.keysym == "Right" or 
            currentDirection == "Right" and e.keysym == "Left" or
            currentDirection == "Up" and e.keysym == "Down" or
            currentDirection == "Down" and e.keysym == "Up"):
            return
        self.direction = e.keysym

    def move(self) -> None:
        """ 
            This method implements what is needed to be done
            for the movement of the snake.
            It generates a new snake coordinate. 
            If based on this new movement, the prey has been 
            captured, it adds a task to the queue for the updated
            score and also creates a new prey.
            It also calls a corresponding method to check if 
            the game should be over. 
            The snake coordinates list (representing its length 
            and position) should be correctly updated.
        """
        NewSnakeCoordinates = self.calculateNewCoordinates()
        snake_X, snake_Y = self.snakeCoordinates[-1]
        prey_x1, prey_y1, prey_x2, prey_y2 = self.rectangleCoordinates
        if (snake_X + SNAKE_ICON_WIDTH//2) >= prey_x1 and (snake_X - SNAKE_ICON_WIDTH//2) <= prey_x2 and (snake_Y + SNAKE_ICON_WIDTH//2) >= prey_y1 and (snake_Y - SNAKE_ICON_WIDTH//2) <= prey_y2:
            self.rectangleCoordinates = ()
            self.score += 1
            self.createNewPrey()
            self.queue.put({"score": self.score})
        else:
            self.snakeCoordinates.pop(0)
        self.isGameOver(NewSnakeCoordinates)
        self.queue.put({"move": NewSnakeCoordinates})
        #complete the method implementation below


    def calculateNewCoordinates(self) -> tuple:
        """
            This method calculates and returns the new 
            coordinates to be added to the snake
            coordinates list based on the movement
            direction and the current coordinate of 
            head of the snake.
            It is used by the move() method.    
        """
        lastX, lastY = self.snakeCoordinates[-1]
        #complete the method implementation below
        if self.direction == "Up":
                lastY -= SNAKE_ICON_WIDTH
                # time.sleep(0.0099)
        elif self.direction == "Down":
                lastY += SNAKE_ICON_WIDTH
                # time.sleep(0.0099)
        elif self.direction == "Right":
                lastX += SNAKE_ICON_WIDTH
                # time.sleep(0.0099)
        elif self.direction == "Left":
                lastX -= SNAKE_ICON_WIDTH
                # time.sleep(0.0099)

        new_head = (lastX,lastY)       
        self.snakeCoordinates.append(new_head)
        return self.snakeCoordinates

    def isGameOver(self, snakeCoordinates) -> None:
        """
            This method checks if the game is over by 
            checking if now the snake has passed any wall
            or if it has bit itself.
            If that is the case, it updates the gameNotOver 
            field and also adds a "game_over" task to the queue. 
        """
        #complete the method implementation below
        snakeHead = snakeCoordinates[-1]  # Get the coordinates of the snake's head
        x, y = snakeHead
        NewSnakeCoordinates = snakeCoordinates[0:-1]

        # Check if the snake has collided with itself
        for segment in NewSnakeCoordinates:
            if snakeHead == segment:
                self.gameNotOver = False
                self.queue.put({"game_over": True})
                return

        # Check if the snake has collided with any of the walls
        if x < 0 or x >= WINDOW_WIDTH or y < 0 or y >= WINDOW_HEIGHT:
            self.gameNotOver = False
            self.queue.put({"game_over": True})


    def createNewPrey(self) -> None:
        """ 
            This methods picks an x and a y randomly as the coordinate 
            of the new prey and uses that to calculate the 
            coordinates (x - 5, y - 5, x + 5, y + 5). [you need to replace 5 with a constant]
            It then adds a "prey" task to the queue with the calculated
            rectangle coordinates as its value. This is used by the 
            queue handler to represent the new prey.                    
            To make playing the game easier, set the x and y to be THRESHOLD
            away from the walls. 
        """
        THRESHOLD = 45   #sets how close prey can be to borders
        #complete the method implementation below
        x = random.randint(THRESHOLD, WINDOW_WIDTH - THRESHOLD)
        y = random.randint(THRESHOLD, WINDOW_HEIGHT - THRESHOLD)

        prey_coords =(x,y)

        snakeSize = len(self.snakeCoordinates)
        
        for i in range(0,snakeSize):
            if self.snakeCoordinates[i] == prey_coords:
                x = random.randint(THRESHOLD, WINDOW_WIDTH - THRESHOLD)
                y = random.randint(THRESHOLD, WINDOW_HEIGHT - THRESHOLD)
            else:
                break
        # Calculate rectangle coordinates for the new prey
        self.rectangleCoordinates = (x - PREY_ICON_WIDTH/2, y - PREY_ICON_WIDTH/2, x + PREY_ICON_WIDTH/2, y + PREY_ICON_WIDTH/2)
        # Add "prey" task to the queue
          
        self.queue.put({"prey": self.rectangleCoordinates})


if __name__ == "__main__":
    #some constants for our GUI
    WINDOW_WIDTH = 500           
    WINDOW_HEIGHT = 300 
    SNAKE_ICON_WIDTH = 15
    PREY_ICON_WIDTH = 10     # prey Icon width ADDED
    #add the specified constant PREY_ICON_WIDTH here     

    BACKGROUND_COLOUR = "green"   #you may change this colour if you wish
    ICON_COLOUR = "yellow"        #you may change this colour if you wish

    gameQueue = queue.Queue()     #instantiate a queue object using python's queue class

    game = Game()        #instantiate the game object

    gui = Gui()    #instantiate the game user interface
    
    QueueHandler()  #instantiate the queue handler    
    
    #start a thread with the main loop of the game
    threading.Thread(target = game.superloop, daemon=True).start()

    #start the GUI's own event loop
    gui.root.mainloop()