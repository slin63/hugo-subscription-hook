import sheets
import pathlib
import emails
import website

# Create any state that we might be missing
pathlib.Path(emails.email_list).touch()
pathlib.Path(website.posts).touch()

# Checks Google Sheets to get a list of subscribers
print("[subhook]: Getting subscribers...")
PATH = str(pathlib.Path(__file__).parent.absolute())
SUBSCRIBERS = PATH + "/subs.txt"
subscribers, sheet = sheets.get_subscribers()
subscribers = set(subscribers)
print(f"[subhook]: Getting subscribers... Done! {len(subscribers)} subscribers.")

# Check our email for a list of unsubscribers and cull them from our list
print("[subhook]: Getting unsubscribes...")
unsubscribes = set(emails.get_unsubscribes())
sheets.remove_subscribers(unsubscribes, sheet)
subscribers.difference_update(unsubscribes)
if unsubscribes:
    print(f"Unsubscribers: {unsubscribes}")
print("[subhook]: Getting unsubscribes... Done!")

# Check of our website has changed at all and update our post count
print("[subhook]: Checking website for changes...")
current_posts = set(website.check_posts())
previous_posts = set(website.get_posts().split("\n"))
website.write_posts("\n".join(current_posts))
new_posts = list(current_posts.difference(previous_posts))
print(f"[subhook]: Checking website for changes... Done! {len(new_posts)} new posts.")

# Email subscribers
if new_posts:
    post_str = ""
    for p in new_posts:
        post_str += f" - {p}\n"
    print("[subhook]: E-mailing subscribers...")
    header = f"[chron·ic·piz·za]: {new_posts[0]}"
    body = f"""
New posts @ https://www.chronicpizza.net !

{post_str}

Respond to this email with anything to unsubscribe.
"""
    emails.send_emails(
        targets=subscribers, header=header, body=body,
    )
    print("[subhook]: E-mailing subscribers... Done!")
