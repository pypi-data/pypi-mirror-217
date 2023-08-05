from slack_sdk import WebClient
import requests


class Slack:
    def __init__(self, botToken):
        self.botToken = botToken
        self.client = WebClient(token=self.botToken)
    def sendFile(self, filePath, channelName, messageTitle, messageInitialComment):

        auth_test = self.client.auth_test()
        bot_user_id = auth_test["user_id"]
        print(f"App's bot user: {bot_user_id}")

        response = self.client.files_upload(
            channels=channelName,
            title=messageTitle,
            file=filePath,
            initial_comment=messageInitialComment,
        )

    def sendMessage(self, channelName, message):

        result = self.client.chat_postMessage(
            channel=channelName,
            text=message
        )




def sendMessageTest(tokenParameter, channelName):
    requests.post("https://slack.com/api/chat.postMessage",
                  headers={"Authorization": "Bearer " + tokenParameter},
                  data={"channel": channelName, "text": "```Test```"})

    