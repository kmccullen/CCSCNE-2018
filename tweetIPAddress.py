from twitter import Twitter, OAuth
import subprocess
import sys

try:
    fileVar = open("/home/pi/lastTweetSeq.txt", "r")
    lastTweet = fileVar.read()
    lastTweetSeq = int(lastTweet) + 1
    fileVar.close()
except IOError:
    lastTweetSeq = 0
    
fileVar = open("/home/pi/lastTweetSeq.txt", "w")
fileVar.write(str(lastTweetSeq) + "\n")
fileVar.close()

with open("/etc/hostname") as fileVar:
    hostName = fileVar.read()[:-1]

myIP = subprocess.Popen("hostname -I", shell=True, stdout=subprocess.PIPE).stdout.read()
myIPstr = str(myIP.strip())
myIPstr = myIPstr.replace("'","").replace("b","")
tweet = hostName + " connected at " + myIPstr + " (" + str(lastTweetSeq) + ")"

token="xxxx"
token_secret="xxxx"
consumer_key="xxxx"
consumer_secret="xxxx"

twitter = Twitter(auth=OAuth(token, token_secret, consumer_key, consumer_secret))
twitter.direct_messages.new(user="uuuu", text=tweet)
