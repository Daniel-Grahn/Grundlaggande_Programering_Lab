import urllib.request
import sys

def read_from_web():
    url= "http://www.gutenberg.org/files/15/15-0.txt"
    response = urllib.request.urlopen(url)
    # response = urllib.request.urlopen(sys.argv[2])
    lines = response.read().decode("utf8").splitlines()
    print(lines)
    
read_from_web()