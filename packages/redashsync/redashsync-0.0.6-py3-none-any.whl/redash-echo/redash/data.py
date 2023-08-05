import time
import requests
import seaborn as sns
import matplotlib.pyplot as plt
import os


class Redash:
    def __init__(self, host):
        self.host = host

    def getQueriesFromRedash(self, queryId, queryApiKey):
        candidate = self.host + "/api/queries/" + str(queryId) + "/results.json?api_key=" + queryApiKey
        return requests.get(candidate)

    def getColumnData(self, response, columnList):
        candidatesList = response.json()['query_result']['data']['rows']
        result = []

        for candidate in candidatesList:
            item = []

            for column in columnList:
                item.append(candidate[column])

            result.append(item)

        return result

    # data = [ [12, 34], [56, 78] ]
    # saveFileName = './resource/one.png'
    def visualizeHistplotAndSave(self, data, saveFileName):
        innerLength = len(data[0])
        result = []
        for i in range(innerLength):
            result.append([])

        for item in data:
            for i in range(innerLength):
                result[i].append(item[i])

        for i in range(innerLength):
            sns.histplot(result[i])

        plt.savefig(saveFileName, dpi=300)


    # data = [ [12, 34], [56, 78] ]
    # labels = ['Open', 'Close']
    # xAxis = [ '2023-07-01', '2023-07-02']
    # saveFileName = './resource/one.png'
    def visualizeLineAndSave(self, data, labels, xAxis, saveFileName):
        fig = plt.figure()
        fig.set_facecolor('white')

        for i, label in enumerate(labels):
            x = xAxis
            y = []
            for item in data:
                y.append(item[i])
            sns.lineplot(x=x, y=y, label=label)
            plt.legend

        plt.savefig(saveFileName, dpi=300)


    # x = ['A', 'B', 'C', 'D']
    # y = [12, 13, 6, 11]
    # saveFileName = './resource/one.png'
    def visualizeBarAndSave(self, x, y, saveFileName):
        fig = plt.figure()
        fig.set_facecolor('white')
        sns.barplot(x=x, y=y)
        plt.savefig(saveFileName, dpi=300)


    # data = [15, 25, 25, 30, 5]
    # labels = ['Group 1', 'Group 2', 'Group 3', 'Group 4', 'Group 5']
    # colors = sns.color_palette('pastel')[0:5]
    # saveFileName = './resource/one.png'
    def visualizePieAndSave(self, data, labels, colors, saveFileName):
        plt.pie(data, labels=labels, colors=colors)
        plt.savefig(saveFileName, dpi=300)

    def removeFile(self, fileName):
        time.sleep(10)
        os.remove(fileName)

    def getMarkdown(self, template, rawData, candidateLength):
        result = ""
        for data in rawData:
            temp = []
            for i in range(candidateLength):
                temp.append(str(data[i]))

            temp = tuple(temp)

            result += (template % temp)

        return result;
