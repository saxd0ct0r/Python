# Timothy Owen
# 16 June 2025
'''
8.21 LAB: Word frequencies
Write a program that reads a list of words. Then, the program outputs those 
words and their frequencies (case insensitive).
    Ex: If the input is:
            hey Hi Mark hi mark
        the output is:
            hey 1
            Hi 2
            Mark 2
            hi 2
            mark 2
Hint: Use lower() to set each word to lowercase before comparing.
'''

user_input = input().split()
word_freq = {}
for word in user_input:
    word = word.lower()
    if word in word_freq:
        word_freq[word] += 1
    else:
        word_freq[word] = 1
    
for word in user_input:
    print(f"{word} {word_freq[word.lower()]}")

