'''main
The main file that allows one to run Ascii-Wordle
Contains the functions and objects used to run the game'''

import blessed
import json
import pyperclip
import random
import time
import text


term = blessed.Terminal()
letterDict = text.lettersDict


class Box:
    '''A class to handle the drawing of 20x10 ASCII Boxes
    These are the analogue of the Wordle "boxes"
    
    Attributes
    ----------
    self.loc : list
        Stores the "location" of each box'''

    def __init__(self, loc : list):
        self.loc = loc
    

    def draw(self, color : str , sleep : float = 0) -> None:  
        '''Draws a box of color "color"
        
        Parameters
        ----------
        color : str
            A str sequence that defines the box color
        sleep : float
            Pauses the drawing of a row for "sleep" seconds to provide a "wipe" animation effect
        
        Returns
        -------
        None'''

        print(color,end = '')

        for i in range(10):
            print(f'{term.move_xy(self.loc[0], self.loc[1] + i)}{"█"*20}')
            time.sleep(sleep) #gives a nice wipe effect
            
        print(term.normal, end = '', flush = True)


class Wordle:
    '''Class that handles game logic for ASCII Wordle
    
    Attributes
    ----------
    boxGrid : list
        The boxes that make up the game screen
        User input is drawn over it
    secretWord : str
        The winning word
    wordList : set
        The set of all valid words
    count : dict
        A dictionary that contains the count of each letter in
        secretWord, in the form letter : count
    corrects : list
        Contains per-letter input validity, corresponding to that of
        Wordle's orange, green, and grey boxes (assuming dark mode)
    curRow : int
        Current active "row" of input'''

    def __init__(self):
        block = input('''
        Maximize your window, set the font size low enough. Press enter to start!
        Do NOT resize your window during gameplay
        ''')
        print(term.clear)
        self.drawWords('WORDLEBUTWORSE', (160,20), term.white) #a nice title!

        self.boxGrid = [[ Box([180+(21*i), 30+(11*j)]) for i in range(0,5) ] for j in range(0,6)]
        self.drawCanvas()

        

        with open('wordList.json', 'r') as textFile:
            wordList = json.load(textFile)
            self.secretWord = random.choice(wordList[0])
            self.wordList = set(wordList[1])

        self.count = self.generateCount()
        self.corrects = []
        self.curRow  = 0
        
    

    def drawCanvas(self) -> None:
        '''Draws all 6 rows of boxes on screen
        Parameters
        ----------
        
        Returns
        -------
        None'''

        for i  in self.boxGrid:
            for j in i:
                j.draw(term.grey8)


    def drawLetterBox(self, letter : list, gridVal : tuple, color : str) -> None:
        '''Draws a giant letter at the specified location
        To account for whitespace characters drawing over the boxes
        and leaving holes, whitespace characters are drawn with a
        color matching that of the "background" box

        An extra offset is added to "gridVal" when printing to center
        the giant ASCII letters
        
        Parameters
        ----------
        letter : list
            Text representing a giant ASCII letter, split along
            newline breaks to allow for cursor position incrementing
        gridVal : tuple
            Prints the text starting from the location of a specified
            box
        color : str
            Draws whitespace characters with color "color"
            to prevent the overwriting of background boxes
        
        Returns
        --------
        None'''

        for col, rowChar in enumerate(letter):
            for row, char in enumerate(rowChar):
                
                if char != ' ':
                    print(f'{term.normal}{term.move_xy(gridVal[0]+row + 5, gridVal[1]+col + 1)}{char}', end = '', flush =  True)

                else:
                    print(f'{color}{term.move_xy(gridVal[0]+row + 5, gridVal[1]+col + 1)}{"█"}', end = '', flush = True)


    def drawWords(self, word : str, startPos : tuple, color : str) -> None:
        '''Allows for the drawing of entire words on screen
        Since words are drawn outside the game "canvas",
        per-character printing isn't used as there is no point in
        printing each character. Quickens the drawing algorithm too

        White-space support isn't available to prevent shenanigans
        with user-input (Can be fixed in the future)
        
        Parameters
        ----------
        word : str
            The word to be printed
        startPos : tuple
            Unlike "gridVal", allows for grid-free printing to print
            anywhere
        color : str
            Used to print each and every color in color "color"
            Added as a parameter to allow for screen0wiping by
            printing in black
            
        Returns
        -------
        None'''

        print(color)

        for col, rowChar in enumerate(word):

            for index, rowChar in enumerate(letterDict[rowChar].split('\n')):
                print(f'{term.move_xy(startPos[0] + 10*col, startPos[1]+index)}{rowChar}')
                
        print(term.normal)


    def generateCount(self) -> dict:
        '''Generates a dictionary containing the count of each
        unique character in secretWord
        
        Parameters
        ----------
        
        Returns
        -------
        count : dict'''

        count = dict()
        for i in self.secretWord:
            if i not in count:
                count[i] = 1
            else:
                count[i] += 1

        return count


    def evaluateInput(self, guess : str) -> None:
        '''Checks the user's guess's validity against the secretWord
        Adds colored emoji squares to corrects to allow for score
        sharing
        
        Parameters
        ----------
        guess : str 
            The user's guess for a particular row
        
        Returns
        -------
        None'''

        for index, char in enumerate(guess):

            if char == self.secretWord[index] and self.loopCount[char] > 0:
                self.boxGrid[self.curRow][index].draw(term.chartreuse3, 0.01)
                    
                self.drawLetterBox(letterDict[char].split('\n'), calculatePos(index, self.curRow), term.chartreuse3)
                self.loopCount[char] -= 1
                self.corrects[self.curRow] += '🟩'
            
            elif char in self.secretWord and self.loopCount[char] > 0:
                self.boxGrid[self.curRow][index].draw(term.gold2, 0.01)

                self.drawLetterBox(letterDict[char].split('\n'), calculatePos(index, self.curRow), term.gold2)
                self.loopCount[char] -= 1
                self.corrects[self.curRow] += '🟨'
            
            else:
                self.boxGrid[self.curRow][index].draw(term.grey23, 0.01)

                self.drawLetterBox(letterDict[char].split('\n'), calculatePos(index, self.curRow), term.grey23)
                self.corrects[self.curRow] += '⬛'


    def removeLetter(self, inputArr : list) -> None:
        '''Removes most recently drawn letter by drawing its
        corresponding box over it
        Also removes the last character entered, from "inputArr"
        
        Parameters
        ----------
        inputArr : list
            Contains the user's currently guessed letters
            of the current row
            
        Returns
        -------
        None'''

        inputArr[0 : len(inputArr)] = inputArr[0:5] #edit the list within func, no need to return. Breaks least astonishment tho :(
        #didn't use self.inputArr above because I felt it'd look messy

        if len(inputArr) > 0:
            self.boxGrid[self.curRow][len(inputArr)-1].draw(term.grey8)
            inputArr.pop()


    def evaluateError(self, key : str) -> None:
        '''Checks if the current row's input has any issues
        Draws a corresponding message and overwrites key to prevent
        the loop from ending
        
        Parameters
        ----------
        key : str
            Last entered key
        
        Returns
        -------
        key : str'''

        if len(self.inputArr) < 5:
            self.drawWords('NOTENOUGHLETTERS', (160,100), term.white)
            return ''
        
        
        elif  ''.join(self.inputArr) not in self.wordList:
            self.drawWords('NOTINWORDLIST', (170,100), term.white) 
            key = ''
            return ''
        
        return key


    def gameLoop(self) -> None: #To whoever is reading this, I am so sorry :(
        '''Starts the main game loop
        Allows for 6 guesses. Enters a context manager that allows
        for the immediate returning of user input
        Ends the game once the loop is over/has been prematurely
        broken out of
        
        Parameters
        ----------
        
        Returns
        -------
        None'''

        while self.curRow <= 5:
            self.corrects.append('')
            self.loopCount = self.count.copy() #lighter than recalculating every loop

            with term.cbreak(): #context manager to allow for "live-input"
                key = '' #declaration
                self.inputArr = []

                while repr(key) != 'KEY_ENTER':
                    
                    key = term.inkey()
                    keyName = key.name if key.is_sequence else key #handles getting keyname for both regular keys and keys like CTRL,ENTER, etc

                    if key.name == 'KEY_ENTER':
                        self.drawWords('################', (160,100), term.black)
                        key = self.evaluateError(key)
                            
                        continue
                        
                    elif key.name == 'KEY_BACKSPACE':
                        self.removeLetter(self.inputArr)
                        continue

                    elif keyName.upper() in letterDict: #Input sanitation
                        self.inputArr.append(keyName.upper())
                        self.drawLetterBox(letterDict[keyName.upper()].split('\n'), calculatePos(len(self.inputArr[0:5]) - 1, self.curRow), term.grey8) #push them to next box
                        continue
                    
                    self.inputArr.append(keyName)
                    self.inputArr.pop() #prevents usage of non-alpha keys
                        
            guess = ''.join(self.inputArr)[0:5]
            self.evaluateInput(guess)

            if self.corrects[self.curRow].count('🟩') == 5: #quits gameloop if player got it right
                break
                
            self.curRow += 1
        
        self.gameEnd()


    def gameEnd(self) -> None:
        '''Ends the game and draws remarks, analogous to that of
        Wordle remarks, on screen
        Also copies game results to the user's clipboard
        
        Parameters
        ----------
        
        Returns
        -------
        None'''

        winRemark = [
        'GENIUS',  'MAGNIFICENT',  'IMPRESSIVE', 
        'SPLENDID', 'GREAT','PHEW', self.secretWord
        ]

        self.drawWords(winRemark[self.curRow], (160 + (30 - len(winRemark[self.curRow])),100), term.white)
        pyperclip.copy(f"Wordle {self.curRow+1}/6{chr(10)}{chr(10).join(self.corrects)}") #have to center stuff later
        stop = input() #prevents program from closing upon completion


def calculatePos(row : int, col :int) -> tuple:
    '''Calculates the location of a box at (row,col) in the game grid
    
    Parameters
    ----------
    row : int
        The row the box belongs to
    col : int
        The column the box belongs to
        
    Returns
    -------
    tuple'''

    return (180+(21*row), 30 + (11*col))
        

def main() -> None:
    '''Creates a game object and runs the game loop
    
    Parameters
    ----------
    
    Returns
    -------
    None'''

    game = Wordle()
    game.gameLoop()


main()
