def is_anagram(word1, word2):
    new_word1 = sorted(word1)
    new_word2 = sorted(word2)
    print(new_word1, new_word2)
    return new_word1 == new_word2

print(is_anagram('tachymetric', 'mccarthyite'))
print(is_anagram('post', 'top'))
print(is_anagram('pott', 'top'))
print(is_anagram('top', 'post'))
print(is_anagram('topss', 'postt'))

%timeit is_anagram('tops', 'spot')

