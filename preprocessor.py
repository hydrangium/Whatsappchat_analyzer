import re
import pandas as pd
def preprocess(data):
    pattern = r'\d{2}/\d{2}/\d{2},\s\d{1,2}:\d{2}\s(?:am|pm)\s-\s'
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)
    df = pd.DataFrame({'User Message': messages, 'Message_dates': dates})

    # Clean 'Message_dates' to remove extra characters
    df['Message_dates'] = df['Message_dates'].str.replace(r' - .*', '', regex=True)

    # Convert 'Message_dates' to datetime
    df['Message_dates'] = pd.to_datetime(df['Message_dates'], format='%d/%m/%y, %I:%M %p')

    # Rename column
    df.rename(columns={'Message_dates': 'Dates'}, inplace=True)

    # Convert time to 12-hour format with AM/PM
    df['Date'] = df['Dates'].dt.strftime('%d/%m/%Y, %I:%M %p')
    df = df.drop(columns=['Dates'])

    users = []
    message = []
    for messg in df['User Message']:
        entry = re.split('([\w\W]+?):\s', messg)
        if entry[1:]:
            users.append(entry[1])
            message.append(entry[2])
        else:
            users.append('group_notification')
            message.append(entry[0])
    df['user'] = users
    df['message'] = message
    df.drop(columns=['User Message'], inplace=True)

    df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y, %I:%M %p')
    df['only_date'] = df['Date'].dt.date
    df['year'] = df['Date'].dt.year
    df['month_num'] = df['Date'].dt.month
    df['day_name']=df['Date'].dt.day_name()
    df['month'] = df['Date'].dt.month_name()
    df['day'] = df['Date'].dt.day
    df['hour'] = df['Date'].dt.hour
    df['minute'] = df['Date'].dt.minute
    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period

    return df