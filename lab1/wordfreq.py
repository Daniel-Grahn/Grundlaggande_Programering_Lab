def countWords(words:list, stopWords:list) -> dict:
  count_words_dict:dict = {}
  
  word_set = set(words)
  
  for word in word_set:
    if(word in stopWords):
      continue
    
    count_words_dict.setdefault(word, words.count(word))
      
  return count_words_dict