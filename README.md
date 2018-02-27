# Facebook Chat Statistics

A small program written in Python that lets you see statistics of any given Facebook Messenger conversation. I used this as a Valentines day surprise for my girlfriend, but can be modified and used for any other purpose. This project was inspired by [this](https://www.reddit.com/r/dataisbeautiful/comments/7xicua/my_girlfriend_made_a_visualization_of_all/) Reddit post.

## Features

The program fetches data such as:

* Start time
* End time
* Number of days
* Number of messages
* Number of words
* Average length of messages
* Average messages per day

It also plots using Matplotlib the following diagrams (see pictures below)

* Who texts the most
* Timeline
* Activity by day
* Activity by weekday
* Top 10 emojis

## Images

<img src="pics/who_texts_the_most.png"/>
<img src="pics/timeline.png">
<img src="pics/activity_by_day.png">
<img src="pics/activity_by_week.png">
<img src="pics/top_10_emojis.png">

## Running locally

### Convert your conversation to a .json file
1. Download your Facebook data by following [these](https://www.facebook.com/help/212802592074644?helpref=uf_permalink) instructions.

2. Install [Facebook Chat Archive Parser](https://github.com/ownaginatious/fbchat-archive-parser) with
```
pip3 install fbchat-archive-parser
```

3. Using your terminal, locate to the downloaded Facebook data folder. With the Facebook Chat Archive Parser you can choose to only parse one specific conversation using the following command
```
fbcap ./messages.htm -t FirstNameOrLastName -f json
``` 

Click [here](https://github.com/ownaginatious/fbchat-archive-parser) for more information on how to use the Facebook Chat Archive Parser.

### Run it
1. First you will have to install the needed packages. The script uses Matplotlib to plot and the package Emoji to easily switch between emojis and strings. Matplotlib can be installed by typing

```
pip3 install matplotlib
```
and Emoji can be installed by
```
pip3 install emoji --upgrade
```

2. Edit the Python script so that it loads your parsed conversation by replacing the path below to the path of your conversation
```
data = json.load(open('/Path/To/Your/Conversation.json'))
```
You can also change the names declared in the script to your liking.

3. Run the script with
```
python3 facebook_chat_statistics.py
```

Enjoy!