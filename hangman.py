import os
import pandas as pd
import random

wordToGuess = ""
wordToDisplay = "initate"
guesses = 0
guessSTR = ""


# cross platform console clear to change the HUD
def clearConsole():
    command = 'clear'
    if os.name in ('nt', 'dos'):
        command = 'cls'
    os.system(command)


# this is to go from a number, to a Str to display (i.e. 3 guesses = XXX---)
def guessToSTR():
    i = 0
    global guessesSTR
    guessesSTR = ""

    while (i < 6):
        if (i < guesses):
            guessesSTR = guessesSTR + "X"
        else:
            guessesSTR = guessesSTR + "-"
        i = i + 1


# pick a word from our pandas dataframe
def selectWord():
    wordIndex = random.randint(1, len(wordList_filtered))

    specificWord = wordList_filtered['Word'].loc[[wordIndex]].item()

    return specificWord.lower()


# reset to a new word (then select the word, with selectWord)
def findNewWord():
    global guesses
    global wordToGuess
    global wordToDisplay
    guesses = 0
    wordToGuess = selectWord()
    wordToDisplay = obfuscateWord(wordToGuess)



# refresh the display, based on the latest guess
def refreshDisplay():
    global finalDisplay
    global wordToDisplay

    wordToDisplay = obfuscateWord(wordToGuess)
    clearConsole()
    guessToSTR()
    finalDisplay = wordToDisplay + "   |   Guesses: " + guessesSTR + "\n\n"

    print(finalDisplay)
    # still needs the input, from the while loop


# this changes if a letter's been guessed, then adds 1 to the guesses (which should almost be called "missedGuesses" as it only increases when a wrong letter has been guessed)
def guessLetter(letter):
    try:
        global guesses
        lettersNotGuessed.remove(letter)
        lettersGuessed.append(letter)

        if (guess not in wordToGuess):
            guesses = guesses + 1
    except:
        pass



# set the wordToDisplay variable (with *'s as the missing letters)
def obfuscateWord(word):
    for x in lettersNotGuessed:
        word = word.replace(x, "*")

    return word





"""
import the refined word list from:
https://github.com/antares330/wordGameList/
"""
input_file = "game_dictionary_filtered.csv"
wordList = pd.read_csv(input_file)

# hangman wouldn't be much fun for words shorter then 4..
length_filter = wordList['CharCount']>3
wordList_filtered = wordList[length_filter]





# setup the letters available to be guessed

lettersNotGuessed = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
lettersGuessed = []


findNewWord()
refreshDisplay()

"""
desired result:
a**-*a**   |   Guesses: XX----

Letters guessed: a, b, c

Enter a letter: _
"""


# this is the engine that keeps asking for inputs, and then uses functions to verify and change the HUD
while (guesses < 7):
    if (wordToGuess != wordToDisplay):
        guess = ""

        # keep asking for an input, until we get a single, alpha numeric character
        while (not(guess.isalpha()) and len(guess) != 1):

            # set up a display for the letters already guessed
            lettersGuessedDisplay = ""

            for i in lettersGuessed:
                lettersGuessedDisplay = lettersGuessedDisplay + i + ", "

            # this takes care of the extra comma at the end
            lettersGuessedDisplay = lettersGuessedDisplay[:-2]



            # display letters guessed
            print("Letters guessed: " + lettersGuessedDisplay + "\n")

            # ask for input
            guess = input("Enter a letter: ")


        guessLetter(guess)
        #print(lettersGuessed)
        #if (guess not in wordToGuess):
        #    guesses = guesses + 1
        refreshDisplay()
    else:
        print("You win! The word was " + wordToGuess + ".. but you already knew that xD")
else:
    print("You've run out of guesses.. The word was " + wordToGuess)
