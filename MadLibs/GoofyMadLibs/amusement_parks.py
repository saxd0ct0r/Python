# Timothy Owen
# 25 June 2025
# Mad Libs Amusement Park rendered in a Python script
keywords = {1: ['noun'],
            2: ['article of clothing'],
            3: ['adjective'],
            4: ['adjective'],
            5: ['noun'],
            6: ['plural noun'],
            7: ['noun'],
            8: ['adjective'],
            9: ['type of food'],
            10:['type of liquid'],
            11:['part of the body'],
            12:['plural noun'],
            13:['plural noun'],
            14:['animal'],
            15:['noun']
            }

vowels = "aeiou"

def get_words(list_of_words):
    for each_word in list_of_words:
        word_to_get = keywords[each_word][0]
        indef_article = "an" if word_to_get[0] in vowels else "a"
        prompt = f"Tell me {indef_article} {word_to_get}: "
        keywords[each_word] = [word_to_get, input(prompt)]

def article(word):
    return 'an' if word[0] in vowels else 'a'

get_words(keywords)
story = f"An amusement park is always fun on a hot summer {keywords[1][1]}.\n\
When you get there, you can wear your {keywords[2][1]} and go\n\
for a swim. And there are lots of {keywords[3][1]} things to eat. You can\n\
start off with {article(keywords[4][1])} {keywords[4][1]}-dog on {article(keywords[5][1])} {keywords[5][1]} with\n\
mustard, relish, and {keywords[6][1]} on it. Then you can have a\n\
buttered ear of {keywords[7][1]} with a nice {keywords[8][1]} slice of\n\
{keywords[9][1]} and a big bottle of cold {keywords[10][1]}. When you\n\
are full, it's time to go on the roller coaster, which should settle your\n\
{keywords[11][1]}. Other amusement park rides are the bumper cars,\n\
which have little {keywords[12][1]} that you drive and run into other\n\
{keywords[13][1]}, and the merry-go-round, where you can sit on a big\n\
{keywords[14][1]} and try to grab the gold {keywords[15][1]} as you ride past it."

print()
print(story)
