
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
          
def countWords(words:list, stopWords:list) -> dict:
  count_words_dict:dict = {}
  word_set = set(words)
  
  for word in word_set:
    if(word in stopWords):
      continue
    
    count_words_dict.setdefault(word, words.count(word))
      

  return count_words_dict

def printTopMost(frequences, n): 
    sorted_words = sorted(frequences.items(), key=lambda x: -x[1])

    for word, freq in sorted_words[:n]:
        print(word.ljust(20) + str(freq).rjust(5))

