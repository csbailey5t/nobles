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
    # this.
    # How much do they care about messages received by the individual?
    in_out = []
    contact_name = []
    contact_id = []
    ind_grp = []

    for index, row in df.iterrows():
        df.loc[index, 'data type'] = data_type
        # print(row['data type'])
        # for contact name, if only two particpats in convo, can just get
        # other key
        # if using pandas groupby
        # for contact id, will need to get from reference sheet at some pt
        # for ind_group, if only two, indv? if more than two keys, grp?

        # if do groupby, count keys to see if grp or ind
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
