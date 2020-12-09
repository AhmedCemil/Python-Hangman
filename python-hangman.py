# Name of the Program / Program adı:        Hangman game / Adam asmaca oyunu
# Creator / Hazırlayan:                     Ahmed Cemil Bilgin
# Time spend / Harcanan Zaman:              2 Days / 2 Gün

import random
import string
import pandas as pd
from time import sleep

word_list_file_name = "word_list.csv"
turkish_alphabet = 'abcçdefgğhıijklmnoöprsştuüvyz'

def load_word_list():
    '''
    Returns a list of valid words.
    Words are strings of lowercase letters.
    
    Depending on the size of the word list,
    this function may take a while to finish.
    '''
    print("Loading word list from file...")
    # reading file
    word_list_file = pd.read_csv(word_list_file_name)
    # converting words to lowercase
    word_list_file['WORDS'] = word_list_file['WORDS'].str.lower() 
    # word_list: list of strings
    word_list = word_list_file['WORDS'].tolist()
    print(f"{len(word_list)} words loaded.")
    return word_list



def pick_a_word(word_list):
    '''
    word_list (list): list of words (strings)
    Returns a word from word_list at random.
    '''
    return random.choice(word_list)

word_list = load_word_list()

def is_all_guessed(asked_word, guessed_letters):
    '''
    asked_word: string, the word the user is guessing
    guessed_letters: list, what letters have been guessed so far
    returns: boolean, True if all the letters of asked_word are in guessed_letters;
            False otherwise
    '''
    count = 0
    for i in range(len(guessed_letters)):
        for j in range(len(asked_word)):
            if asked_word[j] == guessed_letters[i]:
                count += 1
    if count == len(asked_word):
        return True
    else:
        return False



def fill_in_the_blanks(asked_word, guessed_letters):
    '''
    asked_word: string, the word the user is guessing
    guessed_letters: list, what letters have been guessed so far
    returns: string, comprised of letters and underscores that represents
            what letters in asked_word have been guessed so far.
    '''
    blanks_filled_word = ["_ "]*len(asked_word)
    for i in range(len(guessed_letters)):
        for j in range(len(asked_word)):
            if asked_word[j] == guessed_letters[i]:
                blanks_filled_word[j] = asked_word[j]
    return blanks_filled_word



def remaining_letters(guessed_letters, alphabet = turkish_alphabet):
    '''
    guessed_letters: list, what letters have been guessed so far
    returns: string, comprised of letters that represents what letters have not
            yet been guessed.
    '''
    alphabet = turkish_alphabet
    for i in range(len(guessed_letters)):
        alphabet = alphabet.replace(guessed_letters[i],'')
    return alphabet
    
    

