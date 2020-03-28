import sheets

subscribers, sheet = sheets.get_subscribers()
print(subscribers)
sheets.remove_subscribers(["shean.lin2018@gmail.com", "test@gm.com"], sheet)
