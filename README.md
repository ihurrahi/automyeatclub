# automyeatclub
Orders a meal from myeatclub.com

Depends on selenium webdriver

Looks at your order history and orders the highest rated meal you haven't ordered before, as well as any other parameters you pass the script.

Put your myeatclub cookies in a json file that looks like:
```
{
  "sessionid": "<sessionid>",
  "csrftoken": "<csrftoken>"
}
```
These can be found by inspecting your cookies after logging in once.

```
usage: myeatclub.py [-h] [--avoid-tag AVOID_TAG] [--require-tag REQUIRE_TAG]
                    [--avoid-restaurant AVOID_RESTAURANT] [--place-order]
                    [--preserve-browser] [--menu-number MENU_NUMBER]
                    [--cookies-path COOKIES_PATH]

optional arguments:
  -h, --help            show this help message and exit
  --avoid-tag AVOID_TAG
  --require-tag REQUIRE_TAG
  --avoid-restaurant AVOID_RESTAURANT
  --place-order
  --preserve-browser
  --menu-number MENU_NUMBER
  --cookies-path COOKIES_PATH
```
