# Read in text csv
# separate into two dataframes, one for each participant
# break into fields that match the example data format

import pandas as pd

IPHONE_CONVO = 'sample_iphone_text_convo.csv'
ANDROID_CONVO = 'example_data/android_sms_to_text/SMSToTextExample.xslx'
CONTACT_LIST = 'user_index.csv'


class IphoneSMSTransformer:
    """Takes a tsv file of SMS messages, manipulates, and reformats."""

    def __init__(self, data, contact_list):
        self.data = data
        self.contact_list = contact_list
        self.df = None
        self.texts = None
        self.full_data = None

        self.read_data()
        self.split_datetime()
        self.fill_in_SMS_data()
        self.print_to_csv()

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
        df = self.texts

        data_type = 'SMS'
        # I assume that in_out is whether the participant wrote the message
        # or received it?
        # If each participant has their own csv file, it would always be out
        # If not, if data of all participants in one file,
        # will need to determine this.
        in_out = "out"

        users = df['user']
        users = users.tolist()
        users = set(users)

        ind_grp = get_ind_grp(users)

        for index, row in df.iterrows():
            user_list = list(users)
            user_name = row['user']
            contact_name = user_list[1] if user_name == user_list[0] \
                else user_list[0]

            contact_id = get_contact_id(self.contact_list, contact_name)

            df.loc[index, 'data type'] = data_type
            df.loc[index, 'in_out'] = in_out
            df.loc[index, 'contact name'] = contact_name
            df.loc[index, 'contact id'] = contact_id
            df.loc[index, 'ind_grp'] = ind_grp

        self.full_data = df

    def print_to_csv(self):
            df = self.full_data
            df.to_csv('iphone.csv')


class AndroidSMSTransformer:
    """ Takes a data file of SMS messages, manipulates, and reformats. """

    def __init__(self, data, contact_list):
        self.data = data
        self.contact_list = contact_list

        self.read_data()

    def read_data(self):
        pass

    def fill_in_SMS_data(self):
        pass


def get_ind_grp(user_set):
    num_users = len(user_set)
    if num_users > 2:
        ind_grp = "grp"
    else:
        ind_grp = "ind"
    return ind_grp


def get_contact_id(id_file, contact_name):
    contact_index = pd.read_table(id_file)
    contact_row = contact_index[contact_index['name'] == contact_name]
    contact_id = contact_row['id'].iloc[0]
    return contact_id


def main():
    # while the file format for the iphone SMS data is csv,
    # it's actually a tsv file
    texts = IphoneSMSTransformer(IPHONE_CONVO, CONTACT_LIST)
    print(texts)

if __name__ == '__main__':
    main()
