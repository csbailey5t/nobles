import pandas as pd
import click

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
    """Takes a csv file of SMS messages, manipulates, and reformats."""

    def __init__(self, data, contact_list, output, participant):
        self.data = data
        self.contact_list = contact_list
        self.output_file = output
        self.participant = participant
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
            self.data, encoding='utf-8',
            names=['sender', 'phone number', 'datetime', 'message']
        )
        df.dropna(subset=['message'], inplace=True)
        df["message"] = df["message"].str.replace('\r', '')
        self.df = df

    def split_datetime(self):
        # use pandas to_datetime to handle this Series
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

        participant = self.participant
        data_type = 'SMS'
        # can you go straight from Series to set?
        users = df['sender']
        users = users.tolist()
        users = set(users)

        ind_grp = get_ind_grp(users)

        for index, row in df.iterrows():
            sender = row['sender']

            in_out = 'out' if sender == participant else 'in'

            local_users = users
            # can look at whether to set.remove(sender)
            user_list = list(local_users)
            recipients = [recipient for recipient in user_list
                          if recipient is not sender]

            recipient_relationships = [
                get_recipient_relationship(self.contact_list, recipient)
                for recipient in recipients
            ]

            df.loc[index, 'data type'] = data_type
            df.loc[index, 'in_out'] = in_out
            df.loc[index, 'recipients'] = str(recipients)
            df.loc[index, 'recipient relationship'] = str(
                recipient_relationships
                )
            df.loc[index, 'ind_grp'] = ind_grp

        self.full_data = df

    def print_to_csv(self):
            df = self.full_data
            df.to_csv(self.output_file)


def get_ind_grp(user_set):
    num_users = len(user_set)
    if num_users > 2:
        ind_grp = "grp"
    else:
        ind_grp = "ind"
    return ind_grp


def get_recipient_relationship(id_file, recipient_name):
    recipient_index = pd.read_csv(id_file)
    recipient_row = recipient_index[recipient_index['name'] == recipient_name]
    # Add some check to handle when name isn't in the file
    recipient_relationship = recipient_row['relation'].iloc[0]
    return recipient_relationship


@click.command()
@click.option('--input', '-i', default='iphone_multi.csv',
              help='Provide an input file in csv format'
              )
@click.option('--contact_list', '-cl', default='user_index.csv',
              help='Provide a reference file for recipient relationships'
              )
@click.option('--output', '-o', default='iphone.csv',
              help='Provide a filename for the csv output'
              )
@click.option('--participant', '-p', default='Jeff Glenn',
              help='Provide the name of the participant'
              )
def main(input, contact_list, output, participant):
    texts = IphoneSMSTransformer(input, contact_list, output, participant)
    print(texts)

if __name__ == '__main__':
    main()
