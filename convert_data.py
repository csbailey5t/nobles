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
        self.texts = None
        self.cleaned_data = None
        self.full_data = None
        self.subject = None

        self.read_data()
        self.get_user_name()
        self.get_text_data()
        self.split_datetime()
        self.fill_in_SMS_data()
        # self.print_to_csv()

    def __repr__(self):
        return "{}".format(self.full_data)

    def read_data(self):
        df = pd.read_csv(
            self.data, encoding='latin-1',
            names=['user', 'phone number', 'datetime', 'message']
        )
        self.df = df

    def get_user_name(self):
        """
        Gets the primary user from the first line of the csv file.
        This is the user whose texts we are concerned about
        """
        df = self.df
        # get first line
        first_row = df.iloc[0]
        chunks = first_row[0].split(' ')
        names = chunks[-2:]
        name = ' '.join(names)
        self.subject = name
        # Use named entity extraction? Will the name always be two words?

    def get_text_data(self):
        """
        Splits the intro data listing the names in the convo from the texts
        themselves.
        """
        df = self.df
        # since the phone number is a number, we can just check for anything
        # greater than 0. This rules out empty cells.
        content = df[df['phone number'] > 0]
        self.texts = content

    def split_datetime(self):
        date_time = self.texts['datetime']
        date = []
        time = []
        for timestamp in date_time:
            pieces = timestamp.split(' ')
            date.append(pieces[0])
            time.append(pieces[1])
        texts = self.df.drop('datetime', 1)
        texts['date'] = pd.Series(date)
        texts['time'] = pd.Series(time)
        self.cleaned_data = texts

    def fill_in_SMS_data(self):
        df = self.cleaned_data

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
            print('contact name is ', contact_id)
            df.loc[index, 'data type'] = data_type
            df.loc[index, 'in_out'] = in_out
            df.loc[index, 'contact name'] = contact_name
            df.loc[index, 'contact id'] = contact_id
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


def get_contact_id(id_file, contact_name):
    contact_index = pd.read_csv(id_file)
    contact_row = contact_index[contact_index['name'] == contact_name]
    print('contact row is: ', contact_row)
    # contact_id = contact_row['relation'].iloc[0]
    contact_id = contact_row['relation']
    return contact_id


def main():
    # while the file format for the iphone SMS data is csv,
    # it's actually a tsv file
    texts = IphoneSMSTransformer(IPHONE_MULTI, CONTACT_LIST)
    print(texts)

if __name__ == '__main__':
    main()
