import sys
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import numpy as np
import json
from datetime import datetime, timedelta
import matplotlib.dates as mdates
import emoji


#### Facebook Chat Statistics ####


def main():
    if len(sys.argv) == 2:
         path_to_conversation = str(sys.argv[1])
    else:
        print('Usage: python3 {} /Path/To/Conversation.json'.format(sys.argv[0]))
        sys.exit()

    # Load JSON data
    data = json.load(open(path_to_conversation))

    # Set names of conversation participants
    you = data['participants'][1]['name']
    partner = data['participants'][0]['name']

    # Convert unicode characters into what Python expects them to look like
    for message in data['messages']:
        message['sender_name'] = message['sender_name'].encode('raw_unicode_escape').decode('utf-8')
        if 'content' in message:
            message['content'] = message['content'].encode('raw_unicode_escape').decode('utf-8')

    # Start time
    start_time = datetime.fromtimestamp(data['messages'][-1]['timestamp_ms']/1000)
    print('Start time: {}'.format(start_time))

    # End time
    end_time = datetime.fromtimestamp(data['messages'][0]['timestamp_ms']/1000)
    print('End time: {}'.format(end_time))

    #### Totals ####

    # Number of days
    nbr_days = (end_time - start_time).days
    print('Number of days: {}'.format(nbr_days))

    # Number of messages
    nbr_msg = len(data['messages'])
    print('Number of messages: {}'.format(nbr_msg))

    # Total number of words
    nbr_words = 0
    for message in data['messages']:
        if 'content' in message:
            nbr_words += len(message['content'].split())
    print('Number of words: {}'.format(nbr_words))

    #### Averages ####

    # Length of a message
    avg_len_msg = round(nbr_words / nbr_msg, 1)
    print('Average length of messages: {} words'.format(avg_len_msg))

    # Messages per day
    avg_msg_per_day = round(nbr_msg / nbr_days, 1)
    print('Average messages per day: {}'.format(avg_msg_per_day))

    # Plot of who texts the most
    nbr_you = 0
    nbr_partner = 0
    for message in data['messages']:
        if message['sender_name'] == you:
            nbr_you += 1
        else:
            nbr_partner += 1
    procentage_you = 100 * round(nbr_you / nbr_msg, 2)
    procentage_partner = 100 * round(nbr_partner / nbr_msg, 2)
    fracs = [procentage_you, procentage_partner];
    labels = [you, partner]
    colors = ['xkcd:crimson', '#F08080']
    pie = plt.pie(fracs, colors=colors, labels=labels, startangle=90, autopct='%1.1f%%')
    plt.axis('equal')
    plt.title("Who texts the most?")
    plt.show()
    print('Number of messages {}: {} ({} %)'.format(you, nbr_you, procentage_you))
    print('Number of messages {}: {} ({} %)'.format(partner, nbr_partner, procentage_partner))

    # Fetch timeline data
    timeline = [None] * (nbr_days + 2)
    hour = list(range(24))
    weekday_arr = [0, 1, 2, 3, 4, 5, 6]
    nbr_times_hour = [0] * 24
    nbr_times_weekday = [0] * 7
    nbr_times_day = [0] * (nbr_days + 2)
    current_day = end_time.date()
    index = len(timeline) - 1
    timeline[index] = current_day
    nbr_times_day[index] = 1
    for message in data['messages']:
        current = datetime.fromtimestamp(message['timestamp_ms']/1000)
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
        elif current < current_day:
            diff = (current_day - current).days
            index = index - diff
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
    plt.title('Timeline')
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
    plt.bar(hour, nbr_times_hour, align='center', width=0.8, color='xkcd:crimson')
    plt.title('Activity by Day')
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
    plt.bar(weekday_arr, nbr_times_weekday, align='center', width=0.8, color='xkcd:crimson')
    plt.xticks(weekday_arr, weekday_labels)
    plt.title('Activity by Week')
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
    print('Most messages in one day: {}'.format(most_msg))

    # Number of red hearts sent by each person and the most used emojies
    nbr_hearts_you = 0
    nbr_hearts_partner = 0
    emojis_list = {}
    itr = iter(emoji.UNICODE_EMOJI.values())
    for k in itr:
        emojis_list[k] = 0
    for message in data['messages']:
        if 'content' in message and len(message) == 4:
            msg = message['content']
            sender = message['sender_name']
            for c in msg:
                emoji_str = emoji.demojize(c)
                if emoji_str == ':red_heart:':
                    if sender == you:
                        nbr_hearts_you += 1
                    else:
                        nbr_hearts_partner += 1
                if emoji_str in emojis_list:
                    emojis_list[emoji_str] += 1
    print('Number of {} {}: {}'.format(emoji.emojize(':red_heart:'), you, nbr_hearts_you))
    print('Number of {} {}: {}'.format(emoji.emojize(':red_heart:'), partner, nbr_hearts_partner))
    top_emojies = []
    emoji_count = []
    for emoji_key, count in sorted(emojis_list.items(), key=lambda kv: (-kv[1], kv[0]))[:10]:
        top_emojies.append(emoji.emojize(emoji_key))
        emoji_count.append(count)

    # Plot top 10 emojies
    x = np.arange(len(top_emojies))
    plt.bar(x, emoji_count, align="center", width=0.8, color='xkcd:crimson')
    plt.xticks(x, top_emojies)
    plt.title('Top 10 emojis')
    ax.yaxis.grid(linestyle='--')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_linewidth(0.5)
    ax.spines['left'].set_linewidth(0.5)
    fig = plt.figure(1)
    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    main()
