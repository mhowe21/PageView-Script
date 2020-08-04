# imports and install
import json
import multiprocessing
import itertools
import subprocess
import sys
import tempfile
try:
    import requests
except ModuleNotFoundError:
    print("attempting to install requests")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
try:
    import pandas
except ModuleNotFoundError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pandas"])


def run():
    u = userInput()
    pool = multiprocessing.Pool()
    env = u.canvasEnv()
    tok = u.token()
    uID = u.userIDs()
    sd = u.startDate()
    ed = u.endDate()
    # calls(tok,env,sd,ed).pageViewsCSV()
    c = calls(tok, env, sd, ed)

    # multiprocess users
    print("Running...")
    try:
        pool.map(c.pageViewsCSV, uID)
        pool.join()
        pool.close()
    # catch possible  errors at the end of a sequence and close the multithreaded tabs.
    except:
        pool.close()
        print("Done")


class calls():
    def __init__(self, canvasToken, instance, startTime=None, endTime=None):
        self.canvasToken = canvasToken
        self.instance = instance
        self.JSONData = {}
        self.startTime = startTime
        self.endTime = endTime

    def pageViewsCSV(self, userID):
        """Get JSON object for users page views."""

        includeHeader = True
        burnFile = tempfile.TemporaryFile("a+")
        url = f"https://{self.instance}/api/v1/users/{userID}/page_views"
        payload = {"per_page": "100",
                   "start_time": self.startTime, "end_time": self.endTime}
        headers = {"Authorization": f"Bearer {self.canvasToken}"}

        while(url != None):
            response = requests.request(
                "GET", url, headers=headers, data=payload)
            burnFile = response.text.encode("utf8")
            dataframe = pandas.read_json(burnFile)
            dataframe.to_csv(f"user_{userID}_pageview.csv", mode="a",
                             header=includeHeader, index=False, encoding="utf8")
            # turn off headers after the first set of canvas data is returned and written
            includeHeader = False

            try:
                linkHeaders = response.links["next"]["url"]
                url = linkHeaders
            except KeyError:
                url = None

        return None


class userInput():
    def canvasEnv(self):
        cEnv = input("enter canvas domain e.g. canvas.instructure.com: ")
        return cEnv

    def token(self):
        tok = input("enter your token: ")
        return tok

    def userIDs(self):
        uID = input("enter the user id's seperated by comma: ")
        uID = uID.replace(" ", "")
        userList = uID.split(",")
        return userList

    def startDate(self):
        startDate = input(
            "enter the page view start date, leave blank for all. (yyyy-mm-dd): ")
        startDate = startDate.replace(" ", "")
        return startDate

    def endDate(self):
        endDate = input(
            "enter the page view end date, leave blank for all. (yyyy-mm-dd): ")
        endDate = endDate.replace(" ", "")
        return endDate


def main():
    run()


if __name__ == "__main__":
    main()
