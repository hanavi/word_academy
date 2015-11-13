#!/usr/bin/env python


import cheat
import pickle
import progressbar

counts = [5, 4, 9, 8, 10]
BOXID = 21

mybox = cheat.wordbox(boxid=BOXID)

k1 = None


def get_repeat_list(key):
    rlist = []
    if type(key) is tuple:
        for ent in key:
            # print(ent)
            k1 = eval(ent)
            rlist.append(k1)
    else:
        rlist.append(eval(key))

    return rlist


wl = {}
for i, count in enumerate(counts):

    print("")
    print("")
    print("Processing at Level: {}({})".format(i, count))
    print("")

    mybox.reset_all()
    if len(wl) == 0:
        b = progressbar.ProgressBar()
        b.start()
        mybox.find_words(count)
        word_list = mybox.get_word_list(as_dict=False)

        for ent in word_list:
            wl[str(ent)] = {}

        b.update(100)

    else:
        tot = len(wl)
        wl_new = {}
        d = 0
        b = progressbar.ProgressBar()
        b.start()
        for key in wl:
            d += 1
            p = d/tot*100

            if i % 100:
                b.update(p)
            rlist = get_repeat_list(key)
            # rlist = [rlist]
            # print(rlist)

            mybox.load_repeat_list(rlist)
            mybox.run_list()
            mybox.find_words(count)
            twl = mybox.get_word_list(as_dict=False)

            if len(twl) != 0:
                for ent in twl:
                    new_key = []
                    if type(key) is tuple:
                        for k0 in key:
                            new_key.append(k0)
                        new_key.append(str(ent))
                        wl_new[tuple(new_key)] = {}
                    else:
                        wl_new[key, str(ent)] = {}
            mybox.undo_drop_word()

        wl = wl_new


def convert(rlist):
    ret = []
    for key in rlist:
        k = eval(key)
        ret.append(k)
    return ret


print("\n\nFound {} matches\n".format(len(wl)))

mybox.reset_all()

if len(wl) > 0:
    y = [key for key in wl]
    for y0 in y:
        mybox.load_repeat_list(convert(y0))
        print("-------------------------------------")
        mybox.list_operations()
        mybox.run_list()
        print("-------------------------------------")


fd = open("tmpout.dat", 'wb')
pickle.dump(wl, fd)
fd.close()
