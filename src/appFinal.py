'''
Created on Oct 20, 2015

@author: Jack
'''

#All imports

import requests
import Tkinter
import plotly.plotly as py
import plotly.tools as tls
import plotly.graph_objs as go
import PIL.Image
import math
from PIL import ImageTk
from Tkinter import *
from textblob import TextBlob

#Access for plotly

tls.set_credentials_file(username='qazwsxcde125', api_key='jqwnqq7qkh')

#Variables, arrays, and tokens. If GUI implemented, can be used to find info of any tag for any amount of pages

access_token = "2240337162.1fb234f.7ea3766fb8c14fcfb04e6d4a2f226ee2"
clientID = "024afdbe8e0a41f0b4161f3439c24e03"
tag = "capitalone"
likesArray = []
postNumber = []
userList = []
userInfo = []
posNeg = []
totalPol = []
pages = 2
posPosts = 0
negPosts = 0
neuPosts = 0

# Hold user data

class user:
    postNum = 0
    userID = ""
    followers = 0
    following = 0
    
    def __init__(self, postNum, userID, followers, following):
        self.postNum = postNum
        self.userID = userID
        self.followers = followers
        self.following = following

    # Retrieves posts and the amount of likes each one has plus other data
urlGet = "https://api.instagram.com/v1/tags/{}/media/recent?access_token={}".format(tag, access_token)
req = requests.get(urlGet)
j = req.json()
    
    #Retrieve first 20 posts
for i in range(0, pages):
    for i in range(0, 20):
        #Likes
        likesArray.append(j['data'][i]['likes']['count'])
        #Info about users
        userList.append(j['data'][i]['user']['id'])
        #Checking polarity
        data = j['data'][i]['caption']['text']
        blob = TextBlob(data)
        posNeg.append(blob.sentiment)
        #Counting posts
        if (blob.sentiment.polarity == 0.0):
            neuPosts = neuPosts + 1
        elif (blob.sentiment.polarity > 0.0):
            posPosts = posPosts + 1
        else:
            negPosts = negPosts + 1
    #Next page
    urlGet = j['pagination']['next_url']
    req = requests.get(urlGet)
    j = req.json()

    #Extract user info
    
for userID in userList:
    urlGet = "https://api.instagram.com/v1/users/{}?access_token={}".format(userID, access_token)
    req = requests.get(urlGet)
    j = req.json()
    newUser = user(j['data']['counts']['media'], userID, j['data']['counts']['followed_by'], j['data']['counts']['follows'])
    userInfo.append(newUser)
    
    #Creating data for graph
    
ind = 0
for data in posNeg:
    ind = ind + 1
    postNumber.append(ind)
    if (ind == 1):
        totalPol.append(round(data.polarity, 2))
    else:
        totalPol.append(round(data.polarity, 2) + totalPol[ind - 2])
    
    #Creating the graph
    
trace0 = go.Scatter(
    x=postNumber,
    y=totalPol,
    name='#CapitalOne Trends',
    fill='tozeroy'
)
    
    #Insert data
    
graphData = [trace0]
layout = go.Layout(
    title='How #CapitalOne Is Trending',
    xaxis=dict(
        title='Most Recent Posts',
        titlefont=dict(
            family='Courier New, monospace',
            size=14,
            color='#000000'
        )
    ),
    yaxis=dict(
        title='Positivity',
        titlefont=dict(
            family='Courier New, monospace',
            size=14,
            color='#000000'
        )
    )
)
fig = go.Figure(data=graphData, layout=layout)

#Open plotly for interactive graph, needs login info

plot_url = py.plot(fig, filename='Trend Graph')

#Save image to be displayed in GUI

py.image.save_as(fig, 'TrendGraph.png')
    
    #GUI
    
root = Tkinter.Tk()
leftFrame = Frame(root)
count = 0

#Titles

Tkinter.Label(leftFrame, text='Tag Popularity', borderwidth=1).grid(row=0,columnspan=7)
Tkinter.Label(leftFrame, text='Provides information about the tag and users who use the tag', borderwidth=1).grid(row=1,columnspan=7)
Tkinter.Label(leftFrame, text='Positive Posts: %s   Negative Posts: %s   Neutral Posts: %s'%(posPosts, negPosts, neuPosts), borderwidth=1).grid(row=2,columnspan=7)
Tkinter.Label(leftFrame, text='Post ', borderwidth=1).grid(row=3,column=0)
Tkinter.Label(leftFrame, text='Likes ', borderwidth=1).grid(row=3,column=1)
Tkinter.Label(leftFrame, text='Posts ', borderwidth=1).grid(row=3,column=2)
Tkinter.Label(leftFrame, text='Followers ', borderwidth=1).grid(row=3,column=3)
Tkinter.Label(leftFrame, text='Following ', borderwidth=1).grid(row=3,column=4)
Tkinter.Label(leftFrame, text='Polarity ', borderwidth=1).grid(row=3,column=5)
Tkinter.Label(leftFrame, text='Subjectivity', borderwidth=1).grid(row=3,column=6)

#Display info

for r in likesArray:
    count = count + 1
    Tkinter.Label(leftFrame, text='%s. |'%(count), borderwidth=0 ).grid(row=count+3,column=0)
    Tkinter.Label(leftFrame, text='%s'%(r), borderwidth=0 ).grid(row=count+3,column=1)
    Tkinter.Label(leftFrame, text='%s'%(userInfo[count - 1].postNum), borderwidth=0 ).grid(row=count+3,column=2)
    Tkinter.Label(leftFrame, text='%s'%(userInfo[count - 1].followers), borderwidth=0 ).grid(row=count+3,column=3)
    Tkinter.Label(leftFrame, text='%s'%(userInfo[count - 1].following), borderwidth=0 ).grid(row=count+3,column=4)
    textPolarity = (math.ceil((posNeg[count - 1].polarity)*100)/100)
    Tkinter.Label(leftFrame, text='{}'.format(textPolarity), borderwidth=0 ).grid(row=count+3,column=5)
    textSubjectivity = (math.ceil((posNeg[count - 1].subjectivity)*100)/100)
    Tkinter.Label(leftFrame, text='{}'.format(textSubjectivity), borderwidth=0 ).grid(row=count+3,column=6)
leftFrame.pack(side = LEFT)

#Display image

canvas = Tkinter.Canvas(root, width=700, height=700)
canvas.pack(side = RIGHT)
photo = PIL.Image.open("TrendGraph.png")
tk_img = ImageTk.PhotoImage(photo)
canvas.create_image(350, 250, image=tk_img)
root.mainloop(  )

#Run Program