def hangman(asked_word, alphabet = turkish_alphabet):
    '''
    asked_word: string, the asked word to guess.

    Starts up an interactive game of Hangman.

    * At the start of the game, let the user know how many 
      letters the asked_word contains.

    * Ask the user to supply one guess (i.e. letter) per round.

    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computers word.

    * After each round, you should also display to the user the 
      partially guessed word so far, as well as letters that the 
      user has not yet guessed.

    Follows the other limitations detailed in the problem write-up.
    '''
    alphabet = turkish_alphabet

    vowel_letters = "aeıioöuü"
    print("***************************************************************\n")
    remaining_guess = 6
    remaining_mistakes = 3
    print("The word contains", len(asked_word), "letters.")
    print("Except for the appropriate letters, you can only enter incorrectly 3 times.\nPlease guess a letter among the appropriate letters!\n")
    guessed_letters = []
    vowel_guessed = 0
    while True:
        alphabet = remaining_letters(guessed_letters)
        print("Suitable letters you can guess:", alphabet)
        print("You have", str(remaining_guess), "guesses left.")
        print("Guess a letter:", end=" ")
        guessed_letter = input().lower()
        while alphabet.count(guessed_letter) != 1:
            remaining_mistakes -= 1
            if remaining_mistakes == 0:
                print("\nYou no longer have the right to make mistakes. You lost!")
                print("The word you try to guess is " + asked_word)
                return False
            else:
                print("\n\t\t! WARNING !")
                print("You must enter a letter from the Turkish alphabet or a letter that you have not guessed before.")
                print("You are left to make a mistake " + str(remaining_mistakes) + " times.")
                print("Suitable letters you can guess:", alphabet)
                print("Guess a letter:", end=" ")
                guessed_letter = input().lower()
        guessed_letters.append(guessed_letter)

        blanks_filled_word = fill_in_the_blanks(asked_word,guessed_letters)
        if blanks_filled_word.count(guessed_letter) > 0:
            if vowel_letters.count(guessed_letter):
                vowel_guessed = 1
            if is_all_guessed(asked_word,guessed_letters):
                print("\nCongratulations! You got the word " + asked_word + " right!\n")
                unique_letters = list(set(asked_word))
                total_score = remaining_guess * len(unique_letters)
                print("Your total score:", total_score)
                return True
            else:
                print("\nRight guess! Keep guessing: " + "".join(blanks_filled_word) + "\n")
        else:
            if vowel_letters.count(guessed_letter) > 0 and vowel_guessed == 0:
                remaining_guess -= 2
            else:
                remaining_guess -= 1
            print("\nMy word does not contain the letter " + guessed_letter + "\n")
            if remaining_guess <= 0:
                print("Your right to guess is over. You lost!")
                print("The word you try to guess is: " + asked_word)
                return False
        print("----------------------------------------------------------------------\n")
        print("The Word: " + "".join(blanks_filled_word))



def matching_words(asked_word, word_in_list):
    '''
    asked_word: string, the asked word to guess.
    word_in_list: dize, a word in word_list.
    returns: string, comprised of letters and underscores that represents
            what letters in asked_word have been guessed so far.
    '''
    number_of_matching_letters = 0
    backup_word = []
    for k in asked_word: backup_word.append(k)
    while '_ ' in backup_word: backup_word.remove('_ ')
    for i in range(len(asked_word)):
        if asked_word[i] == word_in_list[i] and asked_word[i] != '_ ':
            number_of_matching_letters += 1
    if number_of_matching_letters == len(backup_word):
        return True
    else:
        return False



def show_possible_matches(asked_word):
    '''
    asked_word: string, the asked word to guess.
    returns: nothing, but should print every word that matches my_word in the word list.
            Note that when a letter is guessed on the screen,
            all positions where that letter occurs in the hidden word are revealed.
            Therefore, the hidden letter (_) cannot be one of the letters in the word that has already been exposed.
    '''
    matching_word_list = []

    backup_word = []
    backup_word_harfler = []
    for k in asked_word: backup_word.append(k)
    while '_ ' in backup_word: backup_word.remove('_ ')
    backup_word_harfler = list(set(backup_word))

    for i in word_list:
        if len(i) == len(asked_word):
            matching_word_list.append(i)
    for j in matching_word_list:
        if matching_words(asked_word,j) == True:
            suitable = True
            for k in range(len(asked_word)):
                if asked_word[k] == '_ ' and backup_word_harfler.count(j[k]) > 0:
                    suitable = False
            if suitable:
                print("Suitable words:", j, end="\n")



