import sheets
import pathlib
import emails
import website

# Create any state that we might be missing
pathlib.Path(emails.email_list).touch()
pathlib.Path(website.posts).touch()

# Checks Google Sheets to get a list of subscribers
PATH = str(pathlib.Path(__file__).parent.absolute())
SUBSCRIBERS = PATH + "/subs.txt"
subscribers, sheet = sheets.get_subscribers()

# Check our email for a list of unsubscribers and cull them from our list
unsubscribes = emails.get_unsubscribes()
sheets.remove_subscribers(unsubscribes, sheet)
print(f"Unsubscribers: {unsubscribes}")

# Check of our website has changed at all and update our post count
current_posts = set(website.check_posts())
previous_posts = set(website.get_posts().split("\n"))
website.write_posts("\n".join(current_posts))
new_posts = current_posts.difference(previous_posts)

if new_posts:
    print(f"New posts! {new_posts}")
