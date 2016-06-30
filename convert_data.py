# Read in text csv
# separate into two dataframes, one for each participant
# break into fields that match the example data format

import pandas as pd

CONVO = 'sample_text_convo.csv'


def split_datetime(df):
    date_time = df['datetime']
    date = []
    time = []
    for timestamp in date_time:
        pieces = timestamp.split(' ')
        date.append(pieces[0])
        time.append(pieces[1])
    texts = df.drop('datetime', 1)
    texts['date'] = pd.Series(date)
    texts['time'] = pd.Series(time)
    return texts


def main():
    # while the file format for the iphone SMS data is csv,
    # it's actually a tsv file
    text_conversation = pd.read_table(
        CONVO, encoding='latin-1', sep='\t',
        names=['user', 'phone number', 'datetime', 'message']
    )
    # split date time
    texts = split_datetime(text_conversation)

    print(texts)
    # grouped = text_conversation.groupby(['user'])
    # split into two dataframes, based on user.

    # should be able to use pd.groupby

if __name__ == '__main__':
    main()
