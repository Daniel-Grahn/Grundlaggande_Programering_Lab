import urllib.request
from collections.abc import Iterator

URL = "http://www.gutenberg.org/files/15/15-0.txt"
def read_from_web_gen(url: str):
    '''
    ### This is a Text-Generator
    
    The function takes an url as an argument 
    than, insteed of reading the entier text 
    it "returns" each line at a time as a string.    
    '''

    response = urllib.request.urlopen(url)
    lines = response.read().decode("utf8").splitlines()
    
    for line in lines:
        yield str(line)

def print_text_from_web(url):
    text_gen = read_from_web_gen(url)
    for text in text_gen:
        print(text)
    else:
        text_gen.close()
        print("Done.")

print_text_from_web(URL)