from collections import Counter
from urlextract import URLExtract
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import pandas as pd
import emoji
import seaborn as sns



import streamlit as st
def stats(user_type,df ):
    if user_type is not "Overall":
        df= df[df['user']==user_type]
    words=[]
    for messages in df['message']:
        words.extend(messages.split())
        
    media = df[df['message'].str.contains('<Media omitted>', case=False, na=False)]
    
    urls=[]
    extractor = URLExtract()

    for messages in df['message']:
        urls.extend (extractor.find_urls(messages) )

        
    return len(df), len(words), len(media), len(urls)

def most_busy_user(df):
    
    
    
    cf = df
    cf = cf[~cf['user'].str.contains('added')]
    cf = cf[~cf['user'].str.contains('left')]
    cf = cf[~cf['user'].str.contains('security')]
    cf = cf[~cf['user'].str.contains('changed')]
    cf = cf[~cf['user'].str.contains('removed')]
    cf = cf[~cf['user'].str.contains('deleted')]
    cf = cf[~cf['user'].str.contains('group-notification')]
    cf = cf[~cf['user'].str.contains('joined')]
    cf = cf[~cf['user'].str.contains('created')]
    x = cf['user'].value_counts().head()


    y=pd.DataFrame(round(cf['user'].value_counts()/len(cf)*100,2)).reset_index().rename(columns={'user':'name','count':'percent'})        
    return x,y
    


def get_wordcloud(user_type,df):
    if user_type is not "Overall":
        df= df[df['user']==user_type]
    cf=df
    keywords = ['added', 'left', 'security', 'changed', 'removed', 'deleted', 'group-notification']
    cf = cf[~cf['user'].str.contains('|'.join(keywords))]
    cf = cf[~cf['message'].str.contains('<Media omitted>')]
    f=open('stop_hinglish.txt','r')
    stop_hinglish=f.read()
    words=[]
    for message in cf['message']:
        for word in message.lower().split():
            if word not in stop_hinglish:
                words.append(word)
    from collections import Counter
    f.close()
    y=pd.DataFrame(Counter(words).most_common(len(Counter(words)))).reset_index().drop(columns=['index']).rename(columns={0:'words',1:'freq'})
    wc = WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    df_wc= wc.generate(y['words'].str.cat(sep=' '))
    return df_wc

def top_com_words(user_type,df):
    if user_type is not "Overall":
        df= df[df['user']==user_type]
    cf=df
    keywords = ['added', 'left', 'security', 'changed', 'removed', 'deleted', 'group-notification']
    cf = cf[~cf['user'].str.contains('|'.join(keywords))]
    cf = cf[~cf['message'].str.contains('<Media omitted>')]
    f=open('stop_hinglish.txt','r')
    stop_hinglish=f.read()
    words=[]
    for message in cf['message']:
        for word in message.lower().split():
            if word not in stop_hinglish:
                words.append(word)
    from collections import Counter
    f.close()
    y=pd.DataFrame(Counter(words).most_common(20)).reset_index().drop(columns=['index']).rename(columns={0:'words',1:'frequency'})
    return y

def fetch_message(df,selected_user):
    df= df[df['user']==selected_user]
    return df


def top_emoji(user_type,df ):
    if user_type is not "Overall":
        df= df[df['user']==user_type]
        
    emojis=[]
    for message in df["message"]:
        emojis.extend(emoji.emoji_list(message))
    emojis = [entry['emoji'] for entry in emojis]
    y=pd.DataFrame(Counter(emojis).most_common(10)).rename(columns={0:'emoji',1:'frequency'})
    return y


def time_line(user_type,df ):
    if user_type is not "Overall":
        df= df[df['user']==user_type]
    cf = df
    cf = g(cf.copy())
    timeline=cf.groupby(['year','month_number','month']).count()['message'].reset_index()
    time=[]
    for i in range(len(timeline)):
        time.append(timeline['month'][i]+' - '+ str(timeline['year'][i]))
    timeline['time']=time
    return timeline
    
    
def g(df):
    df['month_number'] = df['month'].map({'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6, 'July': 7, 'August': 8, 'September': 9, 'October': 10, 'November': 11, 'December': 12,'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'Jun': 6, 'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12})
    return df  

def  daily_timeline(user_type,df ):
    if user_type is not "Overall":
        df= df[df['user']==user_type]
    dt= df.groupby('only_date').count()['message'].reset_index()
    return dt
def week_activity(user_type,df ):
    if user_type is not "Overall":
        df= df[df['user']==user_type]
    wt=df['dayname'].value_counts().reset_index().rename(columns={'count':'message'})
    return wt
def month_activity(user_type,df ):
    if user_type is not "Overall":
        df= df[df['user']==user_type]
    wt=df['month'].value_counts().reset_index().rename(columns={'count':'message'})
    return wt

def heat_map_data(user_type,df ):
    if user_type is not "Overall":
        df= df[df['user']==user_type]
    period_order = ['12AM - 1AM', '1AM - 2AM', '2AM - 3AM', '3AM - 4AM', '4AM - 5AM',
                '5AM - 6AM', '6AM - 7AM', '7AM - 8AM', '8AM - 9AM', '9AM - 10AM',
                '10AM - 11AM', '11AM - 12PM', '12PM - 1PM', '1PM - 2PM', '2PM - 3PM',
                '3PM - 4PM', '4PM - 5PM', '5PM - 6PM', '6PM - 7PM', '7PM - 8PM',
                '8PM - 9PM', '9PM - 10PM', '10PM - 11PM', '11PM - 12AM']
    df['period'] = pd.Categorical(df['period'], categories=period_order, ordered=True)
    heatmap_data = df.pivot_table(index='dayname', columns='period', values='message', aggfunc='count').fillna(0)
    
    return heatmap_data
    
