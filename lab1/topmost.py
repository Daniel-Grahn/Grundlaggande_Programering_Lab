import sys
import wordfreq

def main():
    with open(sys.argv[1], encoding="utf-8") as file:
        inp_file = file.readlines()

    with open(sys.argv[2], encoding="utf-8") as stop_file:
        stop_words = stop_file.readlines()

    number = int(sys.argv[3]) 
    newlist = []
    for line in inp_file: 
        newlist.append(line.strip('\n'))
    tokens = wordfreq.tokenize(newlist)
    count_words_dict = wordfreq.countWords(tokens, stop_words)
    wordfreq.printTopMost(count_words_dict, number)

main()