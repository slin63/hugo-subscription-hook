# hugo-subscription-hook

Lightweight hacky subscription form and subscription notifications for my Hugo website, www.chronicpizza.net

Everything is being run on my tiny Raspberry Pi.

## Setup
`source ./.env && python3.7 bot.py`


## Overview

### Subscribing
1. A user submits their email through an HTML form that is targeted towards a Google Form, which outputs information to a Google Sheet. Thanks to [developerdrive](https://www.developerdrive.com/add-google-forms-static-site/) here.
```html
<form action="<google-form-response-url>" method="post">
    <input type="email" placeholder="your email" name="emailAddress" required>
        <button type="submit">subscribe</button>
    </form>
</div>
```

2. An automated script periodically checks Google Sheets to get a list of subscribers. Thanks to [towardsdatascience](https://towardsdatascience.com/accessing-google-spreadsheet-data-using-python-90a5bc214fd2).

4. Another automated script curls my website and looks for changes.

5. If it detects any changes, it notifies the list of subscribers.

### Unsubscribing
1. A user replies to a standard subscription email
2. A script sees this reply and removes the user from the list of subscribers.

https://docs.google.com/spreadsheets/d/1RDugEZOMz_hfKXvz-BHu-7z2TkCsGHmT9gBduccmdgE/edit#gid=2045959944
https://docs.google.com/forms/d/13d6y2Pt9dr0pVVsEi6JJR4Waii3tONyzMZOZGUPq8to/edit?usp=forms_home&ths=true