def hangman_with_hints(asked_word, alphabet=turkish_alphabet):
    '''
    asked_word: string, the asked word to guess.

    Starts up an interactive game of Hangman.

    * At the start of the game, let the user know how many 
      letters the asked_word contains.

    * Ask the user to supply one guess (i.e. letter) per round.

    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computers word.

    * After each round, you should also display to the user the 
      partially guessed word so far, as well as letters that the 
      user has not yet guessed.
     
     * If the guess is the symbol *, print all the words matching the current predicted word in the word list.
    
    Follows the other limitations detailed in the problem write-up.
    '''
    alphabet = turkish_alphabet

    vowel_letters = "aeıioöuü"
    print("***************************************************************\n")
    remaining_guess = 6
    remaining_mistakes = 3
    print("Gizli kelimemiz", len(asked_word), "harf içermektedir.")
    print("Uygun harfler dışında sadece 3 kez hatalı giriş yapabilirsiniz.\nLütfen uygun harfler arasından Guess a letter!\n")
    guessed_letters = []
    vowel_guessed = 0
    unique_letter_index = random.randrange(0, len(asked_word))
    while True:
        alphabet = remaining_letters(guessed_letters)
        print("Suitable letters you can guess:", alphabet)
        print("You have", str(remaining_guess), "guesses left.")
        print("Guess a letter:", end=" ")
        guessed_letter = input().lower()
        while alphabet.count(guessed_letter) != 1:
            remaining_mistakes -= 1
            if remaining_mistakes == 0:
                print("\nYou no longer have the right to make mistakes. You lost!")
                print("The word you try to guess is " + asked_word)
                return False
            else:
                print("\n\t\t! WARNING !")
                print("You must enter a letter from the Turkish alphabet or a letter that you have not guessed before.")
                print("You are left to make a mistake " + str(remaining_mistakes) + " times.")
                print("Suitable letters you can guess:", alphabet)
                print("Guess a letter:", end=" ")
                guessed_letter = input().lower()
        guessed_letters.append(guessed_letter)
        blanks_filled_word = fill_in_the_blanks(asked_word,guessed_letters)
        if blanks_filled_word.count(guessed_letter) > 0:
            if vowel_letters.count(guessed_letter):
                vowel_guessed = 1
            if is_all_guessed(asked_word,guessed_letters):
                print("\nCongratulations! You got the word " + asked_word + " right!\n")
                unique_letters = list(set(asked_word))
                total_score = remaining_guess * len(unique_letters)
                print("Your total score:", total_score)
                return True
            else:
                print("\nRight guess! Keep guessing: " + "".join(blanks_filled_word) + "\n")
                if blanks_filled_word[unique_letter_index] != '_ ':
                    print("Congratulations! You guessed the particular letter.")
                    sleep(1.5)
                    print("Therefore, you no longer have the right to guess.")
                    sleep(1.5)
                    print("You are expected to guess the word.")
                    sleep(1.5)
                    print("Below are the words that are compatible with what you can guess..")
                    sleep(1.5)
                    show_possible_matches(blanks_filled_word)
                    print("Enter the word you guessed:", end=" ")
                    last_blanks_filled_word = input()
                    if last_blanks_filled_word == asked_word:
                        print("\nCongratulations! You got the word " + asked_word + " right!\n")
                        unique_letters = list(set(asked_word))
                        total_score = remaining_guess * len(unique_letters)
                        print("Your total score:", total_score)
                        return True
                    else:
                        print("\nUnfortunately you could not guess the word. You lost!")
                        print("The word you try to guess is: " + asked_word)
                        return False
        else:
            if vowel_letters.count(guessed_letter) > 0 and vowel_guessed == 0:
                remaining_guess -= 2
            else:
                remaining_guess -= 1
            print("\nMy word does not contain the letter " + guessed_letter + "\n")
            if remaining_guess <= 0:
                print("Your right to guess is over. You lost!")
                print("The word you try to guess is: " + asked_word)
                return False
        print("----------------------------------------------------------------------\n")
        print("The Word: " + "".join(blanks_filled_word))


if __name__ == "__main__":
    print("\nWelcome to the hangman game. Please select the game type you want to play;")
    print("type 1 to play hangman 1")
    print("type 2 to play hangman with hints: ", end="")
    choice = int(input())
    print("")
    asked_word = pick_a_word(word_list)
    if choice == 1:
        hangman(asked_word, alphabet=turkish_alphabet)
    if choice == 2:
        hangman_with_hints(asked_word, alphabet=turkish_alphabet)