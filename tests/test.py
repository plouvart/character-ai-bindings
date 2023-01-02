from character_ai_bindings.chatroom import ChatRoomServer

# TODO:
# - use pytest
# - unit testing
def test():
    server = ChatRoomServer(
        username = input("Username: "),
        password = input("Password: "),
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
        glados.ask("Ok")#Wanna do some science stuff together, GLaDOS?"),
    )
    print(
        "Steve's response:",
        steve.ask("Ok")#Found any diamonds today, Steve?"),
    )

    # Delete the chatrooms
    glados.delete()
    steve.delete()

if __name__ == "__main__":
    test()
    print("Test Successful!")

