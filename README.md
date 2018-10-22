# Facebook Chat Statistics

A small program written in Python 3 that lets you see statistics of any given Facebook Messenger conversation. I used this as a Valentines day surprise for my girlfriend and it is therefore focused on only conversations between two persons, but can be modified and used for any other purpose. This project was inspired by [this](https://www.reddit.com/r/dataisbeautiful/comments/7xicua/my_girlfriend_made_a_visualization_of_all/) Reddit post.

## Features

The program fetches data such as:

* Start time
* End time
* Number of days
* Number of messages
* Number of words
* Average length of messages
* Average messages per day
* Number of :heart:s written by each conversation participant

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

Firstly you will need to [download](https://github.com/davidkrantz/FacebookChatStatistics/archive/master.zip) or clone the repository, the latter can be done by typing
```
git clone https://github.com/davidkrantz/FacebookChatStatistics.git
```
in your terminal.

### Download your Facebook conversations to a .json file
Download your Facebook data by following [these](https://www.facebook.com/help/212802592074644?helpref=uf_permalink) instructions and chosing the format to be JSON. Note that you only have to download your messages in order for this program to work.

### Run it
1. First you will have to install the needed packages. The script uses [Matplotlib](https://matplotlib.org/faq/installing_faq.html) to plot and the package [Emoji](https://github.com/carpedm20/emoji) to easily switch between emojis and strings. Matplotlib can be installed by for example typing

```
pip3 install matplotlib
```
and Emoji can be installed by
```
pip3 install emoji --upgrade
```

2. Run the script as below with the path to your parsed conversation as an argument, for example
```
python3 facebook_chat_statistics.py /Path/To/Conversation.json
```

Enjoy!
