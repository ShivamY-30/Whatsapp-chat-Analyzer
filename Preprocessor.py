import re
import pandas as pd

def preprocessing(data):
    pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s\s?[APMapm]+\s-\s'

    message = re.split(pattern , data)[1:]
    len(message)
    dates = re.findall(pattern , data)

    df = pd.DataFrame({'User_message':message , 'Time':dates})

    #Converting the Time datatype
    df['Time'] = pd.to_datetime(df['Time'], format="%d/%m/%Y, %I:%M %p - ")

    user = []
    messages = []
    for sentence in df['User_message']:
        entry = re.split('([\w\W]+?):\s', sentence)
        if entry[1:]:
            user.append(entry[1])
            messages.append(" ".join(entry[2:]))
        else:
            user.append('group_notification')
            messages.append(entry[0])

    df['user'] = user
    df['message'] = messages
    df.drop(columns=['User_message'], inplace=True)

    df['year'] = df['Time'].dt.year
    df['month_num'] = df['Time'].dt.month
    df['month'] = df['Time'].dt.month_name()
    df['day'] = df['Time'].dt.day
    df['day_name'] = df['Time'].dt.day_name()
    df['hours'] =  df['Time'].dt.hour
    df['minute'] =  df['Time'].dt.minute

    target_emoji = "👹"
    replacement_name = "Shivam"
    # Use str.replace to replace the emoji in the 'Text' column
    df['user'] = df['user'].str.replace(target_emoji, replacement_name)


    period = []
    for hour in df[['day_name', 'hours']]['hours']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period

    return df

