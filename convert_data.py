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


def fill_in_SMS_data(df):
    data_type = 'SMS'
    # I assume that in_out is whether the participant wrote the message
    # or received it?
    # If so, if each participant has their own csv file, it would always be out
    # If not, if data of all participants in one file, will need to determine
    in_out = "out"
    # this.
    # How much do they care about messages received by the individual?
    contact_name = []
    # for the moment, let's set contact id to "none"
    # we'll have to grab this from some master reference?
    contact_id = 'none'

    users = df['user']
    users = users.tolist()
    users = set(users)
    num_users = len(users)
    if num_users > 2:
        ind_grp = "grp"
    else:
        ind_grp = "ind"

    for index, row in df.iterrows():
        user_list = list(users)
        user_name = row['user']
        contact_name = user_list[1] if user_name == user_list[0] \
            else user_list[0]

        df.loc[index, 'data type'] = data_type
        df.loc[index, 'in_out'] = in_out
        df.loc[index, 'contact name'] = contact_name
        df.loc[index, 'contact id'] = 'none'
        df.loc[index, 'ind_grp'] = ind_grp

    return df


def main():
    # while the file format for the iphone SMS data is csv,
    # it's actually a tsv file
    text_conversation = pd.read_table(
        CONVO, encoding='latin-1', sep='\t',
        names=['user', 'phone number', 'datetime', 'message']
    )
    # split date time
    texts = split_datetime(text_conversation)
    # define headers for data format
    # headers = ['participant id', 'data type', 'date',
            #    'time', 'in_out', 'contact name', 'contact id',
            #    'ind_grp', 'message']
    # reorder columns in texts df to match headers
    # cols = ['user', 'data type', 'date', 'time', 'in_out', 'contact_name',
            # 'contact id', 'ind_grp', 'message']
    texts = fill_in_SMS_data(texts)
    print(texts)


if __name__ == '__main__':
    main()
