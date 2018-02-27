import matplotlib.pyplot as plt
import matplotlib.dates as dt
from matplotlib.dates import DateFormatter
import numpy as np
import json
from datetime import datetime, timedelta
import matplotlib.dates as mdates
import emoji


#### Facebook Chat Statistics ####

# Load JSON data. Edit the path below to the path of your parsed conversation.
data = json.load(open('/Path/To/Your/Conversation.json'))

# Names. Change these to your liking.
you = 'You'
partner = 'Partner'

# Start time
start_time = data['threads'][0]['messages'][0]['date']
start_time = start_time[:16]
start_time = datetime.strptime(start_time, "%Y-%m-%dT%H:%M")
print("Start time: " + str(start_time))

# End time
end_time = data['threads'][0]['messages'][len(data['threads'][0]['messages']) - 1]['date']
end_time = end_time[:16]
end_time = datetime.strptime(end_time, "%Y-%m-%dT%H:%M")
print("End time: " + str(end_time))

#### Totals ####

# Number of days
nbr_days = (end_time - start_time).days
print("Number of days: " + str(nbr_days))

# Number of messages
nbr_msg = len(data['threads'][0]['messages'])
print("Number of messages: " + str(nbr_msg))

# Total number of words
nbr_words = 0
for i in range(0, len(data['threads'][0]['messages'])):
	nbr_words = nbr_words + len(data['threads'][0]['messages'][i]['message'].split())
print("Number of words: " + str(nbr_words))

#### Averages ####

# Length of a message
avg_len_msg = round(nbr_words / nbr_msg, 1)
print("Average length of messages: " + str(avg_len_msg) + " words")

# Messages per day
avg_msg_per_day = round(nbr_msg / nbr_days, 1)
print("Average messages per day: " + str(avg_msg_per_day))

# Plot of who texts the most
nbr_you = 0
nbr_partner = 0
for i in range(0, len(data['threads'][0]['messages'])):
	if data['threads'][0]['messages'][i]['sender'] == you:
		nbr_you = nbr_you + 1
	else:
		nbr_partner = nbr_partner + 1
procentage_you = 100 * round(nbr_you / nbr_msg, 2)
procentage_partner = 100 * round(nbr_partner / nbr_msg, 2)
fracs = [procentage_you, procentage_partner];
labels = [you, partner]
colors = ['xkcd:crimson', '#F08080']
pie = plt.pie(fracs, colors=colors, labels=labels, startangle=90, autopct='%1.1f%%')
plt.axis('equal')
plt.title("Who texts the most?")
plt.show()
print("Number of times " + you + ": " + str(nbr_you) + ' (' + str(procentage_you) + ')')
print("Number of times " + partner + ": " + str(nbr_partner) + ' (' + str(procentage_partner) + ')')

# Fetch timeline data
timeline = [None] * (nbr_days + 2)
hour = list(range(24))
weekday_arr = [0, 1, 2, 3, 4, 5, 6]
nbr_times_hour = [0] * 24
nbr_times_weekday = [0] * 7
nbr_times_day = [0] * (nbr_days + 2)
current_day = start_time.date()
index = 0
timeline[index] = current_day
nbr_times_day[index] = 1
for i in range(0, len(data['threads'][0]['messages'])):
	current = data['threads'][0]['messages'][i]['date']
	current = current[:16]
	current = datetime.strptime(current, "%Y-%m-%dT%H:%M")
	h = current.hour + current.minute / 60. + current.second / 3600
	h = int(round(h))
	if h == 24:
		h = 0
	nbr_times_hour[h] = nbr_times_hour[h] + 1
	wd = current.weekday()
	nbr_times_weekday[wd] = nbr_times_weekday[wd] + 1
	current = current.date()
	if current == current_day:
		nbr_times_day[index] = nbr_times_day[index] + 1
	elif current > current_day:
		diff = (current - current_day).days
		index = index + diff
		current_day = current
		timeline[index] = current_day
		nbr_times_day[index] = 1
dates = [None] * len(timeline)
for i in range(0, len(timeline)):
	if timeline[i] == None:
		timeline[i] = timeline[i - 1] + timedelta(days=1)
	dates[i] = timeline[i].strftime("%Y-%m-%d")

# Plot timeline
fmt = mdates.DateFormatter('%Y-%m-%d')
loc = mdates.MonthLocator(interval=6)
ax = plt.axes()
ax.xaxis.set_major_formatter(fmt)
ax.xaxis.set_major_locator(loc)
plt.bar(timeline, nbr_times_day, align="center", width=8, color='xkcd:crimson')
plt.title("Timeline")
ax = plt.axes()        
ax.yaxis.grid(linestyle='--')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_linewidth(0.5)
ax.spines['left'].set_linewidth(0.5)
fig = plt.figure(1)
fig.autofmt_xdate()
plt.tight_layout()
plt.show()

# Plot by hour
plt.bar(hour, nbr_times_hour, align="center", width=0.8, color='xkcd:crimson')
plt.title("Activity by Day")
ax = plt.axes()        
ax.yaxis.grid(linestyle='--')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_linewidth(0.5)
ax.spines['left'].set_linewidth(0.5)
fig = plt.figure(1)
plt.tight_layout()
plt.show()

# Plot by weekday
weekday_labels = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
plt.bar(weekday_arr, nbr_times_weekday, align="center", width=0.8, color='xkcd:crimson')
plt.xticks(weekday_arr, weekday_labels)
plt.title("Activity by Week")
ax = plt.axes()        
ax.yaxis.grid(linestyle='--')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_linewidth(0.5)
ax.spines['left'].set_linewidth(0.5)
fig = plt.figure(1)
plt.tight_layout()
plt.show()

# Most messages in one day
most_msg = max(nbr_times_day)
print("Most messages in one day: " + str(most_msg))

# Number of red hearts sent by each person and the most used emojies
nbr_hearts_you = 0
nbr_hearts_partner = 0
emojis_list = {}
iter = iter(emoji.UNICODE_EMOJI.values())
for k in iter:
	emojis_list[k] = 0
for i in range(0, len(data['threads'][0]['messages'])):
	msg = data['threads'][0]['messages'][i]['message']
	sender = data['threads'][0]['messages'][i]['sender']
	for c in msg:
		emoji_str = emoji.demojize(c)
		if emoji_str == ':red_heart:':
			if sender == you:
				nbr_hearts_you = nbr_hearts_you + 1
			else:
				nbr_hearts_partner = nbr_hearts_partner + 1
		if emoji_str in emojis_list:
			emojis_list[emoji_str] = emojis_list[emoji_str] + 1
print("Number of " + emoji.emojize(':red_heart:') + " " + you + ": " + str(nbr_hearts_you))
print("Number of " + emoji.emojize(':red_heart:') + " " + partner + ": " + str(nbr_hearts_partner))
top_emojies = []
emoji_count = []
for emoji_key, count in sorted(emojis_list.items(), key=lambda kv: (-kv[1], kv[0]))[:10]:
	top_emojies.append(emoji.emojize(emoji_key))
	emoji_count.append(count)

# Plot top 10 emojies
x = np.arange(len(top_emojies))
plt.bar(x, emoji_count, align="center", width=0.8, color='xkcd:crimson')
plt.xticks(x, top_emojies)
plt.title("Top 10 Emojis")
ax = plt.axes()        
ax.yaxis.grid(linestyle='--')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_linewidth(0.5)
ax.spines['left'].set_linewidth(0.5)
fig = plt.figure(1)
plt.tight_layout()
plt.show()