# ----- import libraries and  modules ---
import pandas as pd
import datetime
from indexes import columns_multi_index

class TrackerFrame():
    def __init__(self, csv_file, tab, option, value):
        # @property
        # def _constructor(self):
        #     return TrackerFrame

        self.value = value
        self.tab = tab
        self.option = option

        print(f"Passed to dataframe: tab - {tab}, option - {option}, value - {value}")

        # ----- import dataframe or create new one -----
        try:
            self.frame = pd.read_csv(csv_file, index_col= 0, parse_dates=True, header=[0, 1], skipinitialspace=True)
            print(self.frame.index)
        except Exception as e:
            print(e) #e.args
            todays_date = datetime.datetime.now().date() #get today's date
            print(type(todays_date))
            # index = pd.date_range(todays_date, periods=1, freq='D') #create index range with one date (today)
            # print(index)
            self.frame = pd.DataFrame(columns=columns_multi_index) #create empty pd.dataFrame object with columns
            self.frame.columns = self.frame.columns.str.split(', ', 1, expand=True) #convert tuple columnd names into multiIndex
            self.frame.loc[todays_date, ('mood', 'angry')] = 'NOPe' #add one value
            print(self.frame.index)

    # def update_frame(self, )

if __name__ == '__main__':
    TrackerFrame('test_df.csv')

