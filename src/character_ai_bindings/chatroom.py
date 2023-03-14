from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from pathlib import Path
import undetected_chromedriver as uc

""" ChatRoom Module

This is a module that provide a ChatRoomServer object that allows to connect
to character.ai.
The user can use this object to create ChatRoom objects and then use those to 
easily interact with the ai without the need for a browser.

You SHOULD NOT try to use the ChatRoomServer object directly to dialog, but instead use
ChatRoom objects you create with it.
Here's a simple example:

```python


# Create a chatroom server
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


"""



class ChatRoomServer:
    def __init__(self, username, password, verbose=False):
        options = uc.ChromeOptions()
        options.headless=True
        options.add_argument('--headless')
        options.add_argument("--disable-popup-blocking");
        self.driver = uc.Chrome(options=options)
        self.driver.get("https://beta.character.ai/")

        # Close stupid character.ai popup
        try:
            elem = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="#AcceptButton"]'))
            )
        except:
            raise Exception("Couldn't close popup")
        element = self.driver.find_element(By.XPATH, '//*[@id="#AcceptButton"]')
        element.click()
        sleep(1)

        # Open logging popup
        try:
            elem = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[2]/div/div/div/div/div[1]/div[2]/a[4]/button"))
            )
        except:
            raise Exception("Could not open logging popup")
        element = self.driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div/div/div/div/div[1]/div[2]/a[4]/button")
        element.click()
        sleep(1)

        # Click logging button
        try:
            elem = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/div[3]/div/div[1]/div/div/div/div/div[3]/div/button"))
            )
        except:
            raise Exception("Could not open logging page")
        element = self.driver.find_element(By.XPATH, "/html/body/div[3]/div/div[1]/div/div/div/div/div[3]/div/button")
        element.click()
        sleep(1)

        try:
            elem = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, """//*[@id="username"]""")) #This is a dummy element
            )
        except:
            raise Exception("Could not open logging page")

        # Enter informations
        self.driver.find_element(By.XPATH, """//*[@id="username"]""").send_keys(username)
        sleep(0.5)
        self.driver.find_element(By.XPATH, """//*[@id="password"]""").send_keys(password)
        sleep(0.5)
        self.driver.find_element(By.XPATH, """/html/body/div/main/section/div/div/div/form/div[2]/button""").click()
        sleep(0.5)

        # TODO verify connection worked

        self.chatrooms = dict()
        self.current_chatroom = None
        if verbose:
            print("Ready to start chatting!")

    def create_chatroom(
        self, 
        chatroom_name: str,
        url: str,
    ) -> "ChatRoom":
        # Try to mitigate injection problems
        if "\"" in url:
            raise Exception("Invalid character \" found in url")
        self.driver.execute_script("window.open('');")

        WebDriverWait(self.driver, 10).until(EC.number_of_windows_to_be(len(self.chatrooms) + 2))
        sleep(0.2)

        self.chatrooms[chatroom_name] = self.driver.window_handles[-1]
        self.driver.switch_to.window(self.driver.window_handles[-1])
        sleep(0.2)
        self.driver.get(url)
        sleep(1)

        return ChatRoom(
            name = chatroom_name, 
            server = self,
        )

    def delete_chatroom(
        self, 
        chatroom_name: str,
    ):
        if chatroom_name not in self.chatrooms:
            raise Exception(f"Chatroom \"{chatroom_name}\" does not exist, can't delete it!")
        if self.current_chatroom != chatroom_name:
            self.switch_chatroom(chatroom_name)
        self.driver.close()
        del self.chatrooms[chatroom_name]
        self.current_chatroom = None
    
    def switch_chatroom(
        self, 
        chatroom_name: str,
    ):
        if self.current_chatroom == chatroom_name:
            # Already in the required chatroom
            return
        if chatroom_name not in self.chatrooms:
            raise Exception(f"Chatroom \"{chatroom_name}\" does not exist, can't switch to it!")
        self.driver.switch_to.window(
            self.chatrooms[chatroom_name]
        )
        sleep(0.1)
        try:
            elem = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, """//*[@id="user-input"]"""))
            )
        except:
            raise Exception(f"Failed to switch to chatroom {chatroom_name}")
        self.current_chatroom = chatroom_name

    def ask_chatroom(
        self, 
        question: str,
        chatroom_name: str,
    ):
        self.switch_chatroom(chatroom_name)

        self.driver.find_element(By.XPATH, """//*[@id="user-input"]""").send_keys(question)
        self.driver.find_element(By.XPATH, """/html/body/div[1]/div[2]/div/div[3]/div/div/form/div/div/div[2]/button[1]""").click()
        sleep(0.1)

        elem = None
        for i in range(3):
            try:
                elem = WebDriverWait(self.driver, 30).until(
                    EC.presence_of_element_located((By.XPATH, """//*[@id="root"]/div[2]/div/div[3]/div/div/form/div/div/div[2]/button[1]"""))
                )
            except:
                pass
        if elem is None:
            raise Exception("The AI is unresponsive!")
            sys.exit()

        while self.driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div/div[3]/div/div/form/div/div/div[2]/button[1]").get_attribute("disabled") is not None:
            sleep(0.1)

        return self.driver.find_element(By.XPATH, """//*[@id="scrollBar"]/div/div/div[2]/div[2]/div[1]/div[1]/div/div[2]/div/div/div/div[1]/div[1]/div/p""").text

    # TODO, only works correctly when the ai is not currently writing!
    # TODO, must scroll to get all messages
    def get_chatroom_ai_history(
        self,
        chatroom_name: str,
    ) -> list[str]:
        self.switch_chatroom(chatroom_name)
        elem = self.driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div/div[2]/div/div/div/div[1]/div/div/div")
        messages = elem.find_elements(By.CLASS_NAME, "msg")
        ai_messages = [
            msg
            for msg_elem in msg_elems[::2]
            if len(msg := msg_elem.text)
        ]
        return ai_messages

    # TODO, only works correctly when the ai is not currently writing!
    # TODO, must scroll to get all messages
    def get_chatroom_user_history(
        self,
        chatroom_name: str,
    ) -> list[str]:
        self.switch_chatroom(chatroom_name)
        elem = self.driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div/div[2]/div/div/div/div[1]/div/div/div")
        msg_elems = elem.find_elements(By.CLASS_NAME, "msg")
        user_messages = [
            msg
            for msg_elem in msg_elems[1::2]
            if len(msg := msg_elem.text)

        ]
        return user_messages

    def __del__(self):
        self.driver.quit()


