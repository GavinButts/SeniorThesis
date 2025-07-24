

## BRUHAT ORDER
def bruhat_order(word):

    frequency = getCharFrequency(word)
    
    frequency_1, t_1 = dominatingFunction(frequency, 1, word)
    frequency_12, t_12 = dominatingFunction(frequency_1, 2, t_1)
    _, t_121 = dominatingFunction(frequency_12, 1, t_12)

    frequency_2, t_2 = dominatingFunction(frequency, 2, word)
    frequency_21, t_21 = dominatingFunction(frequency_2, 1, t_2)
    _, t_212 = dominatingFunction(frequency_21, 2, t_21)

    display_tree([word, t_1, t_2, t_12, t_21, t_121, t_212])





## PEICEWISE DEFINITION
def dominatingFunction(charFrequency, transposeNum, word):

    if charFrequency[transposeNum-1] > charFrequency[transposeNum]:
        return forwardDominating(transposeNum, word)
    
    elif charFrequency[transposeNum-1] < charFrequency[transposeNum]:
        return reverseDominating(transposeNum, word)
    
    elif charFrequency[transposeNum-1] == charFrequency[transposeNum]:
        return charFrequency, word
    


def forwardDominating(transposeNum, word):
    n = len(word)
    word = [int(c) for c in word]  # Convert to integers
    wordExt = word + word
    countWindow = n * [0]
    dominanceWindow = n * [True]

    # Relabel: a → 1, a+1 → -1, else → 0
    for index, elem in enumerate(wordExt):
        if elem == transposeNum:
            wordExt[index] = 1
        elif elem == transposeNum + 1:
            wordExt[index] = -1
        else:
            wordExt[index] = 0

    for i in range(n):
        countWindow = [x + y for x, y in zip(countWindow, wordExt[i:i + n])]
        dominanceWindow = [a and b for a, b in zip(dominanceWindow, [x > 0 for x in countWindow])]

    newWordList = [x + int(y) for x, y in zip(word, dominanceWindow)]
    newWordStrings = [str(num) for num in newWordList]
    newWord = "".join(newWordStrings)

    return getCharFrequency(newWord), newWord


def reverseDominating(transposeNum, word):
    n = len(word)
    word = [int(c) for c in word]  # Convert to integers
    wordExt = word + word
    countWindow = n * [0]
    dominanceWindow = n * [True]

    # Relabel: a+1 → 1, a → -1, else → 0
    for index, elem in enumerate(wordExt):
        if elem == transposeNum + 1:
            wordExt[index] = 1
        elif elem == transposeNum:
            wordExt[index] = -1
        else:
            wordExt[index] = 0

    for i in range(n):
        rev_window = wordExt[i:i + n][::-1]
        countWindow = [x + y for x, y in zip(countWindow, rev_window)]
        dominanceWindow = [a and b for a, b in zip(dominanceWindow, [x > 0 for x in countWindow])]

    newWordList = []
    for i in range(n):
        if dominanceWindow[i] and word[i] == transposeNum + 1:
            newWordList.append(word[i] - 1)
        else:
            newWordList.append(word[i])

    newWordStrings = [str(num) for num in newWordList]
    newWord = "".join(newWordStrings)

    return getCharFrequency(newWord), newWord



def getCharFrequency(word):
    freq = [0,0,0]
    for char in word:
        charValue = int(char)
        
        if charValue > 3:
            print(f"Not valid word; the number {charValue} is not allowed.")
            return [0,0,0]
        
        else:
            freq[charValue-1] += 1

    return freq


def display_tree(strings):
    if len(strings) != 7:
        raise ValueError("Expected exactly 7 strings")

    nodes = [f"[{s}]" for s in strings]
    max_len = max(len(n) for n in nodes)
    padded = [s.center(max_len) for s in nodes]

    root = padded[0]
    l1, r1 = padded[1], padded[2]
    l2, r2 = padded[3], padded[4]
    l3, r3 = padded[5], padded[6]

    node_gap = max_len + 4
    total_width = 2 * max_len + node_gap

    
    def line(l, r):
        return f"{l}{' ' * node_gap}{r}".center(total_width)


    print("\n\n")
    print("Bruhat Order Diagram:".center(total_width))
    print("\n")
    print(root.center(total_width))
    

    slash_line = f"/{' ' * (node_gap - 2)}\\".center(total_width)
    print(slash_line)

    
    print(line(l1, r1))
    print(line('|'.center(max_len), '|'.center(max_len)))
    print(line(l2, r2))
    print(line('|'.center(max_len), '|'.center(max_len)))
    print(line(l3, r3))

    print("\n\n\n")




#### MAIN

word = input("Please input word : \n")

bruhat_order(word)





