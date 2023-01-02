# character-ai-bindings

## Description

Small API to access character ai chatrooms directly from Python

This API uses selenium to interact with character.ai and
provides simple methods to send user text and receive AIs answers!


## Requirements

You need to have Chrome or Chromium installed somewhere where the undetected\_chromedriver library
can easily find it.
You also need [Poetry](https://python-poetry.org/) to easily download dependencies and build a python wheel
that you can install with pip (see next section)

## Installation

This project uses poetry to easilly build and package the library.

To build this project into a python wheel you can install you must first have [Poetry](https://python-poetry.org/).
Then you must build the project from within the root folder after having cloned the repository.

```bash
git clone https://github.com/plouvart/character-ai-bindings
cd character-ai-bindings
poetry build
```

Once built, the python wheel will be available in the dist/ folder
To install it, just do:

```bash
pip install dist/character_ai_bindings-0.1.0-py3-none-any.whl
```

I may host the project on pypi if enough people are interested :)

## Usage

Here's a short code snippet demonstrating how to use the API.
You need an account at character.ai

```python
from character_ai_bindings.chatroom import ChatRoomServer

server = ChatRoomServer(
	username = "mr_kitty_cat",
	password = "p@ssw0rd",
)

# Instantiate a chatroom with GLaDOS and Steve AIs
# You need to use the url of the chatroom on character.ai website
glados = server.create_chatroom(
	chatroom_name = "GLaDOS",
	url = "https://beta.character.ai/chat?char=uqNQFjKGz4wbqj6A2XoNjrWUq0yQQdKgHkI92aZxsxA",
)
steve = server.create_chatroom(
	chatroom_name = "Steve",
	url = "https://beta.character.ai/chat?char=if4F8RpPbbzyez8M39tO6FCBmadFaDQdhzKRezAYfi0",
)

# Ask them a question
print(
	"Glados response:",
	glados.ask("Wanna do some science stuff together, GLaDOS?"),
)
print(
	"Steve's response:",
	steve.ask("Found any diamonds today, Steve?"),
)

# Delete the chatrooms
glados.delete()
steve.delete()
```

Next is up to you!
You may even have characters speak with each other if you want to :p

## Limitations

- May fail without much debug info
- Slow. But that's because character.ai may not be easily accessed with a bot

## Credits

- character.ai devs
- poetry devs
- selenium devs
- undetected\_chromedriver devs
