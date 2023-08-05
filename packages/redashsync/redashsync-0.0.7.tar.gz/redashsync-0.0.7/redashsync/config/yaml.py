import yaml

class Config:
    def __init__(self, filePath):
        with open(filePath, encoding='UTF-8') as f:
            self.raw = yaml.load(f,  Loader=yaml.FullLoader)

    def getRedashHost(self):
        return self.raw['redash_configs']['url']

    def getQueryApiKey(self):
        return self.raw['redash_configs']['query_api_key']

    def getSlackBotToken(self):
        return self.raw['slack_configs']['slack']['token']

    def getQueryId(self):
        return self.raw['redash_configs']['queries'][0]['query_id']
    