import pandas as pd


def duplicates_checker():

    try:
        duplicates_eliminater = pd.read_csv('users_data.csv')
        duplicates_eliminater.drop_duplicates(subset='0', keep='last', inplace=True)
        duplicates_eliminater.to_csv('users_data.csv', index=False)
        print('Duplicates eliminated!')
    except FileNotFoundError:
        print('No file found!')


class UserCoordinates:
    def __init__(self):
        self.user_longitude = float
        self.user_latitude = float
        self.user_id = int

    def store_coordinates(self, user_id, user_latitude, user_longitude):
        data = [(user_id, user_latitude, user_longitude)]

        try:
            users_data_read = pd.read_csv('users_data.csv')
            print(users_data_read.head())
        except FileNotFoundError:
            print('No file found! Creating..')
            users_data = pd.DataFrame(data=data)
            users_data.to_csv('users_data.csv', index=False)
        else:
            pd.DataFrame(data=data).to_csv('users_data.csv', mode='a', index=False, header=False)

        duplicates_checker()

    def location_checker(self, user_id):
        self.user_id = user_id
        try:
            users_data_coords = pd.read_csv('users_data.csv')
            if users_data_coords.loc[users_data_coords['0'] == user_id]['1'].any():
                self.user_latitude = users_data_coords.loc[users_data_coords['0'] == user_id]['1']
                self.user_longitude = users_data_coords.loc[users_data_coords['0'] == user_id]['2']
                return True
            else:
                return False
        except FileNotFoundError:
            return False
