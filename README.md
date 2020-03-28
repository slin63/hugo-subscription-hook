# hugo-subscription-hook

Lightweight hacky subscription form and subscription notifications for my Hugo website, www.chronicpizza.net

Everything is being run on my tiny Raspberry Pi

## Subscribing
1. x A user submits their email through an HTML form that is targeted towards a Google Form, which outputs information to a Google Sheet. Thanks to [developerdrive](https://www.developerdrive.com/add-google-forms-static-site/) here.
```html
<form action="<google-form-response-url>" method="post">
    <input type="email" placeholder="your email" name="emailAddress" required>
        <button type="submit">subscribe</button>
    </form>
</div>
```

2. x An automated script periodically checks Google Sheet and checks for new subscribers. Thanks to [towardsdatascience](https://towardsdatascience.com/accessing-google-spreadsheet-data-using-python-90a5bc214fd2).

3. Subscribers are added to a text file.

4. Another automated script curls my website and looks for changes.

5. If it detects any changes, it notifies the list of subscribers.

## Unsubscribing
1. A user replies "unsubscribe" to a standard subscription email

2. An automated script periodically checks its email inbox and removes emails from the subscribe sheet as needed
