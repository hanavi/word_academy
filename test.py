#!/usr/bin/env python

import unittest

from boxes import boxes
import cheat


class TestCheatBoxes(unittest.TestCase):

    def setUp(self):

        self.cheat = cheat.wordbox(boxid=0)
        self.cheat.load_dictionary()

    def test_neighbors(self):

        actual_neighbor = {}
        actual_neighbor[0] = set([1, 6, 7])
        actual_neighbor[1] = set([0, 2, 7, 6, 8])
        actual_neighbor[2] = set([1, 3, 8, 7, 9])
        actual_neighbor[3] = set([2, 4, 9, 8, 10])
        actual_neighbor[4] = set([3, 5, 10, 9, 11])
        actual_neighbor[5] = set([4, 11, 10])
        actual_neighbor[6] = set([7, 12, 0, 13, 1])
        actual_neighbor[7] = set([8, 6, 13, 1, 14, 2, 12, 0])
        actual_neighbor[8] = set([9, 7, 14, 2, 15, 3, 13, 1])
        actual_neighbor[9] = set([10, 8, 15, 3, 16, 4, 14, 2])
        actual_neighbor[10] = set([11, 9, 16, 4, 17, 5, 15, 3])
        actual_neighbor[11] = set([10, 17, 5, 16, 4])
        actual_neighbor[12] = set([13, 18, 6, 19, 7])
        actual_neighbor[13] = set([14, 12, 19, 7, 20, 8, 18, 6])
        actual_neighbor[14] = set([15, 13, 20, 8, 21, 9, 19, 7])
        actual_neighbor[15] = set([16, 14, 21, 9, 22, 10, 20, 8])
        actual_neighbor[16] = set([17, 15, 22, 10, 23, 11, 21, 9])
        actual_neighbor[17] = set([16, 23, 11, 22, 10])
        actual_neighbor[18] = set([19, 24, 12, 25, 13])
        actual_neighbor[19] = set([20, 18, 25, 13, 26, 14, 24, 12])
        actual_neighbor[20] = set([21, 19, 26, 14, 27, 15, 25, 13])
        actual_neighbor[21] = set([22, 20, 27, 15, 28, 16, 26, 14])
        actual_neighbor[22] = set([23, 21, 28, 16, 29, 17, 27, 15])
        actual_neighbor[23] = set([22, 29, 17, 28, 16])
        actual_neighbor[24] = set([25, 30, 18, 31, 19])
        actual_neighbor[25] = set([26, 24, 31, 19, 32, 20, 30, 18])
        actual_neighbor[26] = set([27, 25, 32, 20, 33, 21, 31, 19])
        actual_neighbor[27] = set([28, 26, 33, 21, 34, 22, 32, 20])
        actual_neighbor[28] = set([29, 27, 34, 22, 35, 23, 33, 21])
        actual_neighbor[29] = set([28, 35, 23, 34, 22])
        actual_neighbor[30] = set([31, 24, 25])
        actual_neighbor[31] = set([30, 32, 25, 24, 26])
        actual_neighbor[32] = set([31, 33, 26, 25, 27])
        actual_neighbor[33] = set([32, 34, 27, 26, 28])
        actual_neighbor[34] = set([33, 35, 28, 27, 29])
        actual_neighbor[35] = set([34, 29, 28])

        for i in range(36):
            self.assertEqual(actual_neighbor[i],
                             set(self.cheat.get_neighbors(i)))

    def test_get_words(self):

        words_check_1 = self.cheat.get_words(0,3)
        words_check_2 = self.cheat.get_words(5,3)
        words_check_3 = self.cheat.get_words(10,5)




if __name__ == '__main__':
    unittest.main()
