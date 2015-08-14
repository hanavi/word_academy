#!/usr/bin/env python

import cheat

mybox = cheat.wordbox(maxboxid=True)

def drop_word(word):
    word_list = mybox.find_specific_word(word)
    if word_list is None:
        print("\nError: Word not found!")
        return None

    print("\nPlease select word to drop from list\n")

    for i,word in enumerate(word_list):
        print("({}) {}".format(i, word))

        mybox.print_letter_box(highlight=word)
        mybox.drop_word(word)
        mybox.print_letter_box()
        mybox.undo_drop_word()

    print(" ")

    n = raw_input("Drop (q to cancel): ")
    letter_range = [str(i) for i in range(len(word_list))]

    if n == 'q':
        return
    elif n in letter_range:
        mybox.drop_word(word_list[int(n)])
        mybox.print_letter_box()
    else:
        print("\nError: Please try again")



menu = ("\n"
        "Please select from options below \n"
        "--------------------------------------------\n"
        "(p) Print word box \n"
        "(f) Find words \n"
        "(w) Print found word grid \n"
        "(d) Drop word \n"
        "(u) Undo drop word \n"
        "(l) List current operations \n"
        "(r) Replay current operations \n"
        "(q) Quit \n"
        "--------------------------------------------\n")

if __name__ == '__main__':
    c = True
    while(c):
        print(menu)
        command = raw_input("Command: ")

        if command == 'p':
            mybox.print_letter_box()
        elif command == 'f':
            n = int(raw_input("Enter word length: "))
            mybox.find_words(n)
            mybox.print_word_grid()
        elif command == 'w':
            mybox.print_word_grid()
        elif command == 'q':
            c = False
        elif command == 'd':
            dword = raw_input("Enter word to drop: ")
            drop_word(dword)
        elif command == 'u':
            mybox.undo_drop_word()
            mybox.print_letter_box()
        elif command == 'l':
            mybox.list_operations()
        elif command == 'r':
            mybox.run_list(show_steps=True)
        else:
            print("\nCommand not found! Please try again")

    print ("\n")

