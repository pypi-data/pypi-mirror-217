import pandas as pd

csv_import_columns_keys = {
    'Office Name': 'Office Name',
    'Pincode': 'Pincode',
    'StateName':'StateName',
    'District':'District'
}

class IndiaPincodes:
    def read_csv_file(self):
        df = pd.read_csv('./city_pincode_district_state.csv',usecols=list(csv_import_columns_keys.keys()), converters={'Office Name': str.strip, 'Pincode': str.strip,"District":str.strip, "StateName": str.strip})
        if sorted(list(df.columns)) == sorted(list(csv_import_columns_keys.keys())):
            df.rename(columns=csv_import_columns_keys, inplace=True)
            df.fillna(value=0, inplace=True)
            data_list = df.to_dict(orient='records')
            return data_list
    
    def state_wise_pincode(self,state_name):
        pincode_list = self.read_csv_file()
        state_wise_pincode = []
        for data in pincode_list:
            res_data = {}
            if data['StateName']==state_name:
                res_data.clear()
                res_data['Office Name'] = data['Office Name']
                res_data['Pincode'] = data['Pincode']
                res_data['StateName'] = data['StateName']
                res_data['District'] = data['District']
                state_wise_pincode.append(res_data)
        return state_wise_pincode
                
                

obj = IndiaPincodes()
res = obj.read_csv_file()
state_wise_pincode_data = obj.state_wise_pincode('West Bengal')
