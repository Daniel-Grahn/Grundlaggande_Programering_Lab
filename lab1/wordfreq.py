def tokenize(document: list[str]):
    token = []
    for line in document:
        # print(line.split())
        
        if(len(line) == 0):
            continue
        
        for w in line.split():
            word = w.lower()
            
            word_holder = ""
            for i in range(0, len(word)):
                char = word[i]
                valid = True
                
                #valedering
                letter = word[i]
                
                if (not valid):    
                    token.append(word_holder)
                    word_holder = letter
                    break
                else:
                    word_holder+=letter

            # print(word, lower_word) 
        
    return token


print("result:", tokenize(['This is a simple, sentence']))