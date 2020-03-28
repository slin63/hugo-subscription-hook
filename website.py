# Checks if the website has new posts.
import requests
import pathlib


script_path = str(pathlib.Path(__file__).parent.absolute())
posts = script_path + "/posts.txt"
# WEBSITE = "https://www.chronicpizza.net/"
WEBSITE = "http://localhost:1313/"

# The title of every post contains one of this character.
# We can easily use it to count how many posts there are.
SPECIAL_CHAR = "•"

# Returns post names, from newest to oldest
def check_posts():
    r = requests.get(WEBSITE).text
    names = []
    post_idx = [i for i, ltr in enumerate(r) if ltr == SPECIAL_CHAR]
    for idx in post_idx:
        start = idx - 2
        end = r.find("</a>", start)
        names.append(r[start:end])

    return names


def get_posts():
    with open(posts) as file:
        return file.read()


def write_posts(s):
    with open(posts, "w") as file:
        file.write(s)
