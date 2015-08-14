#!/usr/bin/env python

import numpy as np
from boxes import boxes
import logging


class wordbox(object):

    def __init__(self, starting=None, boxid=0, verbose=False, maxboxid=False):

        # Deal with logging
        if verbose is True:
            logging.getLogger().setLevel(logging.DEBUG)
        else:
            logging.getLogger().setLevel(logging.WARN)

        # Load a grid from file if one is not given
        if starting is None:
            if maxboxid:
                boxid = max(boxes.keys())
            starting = boxes[boxid]

        # Set some useful variables
        self.n = np.sqrt(len(starting))            # Grid size
        self.letterbox_original = starting.copy()  # Set the original grid
        self.letterbox = starting.copy()           # Set the grid for use
        self.total_length = len(self.letterbox)    # Total number of entries

        # Build the numberbox
        tmp = np.array(range(starting.size))
        self.numberbox = tmp.reshape(self.n, self.n)

        # This is the storage for the quick repeat of the drop function
        self.repeat_list = []
        self.repeat_list_words = []

        # Deal with the dictionary
        self.dict_is_loaded = False
        self.load_dictionary()

        # Temp store word list
        self.word_list = None

        # Set up the color pallatte
        self.colors = {
            'BBLUE' : '\033[1;36m',
            'OKGREEN' : '\033[92m',
            'BRED' : '\033[1;31m',
            'DEFAULT' : '\033[0m'
        }

    def get_neighbors(self, boxnum):
        """ Return a list of neighbors for a given box position """

        nlist = []

        top_edge = self.numberbox[0]
        bottom_edge = self.numberbox[-1]
        left_edge = self.numberbox[:, 0]
        right_edge = self.numberbox[:, -1]

        if boxnum == 0:
            nlist.append(boxnum + 1)
            nlist.append(boxnum + self.n)
            nlist.append(boxnum + self.n + 1)

            return np.array(nlist).astype(int)

        if boxnum == self.n - 1:
            nlist.append(boxnum - 1)
            nlist.append(boxnum + self.n)
            nlist.append(boxnum + self.n - 1)

            return np.array(nlist).astype(int)

        if boxnum == self.n*self.n - 1:
            nlist.append(boxnum - 1)
            nlist.append(boxnum - self.n)
            nlist.append(boxnum - self.n - 1)

            return np.array(nlist).astype(int)

        if boxnum == self.n*self.n - self.n:
            nlist.append(boxnum + 1)
            nlist.append(boxnum - self.n)
            nlist.append(boxnum - self.n + 1)

            return np.array(nlist).astype(int)

        if boxnum in top_edge:
            nlist.append(boxnum - 1)
            nlist.append(boxnum + 1)
            nlist.append(boxnum + self.n)
            nlist.append(boxnum + self.n - 1)
            nlist.append(boxnum + self.n + 1)

            return np.array(nlist).astype(int)

        if boxnum in bottom_edge:
            nlist.append(boxnum - 1)
            nlist.append(boxnum + 1)
            nlist.append(boxnum - self.n)
            nlist.append(boxnum - self.n - 1)
            nlist.append(boxnum - self.n + 1)

            return np.array(nlist).astype(int)

        if boxnum in left_edge:
            nlist.append(boxnum + 1)
            nlist.append(boxnum + self.n)
            nlist.append(boxnum - self.n)
            nlist.append(boxnum + self.n + 1)
            nlist.append(boxnum - self.n + 1)

            return np.array(nlist).astype(int)

        if boxnum in right_edge:
            nlist.append(boxnum - 1)
            nlist.append(boxnum + self.n)
            nlist.append(boxnum - self.n)
            nlist.append(boxnum + self.n - 1)
            nlist.append(boxnum - self.n - 1)

            return np.array(nlist).astype(int)

        nlist.append(boxnum + 1)
        nlist.append(boxnum - 1)
        nlist.append(boxnum + self.n)
        nlist.append(boxnum - self.n)
        nlist.append(boxnum + self.n + 1)
        nlist.append(boxnum - self.n + 1)
        nlist.append(boxnum + self.n - 1)
        nlist.append(boxnum - self.n - 1)

        return np.array(nlist).astype(int)

    def get_words(self, entry, count, prefilter_length=3, prefilter=True):
        """ Return all words found that pass an initial prefilter """

        words = []
        words.append([entry])

        if prefilter:
            self.set_filters(count, self.letterbox[entry], prefilter_length)

        for i in range(count-1):
            new_words = []

            for word in words:
                surr = self.get_neighbors(word[-1])
                for s in surr:
                    if s not in word and self.letterbox[s] != ' ':
                        if prefilter:
                            if i == (prefilter_length-2):
                                tword = word[:]
                                tword.extend([s])
                                text_word = self.get_text_word(tword)
                                if text_word in self.d_filter_short:
                                    new_words.append(tword)
                            else:
                                tword = word[:]
                                tword.extend([s])
                                new_words.append(tword)
                        else:
                            tword = word[:]
                            tword.extend([s])
                            new_words.append(tword)

            words = new_words

        return words

    def get_text_word(self, word):
        """ Convert number words to text words """

        t_word = ''
        for i in word:
            t_word += self.letterbox[i]
        return t_word

    def load_dictionary(self):
        """ Load the dictionary from file """

        fname = "/usr/share/dict/words"
        fd = open(fname)
        self.dictionary = np.unique([line.rstrip().lower() for line in fd])
        fd.close()
        self.dict_is_loaded = True

    def check_word(self, word, is_text=False):
        """ Check to see if a word is in the dictionary """

        if self.dict_is_loaded is False:
            self.load_dictionary()

        if not is_text:
            text_word = self.get_text_word(word)
        else:
            text_word = word

        if text_word[:3] in self.d_filter_short:
            if text_word in self.d_filter:
                return True
            elif (text_word[-1] == 's' and
                  text_word[:-1] in self.d_filter_plurals):
                return True
            else:
                return False
        else:
            return False

    def set_filters(self, word_length, letter, pre_filter_length=3):
        """ Set up the filters so we can process the dictionary faster """

        logging.debug("Setting filter -> length = {}, letter = {}".format(
            word_length, letter))

        self.d_filter = filter(lambda d: (len(d) == word_length and
                               d[0] == letter),
                               self.dictionary)

        self.d_filter_short = np.unique([short[:pre_filter_length] for
                                         short in self.d_filter])

        self.d_filter_plurals = filter(
            lambda d: len(d) == (word_length-1) and d[0] == letter and
            d[-1] != 's', self.dictionary
        )

    def find_words(self, word_length=3):
        """ Search for words of a given length over all starting positions """

        if self.dict_is_loaded is False:
            self.load_dictionary()

        all_words = {}
        for i in range(self.total_length):

            all_words = self.find_words_from_pos(
                i, word_list=all_words,
                word_length=word_length
            )

        self.word_list = all_words
        # return all_words

    def find_words_from_pos(self, start, word_list=None, word_length=3,
                            runfilter=True):
        """ Search for words of a given length starting at a particular
        location
        """

        if word_list is None:
            word_list = {}

        logging.info("Processing box: {} ({})".format(start,
                                                      self.letterbox[start]))
        if self.letterbox[start] == ' ':
            return word_list

        words = self.get_words(start, word_length, prefilter=runfilter)
        logging.info("Found {} words".format(len(words)))

        for word in words:
            if not runfilter or self.check_word(word) == True:
                text_word = self.get_text_word(word)
                if text_word not in word_list:
                    word_list[text_word] = []

                word_list[text_word].append(word)

                # print self.get_text_word(word), word

        # self.word_list = word_list
        return word_list

    def find_words_from_letter(self, letter, word_length=3, runfilter=True):
        """ Search for all words of a given length starting with a particular
        letter
        """

        n = np.argwhere(self.letterbox == letter)
        word_list = {}
        for n0 in n:
            word_list = self.find_words_from_pos(
                n0[0], word_list=word_list, runfilter=runfilter,
                word_length=word_length
            )
        self.word_list = word_list
        return word_list

    def drop_word(self, word):
        """ Drop a word from the grid and update the grid """

        self.repeat_list_words.append(self.get_text_word(word))

        for i in word:
            self.letterbox[i] = ' '

        for i in range(int(self.n)):
            cols = []
            for j in range(self.total_length):
                if j % self.n == i:
                    cols.append(j)

            letters = [self.letterbox[k] for k in cols
                       if self.letterbox[k] != ' ']

            letters.reverse()

            for j in range(int(self.n)-len(letters)):
                letters.append(' ')

            letters.reverse()

            for j, k in enumerate(cols):
                self.letterbox[k] = letters[j]

        self.add_list_entry(word)

    def undo_drop_word(self):
        self.drop_list_entry()
        self.run_list()

    def print_letter_box(self, original=False, highlight=None):
        """ Print out the grid """

        # TODO: Clean this up!
        BBLUE = '\033[1;36m'
        OKGREEN = '\033[92m'
        BRED = '\033[1;31m'
        DEFAULT = '\033[0m'

        count = 0
        print(" ")
        for i in range(int(self.n)):
            output = '{}'.format(BBLUE)
            start_count = count
            for j in range(int(self.n)):
                if original:
                    output += "{: >4} ".format(self.letterbox_original[count])
                else:
                    output += "{: >4} ".format(self.letterbox[count])

                count += 1

            if highlight is not None:
                count = start_count
                output += "      {}|{}   {} ".format(OKGREEN, OKGREEN, BBLUE)
                for j in range(int(self.n)):
                    if count in highlight:
                        output += "   {}{}{} ".format(
                            BRED, self.letterbox[count], BBLUE)
                    else:
                        output += "{: >4} ".format(self.letterbox[count])
                    count += 1

            print(output)

        print(" ")

        print DEFAULT

    def reset(self):
        """ Set the word grid back to original """

        self.letterbox = self.letterbox_original.copy()

    def find_specific_word(self, inword):
        """ Search for a specific word in the grid """

        if self.word_list is not None:
            if inword in self.word_list:
                return self.word_list[inword]

        word_list = self.find_words_from_letter(
            inword[0], word_length=len(inword), runfilter=False
        )
        if inword in word_list:
            return word_list[inword]

    def reset_all(self):
        """ Reset everything """

        self.reset()
        self.reset_list()

    def reset_list(self):
        """ Reset the dropped words list """

        self.repeat_list = []
        self.repeat_list_words = []

    def add_list_entry(self, new_word):
        """ Add an entry to the drop words list """

        if self.repeat_list is None:
            self.repeat_list = []
            self.repeat_list_words = []

        self.repeat_list.append(new_word)

    def drop_list_entry(self):
        """ Drop the last entry from the drop word list """

        self.repeat_list = self.repeat_list[:-1]
        self.repeat_list_words = self.repeat_list_words[:-1]

    def run_list(self, show_steps=False):
        """ Run the drop word list """

        self.reset()
        tlist = self.repeat_list[:]
        tlist_names = self.repeat_list_words[:]
        self.reset_list()
        for rep, word in zip(tlist,tlist_names):
            if show_steps:
                print("\n   {}{}{}".format(self.colors['BRED'], word,
                                           self.colors['DEFAULT']))
                self.print_letter_box(highlight=rep)
            self.drop_word(rep)

        if show_steps:
            self.print_letter_box()

    def print_word_grid(self, size=7):
        """ Print the found words in a grid """

        print ("\n")
        count = 0
        words = self.word_list.keys()
        words.sort()
        for name in words:
            count += 1
            if count < size:
                print name, "   ",
            else:
                print name
                count = 0
        print ("\n")

    def get_word_list(self):
        """ Return the found words """

        return self.word_list

    def list_operations(self):
        """ Print out a list of the current droped words """
        print(" ")
        for w, tw in zip(self.repeat_list, self.repeat_list_words):
            print("{}: {}".format(tw, w))
        print(" ")
