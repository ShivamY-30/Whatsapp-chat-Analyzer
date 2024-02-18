# import WordCloud as WordCloud
from urlextract import URLExtract
from collections import Counter
import pandas as pd
import emoji



def helper_method(selected_user , df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    num_msg = df.shape[0]
    num_words = []
    for msg in df['message']:
        num_words.extend(msg.split())

    #To calculate number oflinks
    extractor = URLExtract()
    links = []
    for msg in df['message']:
        links.extend(extractor.find_urls(msg))


    # TO calculate total shared media
    total_media = df[df['message'] == '<Media omitted>\n'].shape[0]

    return num_msg, len(num_words),total_media ,len(links)



def Top_user(df):
    df = df[df['user'] != 'group_notification']
    Top_users = df['user'].value_counts().head()
    percentage_df = round(((df['user'].value_counts())/df.shape[0])*100 , 2).reset_index().rename(columns={'user' : 'name' , 'count': 'Percentage'})
    # percentage_df.reset_index().rename(columns={'user' : 'name' , 'count': 'Percentage'})
    return Top_users , percentage_df.head(5)




# def wordcloud(selected_user , df):
#
#     if selected_user != 'Overall':
#         df = df[df['user'] == selected_user]
#
#     wc = WordCloud(width = 400 ,height = 400 , min_font_size = 8, background_color = 'white' )
#     df_wc = wc.generate(df['message'].str.cat(sep = " "))
#
#     return df_wc


def most_common_Words(selected_user , df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # Removing group_notification
    temp = df[df['user'] != 'group_notification']
    #removing mediamessages
    temp = df[df['message'] != '<Media omitted>\n']

    # 3 remove all hinglish stop words
    file = open('stop_hinglish.txt' , 'r')
    stop_words = file.read()
    # print(stop_words)
    words = []
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    # words
    return pd.DataFrame(Counter(words).most_common(15),columns= ['Message' ,'Frequency' ])




def emoji_founder(selected_user , df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.UNICODE_EMOJI['en']])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))) , columns= ['Emoji' ,'Frequency' ])

    return emoji_df.head(10)

def timeline_chat(selected_user , df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year' , 'month_num' , 'month']).count()['message'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

    timeline['time']=time
    return timeline


def day_most_activity(selected_user , df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    major_day = df['day_name'].value_counts().reset_index()

    return major_day

def month_most_activity(selected_user , df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    major_month = df['month'].value_counts().reset_index()

    return major_month


def activity_heatmap(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    user_heatmap = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)

    return user_heatmap
