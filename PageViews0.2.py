import requests
import json
import multiprocessing
import itertools


class run():
    def run(self):
        u = userInput()
        c = calls()
        env = u.canvasEnv()
        tok = u.token()
        uID = u.userIDs()
        sd = u.startDate()
        ed = u.endDate()

        p = multiprocessing.Pool(processes=3)
        try:
            p.starmap(c.pages,zip(uID, itertools.repeat(env), itertools.repeat(tok), itertools.repeat(sd), itertools.repeat(ed)))
        except:
            p.join()
            p.close()


class calls():
    def pages(self, userID, instance, token, startDate, endDate):

        url = "https://" + instance + ".instructure.com/api/v1/users/" + userID + "/page_views"

        payload = {'per_page': '100',
                   'start_time': startDate,
                   'end_time': endDate}

        headers = {
            'Authorization': 'Bearer ' + str(token)
        }
        while(url != None):

            response = requests.request(
                "GET", url, headers=headers, data=payload)

            JSONResponse = response.json()
            # print(JSONResponse)
            f = open("user " + userID + " pagesFile.csv", "a")

            for i in range(len(JSONResponse)):
                f.write(str(JSONResponse[i]["created_at"]) + "," + str(JSONResponse[i]["updated_at"]) + "," + str(JSONResponse[i]["url"]) + "," + str(JSONResponse[i]["participated"])+ "," + str(JSONResponse[i]["http_method"]) + "," + str(
                    JSONResponse[i]["user_agent"])+"," + str(JSONResponse[i]["remote_ip"]) + '\n')

            # canvas paginates to results of 100 so we need to get the next relitivle link if there are more then 100 results
            try:
                rLinks = response.links['next']['url']
                url = rLinks
            except KeyError:
                url = None
            rateLimit = response.headers['X-Rate-Limit-Remaining']
            print("rate limit remaining " + rateLimit)
            

            f.close()


class userInput():
    def canvasEnv(self):
        cEnv = input("enter canvas domain: ")
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
        startDate = input("enter the page view start date (yyyy-mm-dd): ")
        return startDate

    def endDate(self):
        endDate = input("enter the page view end date (yyyy-mm-dd): ")
        return endDate


def main():
    r = run()
    r.run()

if __name__ == "__main__":
    main()
