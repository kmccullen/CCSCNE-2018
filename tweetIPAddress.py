from twitter import Twitter, OAuth
import subprocess
from datetime import datetime

try:
    fileVar = open("/home/pi/lastTweetSeq.txt", "r")
    lastTweet = fileVar.read()
    lastTweetSeq = int(lastTweet) + 1
    fileVar.close()
except FileNotFoundError:
    lastTweetSeq = 0
fileVar = open("/home/pi/lastTweetSeq.txt", "w")
fileVar.write(str(lastTweetSeq) + "\n")

myIP = subprocess.Popen("hostname -I", shell=True, stdout=subprocess.PIPE).stdout.read()
myIPstr = str(myIP.strip())
myIPstr = myIPstr.replace("'","").replace("b","")
print(str(datetime.now()) + " " + myIPstr)
tweet = 'Raspberry Pi connected at ' + myIPstr + " (" + str(lastTweetSeq) + ")"

token="xxxx"
token_secret="xxxx"
consumer_key="xxxx"
consumer_secret="xxxx"

twitter = Twitter(auth=OAuth(token, token_secret, consumer_key, consumer_secret))
twitter.statuses.update(status=tweet)
twitter.direct_messages.new(user="uuuu", text=tweet)
