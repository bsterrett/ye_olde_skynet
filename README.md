Ye Olde Skynet
============

A bot to do simple tasks in the game Travian.


Overview
------------

Skynet works in three parts: the browser, the Selenium server, and the ~~neoneurocorticum~~ conductor. The conductor decides what high level actions to take, like launching a wave of raids, and maps actions to a series of low level behaviors, like clicking. The Selenium server takes these low level behaviors, maps them to browser-specific instructions, and sends them to the browser, while passing information about the current state of the browser back to the conductor. The browser executes instructions it receives from the Selenium server while sending and receiving information to and from Travian through the internet.


Features
------------

Skynet only has the ability to send a single wave of raids, but more features are planned. You can look forward to:

- Scheduled events
- Repeating events
- Build queue
- Intelligent raid balancing
- Hero resource bonus balancing
- Resource upgrade recommender


Installation
------------

Before you can use Skynet, you will need to:
- Install the dependencies listed below
- Download this repository
- Configure a secrets.json (described below)


Dependencies
------------

Skynet will automatically install all of its own dependencies except these:
- [virtualenv](https://virtualenv.pypa.io/en/stable/installation/ "Installing virtualenv")
- [java](https://java.com/en/download/help/download_options.xml "Installing Java")
- [Firefox](https://www.mozilla.org/firefox/new/ "Installing Firefox")
- [geckodriver](https://github.com/mozilla/geckodriver/releases/latest "Downloading geckodriver")


Install all of these on your system and add them to your PATH. Each time Skynet is run, it will use virtualenv to check for and install its own Python 3 interpreter and modules, if necessary.


secrets.json
------------

```json
{
  "base_url": "https://ts0.travian.us/",
  "username": "example_travian_user",
  "password": "example_travian_password"
}
```


Usage
------------

In order to use Skynet, run:
```bash
./skynet.sh
```


