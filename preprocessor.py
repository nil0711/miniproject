import io
import pandas as pd
from datetime import datetime
import numpy as np

def get_time_period(hour):
    if 0 <= hour < 1:
        return '12AM - 1AM'
    elif 1 <= hour < 12:
        return f'{str(hour)[:-2]}AM - {str(hour+1)[:-2]}AM'
    elif hour == 12:
        return '12PM - 1PM'
    else:
        return f'{str(hour-12)[:-2]}PM - {str(hour-11)[:-2]}PM'
def extract_info(line):
    date_formats = ['%d/%m/%y, %I:%M %p', '%d/%m/%y, %H:%M -']
    
    for date_format in date_formats:
        try:
            date_obj = datetime.strptime(line[:17], date_format)
            message = line[17:].strip()
            return date_obj, message
        except ValueError:
            continue

    return None

# Function to preprocess the text file
def preprocess_text_file(uploaded_file):
    content = uploaded_file.read().decode("utf-8").splitlines()

    processed_lines = []
    current_date = None
    current_message = ""

    for line in content:
        line = line.strip()
        if not line:
            continue

        extracted_info = extract_info(line)
        if extracted_info:
            if current_message:
                processed_lines.append((current_date, current_message))
                current_message = ""
            current_date, current_message = extracted_info
        else:
            current_message += ' ' + line

    if current_message:
        processed_lines.append((current_date, current_message))

    df = pd.DataFrame(processed_lines, columns=['date', 'usermessage'])
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df['date'] = df['date'].dt.strftime('%d/%m/%y %I:%M %p')
    df['usermessage'] = df['usermessage'].str.lstrip('-')
    df[['user', 'message']] = df['usermessage'].str.extract(r'([^:]+):?(.*)')
    df.drop('usermessage', axis=1, inplace=True)
    df.loc[df['message'] == '', 'message'] = df['user']
    df.loc[df['message'] == df['user'], 'user'] = 'group-notification'
    df['date'] = pd.to_datetime(df['date'], format='%d/%m/%y %I:%M %p')

    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.strftime('%B')
    df['day'] = df['date'].dt.day
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute
    df['am/pm'] = df['date'].dt.strftime('%p')
    df['dayname']=df['date'].dt.day_name()
    df['period'] = df['hour'].apply(get_time_period)

    df['only_date']=df['date'].dt.date
    df = df[~df['user'].str.contains('added')]
    df = df[~df['user'].str.contains('left')]
    df = df[~df['user'].str.contains('security')]
    df = df[~df['user'].str.contains('changed')]
    df = df[~df['user'].str.contains('removed')]
    df = df[~df['user'].str.contains('deleted')]
    df = df[~df['user'].str.contains('joined')]
    df = df[~df['user'].str.contains('created')]

    df = df[~np.isnan(df['year'])]
    df['year'] = df['year'].astype(int)

    return df
