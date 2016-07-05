# Read in text csv
# separate into two dataframes, one for each participant
# break into fields that match the example data format

import pandas as pd

CONVO = 'sample_text_convo.csv'


class SMSTransformer:
    """Takes a tsv file of SMS messages, manipulates them,
     and reformates them."""

    def __init__(self, data):
        self.data = data
        self.df = None
        self.texts = None
        self.full_data = None

        self.read_data()
        self.split_datetime()
        self.fill_in_SMS_data()

    def __repr__(self):
        return "{}".format(self.full_data)

    def read_data(self):
        df = pd.read_table(
            self.data, encoding='latin-1', sep='\t',
            names=['user', 'phone number', 'datetime', 'message']
        )
        self.df = df

    def split_datetime(self):
        date_time = self.df['datetime']
        date = []
        time = []
        for timestamp in date_time:
            pieces = timestamp.split(' ')
            date.append(pieces[0])
            time.append(pieces[1])
        texts = self.df.drop('datetime', 1)
        texts['date'] = pd.Series(date)
        texts['time'] = pd.Series(time)
        self.texts = texts

    def fill_in_SMS_data(self):
        data_type = 'SMS'
        # I assume that in_out is whether the participant wrote the message
        # or received it?
        # If each participant has their own csv file, it would always be out
        # If not, if data of all participants in one file,
        # will need to determine this.
        in_out = "out"
        # How much do they care about messages received by the individual?
        contact_name = []
        # for the moment, let's set contact id to "none"
        # we'll have to grab this from some master reference?
        contact_id = 'none'
        df = self.texts

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
            df.loc[index, 'contact id'] = contact_id
            df.loc[index, 'ind_grp'] = ind_grp

        self.full_data = df


def main():
    # while the file format for the iphone SMS data is csv,
    # it's actually a tsv file
    texts = SMSTransformer(CONVO)
    print(texts)


if __name__ == '__main__':
    main()
