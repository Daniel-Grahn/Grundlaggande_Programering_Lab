
def tokenize(lines: list[str]):
    words = []

    for line in lines:
        start = 0

        while start < len(line):
            while start < len(line) and line[start].isspace():
                start += 1

            if start >= len(line):
                break
            end = start

            if line[end].isalpha():
                while end < len(line) and line[end].isalpha():
                    end += 1
            elif line[end].isdigit():
                while end < len(line) and line[end].isdigit():
                    end += 1
            else:
                end += 1
            words.append(line[start:end].lower())
            start = end 
    return words      
          
def countWords(words:list, rawStopWords:list) -> dict:
  """
    ## Count how many times each word occurs in a list.

    Words included in `rawStopWords` are excluded from the count. The
    stop words are stripped of newline characters before being compared
    with the words in `words`.

    ### Args:
        words: A list of words to count.
        rawStopWords: A list of stop words, which may contain newline
            characters (e.g. ``"the\\n"``).

    ### Returns:
        A dictionary mapping each word to the number of times it occurs
        in `words`, excluding the stop words.
    """
  
  stopWords = [n.strip("\n") for n in rawStopWords] 
  count_words_dict:dict = {}
  
  #Make a uniq list of words
  word_set = set(words)
  
  for word in word_set:
    #count the word if it is not in the stopWords
    if not (word in stopWords):
      count_words_dict.setdefault(word, words.count(word))
      
  return count_words_dict

def printTopMost(frequences, n): 
    sorted_words = sorted(frequences.items(), key=lambda x: -x[1])

    for word, freq in sorted_words[:n]:
        print(word.ljust(20) + str(freq).rjust(5))

