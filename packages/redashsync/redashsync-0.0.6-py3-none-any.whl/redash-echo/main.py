from redash.data import *
from slack.messages import *
from config.yaml import *
from datetime import datetime
from cron_converter import Cron


def run1():
    config = Config("./resource/sample.yml")
    redashHost = config.getRedashHost()
    redashQueryKey = config.getQueryApiKey()
    redashQueryId = config.getQueryId()
    slackBotToken = config.getSlackBotToken()

    redash = Redash(redashHost)
    slack = Slack(slackBotToken)

    cron = Cron()
    cron.from_string("*/1 * * * *")
    referenceTime = datetime.now()
    schedule = cron.schedule(referenceTime)
    expectedTime = schedule.next().isoformat()

    while True:
        if(expectedTime == datetime.now().isoformat()[0:19]):
            print(expectedTime)
            expectedTime = schedule.next().isoformat()

            response = redash.getQueriesFromRedash(redashQueryId, redashQueryKey)
            result = redash.getColumnData(response, ['Open', 'Close'])
            template = "*시가* : %s \n*종가* : %s \n"
            result = redash.getMarkdown(template, result[0:5], 2)

            slack.sendMessage("#redash-echo", result)

def run2():
    config = Config("./resource/sample.yml")
    redashHost = config.getRedashHost()
    redashQueryKey = config.getQueryApiKey()
    redashQueryId = config.getQueryId()
    slackBotToken = config.getSlackBotToken()

    redash = Redash(redashHost)
    slack = Slack(slackBotToken)

    # Histogram
    response = redash.getQueriesFromRedash(redashQueryId, redashQueryKey)
    result = redash.getColumnData(response, ['Open', 'Close'])
    redash.visualizeHistplotAndSave(result, "./resource/one.png")
    slack.sendFile("./resource/one.png", "#redash-echo", "Title", "comment")


def run3():
    config = Config("./resource/sample.yml")
    redashHost = config.getRedashHost()
    redashQueryKey = config.getQueryApiKey()
    redashQueryId = config.getQueryId()
    slackBotToken = config.getSlackBotToken()

    redash = Redash(redashHost)
    slack = Slack(slackBotToken)

    # Line
    response = redash.getQueriesFromRedash(redashQueryId, redashQueryKey)
    result = redash.getColumnData(response, ['Open', 'Close'])

    data = [ [12, 34], [56, 78] ]
    labels = ['Open', 'Close']
    xAxis = ['2023-07-01', '2023-07-02']
    saveFileName = './resource/one.png'
    redash.visualizeLineAndSave(data, labels, xAxis, saveFileName)
    slack.sendFile("./resource/one.png", "#redash-echo", "Title", "comment")

def run4():
    config = Config("./resource/sample.yml")
    redashHost = config.getRedashHost()
    redashQueryKey = config.getQueryApiKey()
    redashQueryId = config.getQueryId()
    slackBotToken = config.getSlackBotToken()

    redash = Redash(redashHost)
    slack = Slack(slackBotToken)

    # Bar
    x = ['A', 'B', 'C', 'D']
    y = [12, 13, 6, 11]
    saveFileName = './resource/one.png'
    redash.visualizeBarAndSave(x, y, saveFileName)
    slack.sendFile("./resource/one.png", "#redash-echo", "Title", "comment")

def run5():
    config = Config("./resource/sample.yml")
    redashHost = config.getRedashHost()
    redashQueryKey = config.getQueryApiKey()
    redashQueryId = config.getQueryId()
    slackBotToken = config.getSlackBotToken()

    redash = Redash(redashHost)
    slack = Slack(slackBotToken)

    # Pie
    data = [15, 25, 25, 30, 5]
    labels = ['Group 1', 'Group 2', 'Group 3', 'Group 4', 'Group 5']
    colors = sns.color_palette('pastel')[0:5]
    saveFileName = './resource/one.png'
    redash.visualizePieAndSave(data, labels, colors, saveFileName)
    slack.sendFile("./resource/one.png", "#redash-echo", "Title", "comment")

def run6():
    config = Config("./resource/sample.yml")
    redashHost = config.getRedashHost()
    redashQueryKey = config.getQueryApiKey()
    redashQueryId = config.getQueryId()
    slackBotToken = config.getSlackBotToken()

    redash = Redash(redashHost)
    slack = Slack(slackBotToken)

    response = redash.getQueriesFromRedash(redashQueryId, redashQueryKey)
    print(response.json()['query_result']['data']['rows'])
    data = redash.getColumnData(response, ['Open', 'Close'])

    # [ [Date1], [Date2] ]
    xAxisRaw = redash.getColumnData(response, ['Date'])
    xAxis = []
    for item in xAxisRaw:
        xAxis.append(item[0])

    labels = ['Open', 'Close']
    saveFileName = './resource/one.png'
    redash.visualizeLineAndSave(data, labels, xAxis, saveFileName)
    slack.sendFile("./resource/one.png", "#redash-echo", "Title", "comment")



if __name__ == '__main__':
    run6()



    





