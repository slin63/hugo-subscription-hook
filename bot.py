import sheets
import pathlib
import emails

# Checks Google Sheets to get a list of subscribers and cull users who have unsubscribed.
PATH = str(pathlib.Path(__file__).parent.absolute())
SUBSCRIBERS = PATH + "/subs.txt"

subscribers, sheet = sheets.get_subscribers()
unsubscribes = emails.get_unsubscribes()
sheets.remove_subscribers(unsubscribes, sheet)
print(f"Unsubscribers: {unsubscribes}")

