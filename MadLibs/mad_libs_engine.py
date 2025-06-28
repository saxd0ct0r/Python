# Timothy Owen
# 26 June 2025
# Opens a .mlb file, which is a text file with select words delimited for
# substitution. The user is prompted by the script to provide a word based on 
# the part of speech to be replaced. After all the file is processed, the user
# then gets to read the story, to humorous effect.

def article(word):
    return 'an ' if word[0].lower() in 'aeiou' else 'a '

new_story = ""
# filename = input("Enter name of Mad Lib file:")
filename = "amusement_parks.mlb"
my_madlib = open("c:/VSC/Python/MadLibs/" + filename, "r")
for line in my_madlib:
    while len(line) > 0:
        if "__" in line:
            dunder_position = line.index("__")
            if "a/an" in line[:dunder_position]:
                article_index = line.index("a/an")
                new_story += line[:article_index]
            else:
                article_index = None
                new_story += line[:dunder_position]
            dunder_end = line.index("__", dunder_position + 2)
            word_prompt = line[dunder_position + 2:dunder_end]
            prompt_article = article(word_prompt)
            word_prompt = prompt_article + word_prompt
            word = input(f"Tell me {word_prompt}: ")
            word_article = "" if article_index == None else article(word)
            word = word_article + word
            new_story += word
            line = line[dunder_end + 2:]
        else:
            # print(line)
            new_story += line
            line = ""
    # if "a/an" in line or "__" in line:
    #     print(f"Something to replace")
    # print(line, end="")
    # new_story += line

print("\n\n")
print(new_story)
my_madlib.close()