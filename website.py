# Checks if the website has new posts.
import requests
import pathlib


script_path = str(pathlib.Path(__file__).parent.absolute())
post_count = script_path + "/post_count.txt"
# WEBSITE = "https://www.chronicpizza.net/"
WEBSITE = "http://localhost:1313/"
# The title of every post contains one of this character.
# We can easily use it to count how many posts there are.
SPECIAL_CHAR = "•"

def check_post_count():
    r = requests.get(WEBSITE)
    return r.text.count(SPECIAL_CHAR)

def get_post_count():
    with open(post_count) as file:
        s = file.read()
    return int(s)

def write_post_count(c):
     with open(post_count, "w") as file:
        file.write(str(c))

x = check_post_count()
z = get_post_count()
print(z)
write_post_count(x)
