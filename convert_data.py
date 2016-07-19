# Read in text csv
# separate into two dataframes, one for each participant
# break into fields that match the example data format

import pandas as pd

IPHONE_CONVO = 'sample_iphone_text_convo.csv'
IPHONE_MULTI = 'iphone_multi.csv'
ANDROID_CONVO = 'example_data/android_sms_to_text/SMSToTextExample.xslx'
CONTACT_LIST = 'user_index.csv'


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


class IphoneSMSTransformer:
    """Takes a tsv file of SMS messages, manipulates, and reformats."""

    def __init__(self, data, contact_list):
        self.data = data
        self.contact_list = contact_list
        self.df = None
        self.cleaned_data = None
        self.full_data = None
        self.subject = None

        self.read_data()
        self.split_datetime()
        self.fill_in_SMS_data()
        self.print_to_csv()

    def __repr__(self):
        return "{}".format(self.full_data)

    def read_data(self):
        df = pd.read_csv(
            self.data, encoding='latin-1',
            names=['sender', 'phone number', 'datetime', 'message']
        )
        self.df = df

    def split_datetime(self):
        data = self.df
        date_time = data['datetime']
        date = []
        time = []
        for timestamp in date_time:
            pieces = timestamp.split(' ')
            date.append(pieces[0])
            time.append(pieces[1])
        texts = data.drop('datetime', 1)
        texts['date'] = pd.Series(date)
        texts['time'] = pd.Series(time)
        self.cleaned_data = texts

    def fill_in_SMS_data(self):
        df = self.cleaned_data
        # set this manually while developing, but eventually with command line
        participant = 'Jeff Glenn'
        data_type = 'SMS'

        users = df['sender']
        users = users.tolist()
        users = set(users)

        ind_grp = get_ind_grp(users)

        for index, row in df.iterrows():
            user_list = list(users)
            sender = row['sender']

            # Since each file should have a single user as its main person,
            # in and out will be determined by relation to that person.
            # let's make this a command line option
            in_out = 'out' if sender == participant else 'in'

            # contact name will need to be fixed to handle multigroup
            # can replace this with the user name from the first column
            # since the user in each case will actually be the
            # study participant
            # Problem: in multi convo, more than one recipient. put in all as
            # list? or create multiple fields? would then need mulitple fields
            # for relationship
            contact_name = 'Finley'

            contact_relationship = get_contact_relationship(
                self.contact_list, contact_name
                )
            df.loc[index, 'data type'] = data_type
            df.loc[index, 'in_out'] = in_out
            df.loc[index, 'contact name'] = contact_name
            df.loc[index, 'contact relationship'] = contact_relationship
            df.loc[index, 'ind_grp'] = ind_grp

        self.full_data = df

    def print_to_csv(self):
            df = self.full_data
            df.to_csv('iphone.csv')


def get_ind_grp(user_set):
    num_users = len(user_set)
    if num_users > 2:
        ind_grp = "grp"
    else:
        ind_grp = "ind"
    return ind_grp


def get_contact_relationship(id_file, contact_name):
    contact_index = pd.read_csv(id_file)
    contact_row = contact_index[contact_index['name'] == contact_name]
    contact_relationship = contact_row['relation'].iloc[0]
    return contact_relationship


def main():
    # while the file format for the iphone SMS data is csv,
    # it's actually a tsv file
    texts = IphoneSMSTransformer(IPHONE_MULTI, CONTACT_LIST)
    print(texts)

if __name__ == '__main__':
    main()
