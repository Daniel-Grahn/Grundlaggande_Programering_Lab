import sys
import wordfreq
import urllib.request
from collections.abc import Iterator
def read_from_web_gen(url: str):
    '''
    ### This is a Text-Generator
    
    The function takes an url as an argument 
    than, insteed of reading the entier text 
    it "returns" every line as a string.    
    '''

    response = urllib.request.urlopen(url)
    lines = response.read().decode("utf8").splitlines()
    
    return lines

def isurl(url):
    return url.lower().startswith("https://") or url.lower().startswith("http://")
def main():
    stop_words = "C:\Users\Thor\Documents\GitHub\Grundlaggande_Programering_Lab\lab1\eng_stopwords.txt"
    url = "https://www.gutenberg.org/files/15/15-0.txt"
    if isurl(url):
        inp_file = read_from_web_gen(url)
    else:
        with open(sys.argv[1], encoding="utf-8") as file:
            inp_file = file.readlines()
    with open(stop_words, encoding="utf-8") as stop_file:
        stop_words = stop_file.readlines()

    number = 5
    newlist = []
    for line in inp_file: 
        newlist.append(line.strip('\n'))
    tokens = wordfreq.tokenize(newlist)
    count_words_dict = wordfreq.countWords(tokens, stop_words)
    wordfreq.printTopMost(count_words_dict, number)

main()