class ChatRoom:
    def __init__(
        self,
        name: str,
        server: ChatRoomServer,
    ):
        """ ChatRoom Initializer

        Initializes a ChatRoom with a name and a ChatRoomServer object
        
        Don't create a ChatRoom yourself!
        Use ChatRoomServer.create_chatroom method to get a new ChatRoom.
        """
        self.name = name
        self.server = server

    def ask(
        self,
        question: str,
    ) -> "ChatRoom":
        """ Ask

        Send a message to the AI.
        Return its answers.
        """
        return self.server.ask_chatroom(question, self.name)

    def get_ai_history(self) -> list[str]:
        """ Get AI History

        return a list of the posts made by AI.
        LIMITATIONS:
            - only the first few latest posts are accessible.
            - the AI must not be currently writing something when this is called
        TODO: get all posts by simulating scrolling of the chat
        """
        return self.server.get_chatroom_ai_history(self.name)

    def get_user_history(self) -> list[str]:
        """ Get User History

        return a list of the posts made by User.
        LIMITATIONS:
            - only the first few latest posts are accessible.
            - the AI must not be currently writing something when this is called
        TODO: get all posts by simulating scrolling of the chat
        """
        return self.server.get_chatroom_user_history(self.name)
        
    def delete(
        self,
    ):
        """ Delete

        Remove the chatroom from the server.
        It does not delete the chat. It just closes the chatroom tab on the server.
        Reopening it will still have the messages.
        """
        self.server.delete_chatroom(self.name)


