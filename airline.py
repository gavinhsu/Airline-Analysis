import numpy as np
class MenuFunction():

    select_airline = '''
Filter airline
1. index
2. airline
3. price range
4. departure time
5. arrival time
'''

    select_round_airline = '''
Filter airline
1. index
2. airline
3. price range
'''

    schedule = '''
Which kind of trip are you going to schedule?
1. one-way trip
2. round trip
3. overall analysis of airline
'''

    prefer_sort = '''
Which kind of sorting result do you prefer?
1. Cheapest
2. Fastest
3. No preference
'''

    prefer_dt = '''
What is your desired deaprture time?
1. Morning (5AM - 12PM)
2. Afternoon (12PM - 5PM)
3. Evening (5PM - 8PM)
4. Night (8PM - 5AM)
'''

    prefer_arr = '''
What is your desired deaprture time?
1. Morning (5AM - 12PM)
2. Afternoon (12PM - 5PM)
3. Evening (5PM - 8PM)
4. Night (8PM - 5AM)
'''

    prefer_round_sort = '''
Which kind of sorting result do you prefer?
1. Cheapest
2. Fastest Outbound Time
3. Fastest Return Time
4. No preference
'''
    

    #fetch user input for departure, date, destination
    def one_way_info(self):
        departure = input("Where are you going to fly from?\n")
        date = input('When are you planned to fly? (dd/mm/yyyy)\n')
        destination = input("Where are you going to fly to?\n")
        return departure,date,destination
    
    def round_trip_info(self):
        departure = input("Where are you going to fly from?\n")
        departure_date = input('When are you planned to fly? (dd/mm/yyyy)\n')
        return_date = input('When are you planned to return? (dd/mm/yyyy)\n')
        destination = input("Where are you going to fly to?\n")
        return departure,departure_date,return_date,destination

    #duration to minute to sort
    def transform_duration(self,df):
        duration = []
        for i in df['Duration'].to_list():
            try:
                hour = int(i[:i.index('h')])
                minute = int(i[i.index('h')+1:-1].strip())
                duration.append(hour*60 + minute)
            except:
                minute = int(i[:-1])
                duration.append(minute)
        df['duration'] = duration
        return df

    #round trip duration
    def round_transform_duration(self,df):
        out_bound_duration = []
        return_duration = []
        for i in df['DurationOutbound'].to_list():
            try:
                hour = int(i[:i.index('h')])
                minute = int(i[i.index('h')+1:-1].strip())
                out_bound_duration.append(hour*60 + minute)
            except:
                minute = int(i[:-1])
                out_bound_duration.append(minute)
        for i in df['DurationReturn'].to_list():
            try:
                hour = int(i[:i.index('h')])
                minute = int(i[i.index('h')+1:-1].strip())
                return_duration.append(hour*60 + minute)
            except:
                minute = int(i[:-1])
                return_duration.append(minute)       
        df['outboundduration'] = out_bound_duration
        df['returnduration'] = return_duration
        return df

    #sort by price or duration
    def sort_table(self,sort_type,df):
        if(sort_type == 1):
            print("The airline searching result will be sorted from low price to high price\n")
            cheap_df = df.sort_values(by=['Price']).reset_index(drop=True)
            cheap_df.index = np.arange(1, len(cheap_df) + 1)
            cheap_df.drop(['duration'],inplace=True,axis=1,errors='ignore')
            print("")
            print(cheap_df)
            return cheap_df
        elif(sort_type == 2):
            print("The airline searching result will be sorted from short duration to long duration\n")
            fast_df = self.transform_duration(df)
            fast_df = fast_df.sort_values(by=['duration']).reset_index(drop=True)
            fast_df.drop(['duration'],inplace=True,axis=1,errors='ignore')
            fast_df.index = np.arange(1, len(fast_df) + 1)
            print("")
            print(fast_df)
            return fast_df
        elif(sort_type == 3):
            print("Your searching result is ")
            print("")
            #drop duration column if exist
            df.drop(['duration'],inplace=True,axis=1,errors='ignore')
            df.index = np.arange(1, len(df) + 1)
            print(df)
            return df

    #round trip sort by price or outbound/return duration
    def sort_round_trip_table(self,sort_type,df):
        if(sort_type == 1):
            print("The airline searching result will be sorted from low price to high price\n")
            cheap_df = df.sort_values(by=['Price']).reset_index(drop=True)
            cheap_df.index = np.arange(1, len(cheap_df) + 1)
            cheap_df.drop(['outboundduration'],inplace=True,axis=1,errors='ignore')
            cheap_df.drop(['returnduration'],inplace=True,axis=1,errors='ignore')
            print("")
            print(cheap_df)
            return cheap_df
        elif(sort_type == 2):
            print("The airline searching result will be sorted from short duration to long duration of out bound\n")
            outbound_df = self.round_transform_duration(df)
            outbound_df = outbound_df.sort_values(by=['outboundduration']).reset_index(drop=True)
            outbound_df.drop(['outboundduration'],inplace=True,axis=1,errors='ignore')
            outbound_df.drop(['returnduration'],inplace=True,axis=1,errors='ignore')
            outbound_df.index = np.arange(1, len(outbound_df) + 1)
            print("")
            print(outbound_df)
            return outbound_df
        elif(sort_type == 3):
            print("The airline searching result will be sorted from short duration to long duration of return\n")
            return_df = self.round_transform_duration(df)
            return_df = return_df.sort_values(by=['returnduration']).reset_index(drop=True)
            return_df.drop(['outboundduration'],inplace=True,axis=1,errors='ignore')
            return_df.drop(['returnduration'],inplace=True,axis=1,errors='ignore')
            return_df.index = np.arange(1, len(return_df) + 1)
            print("")
            print(return_df)
            return return_df       
        elif(sort_type == 4):
            print("Your searching result is ")
            print("")
            #drop duration column if exist
            df.drop(['outboundduration'],inplace=True,axis=1,errors='ignore')
            df.drop(['returnduration'],inplace=True,axis=1,errors='ignore')
            df.index = np.arange(1, len(df) + 1)
            print(df)
            return df

    #filter option
    def index_option(self,df,index):
        df.index = np.arange(1, len(df) + 1)
        return df.iloc[[index-1]].reset_index(drop=True)

    def airline_option(self,df,airline):
        new_df = df[df['Airline'].str.contains(airline)].reset_index(drop=True)
        new_df.index = np.arange(1, len(new_df) + 1)
        return new_df

    def price_option(self,df,max_price,min_price):
        new_df = df[(df['Price'] <= max_price) & (df['Price'] >= min_price)].reset_index(drop=True)
        new_df.index = np.arange(1, len(new_df) + 1)
        return new_df
    
    def dt_option(self,df, dt_time_range):
            if(dt_time_range == 1):
                new_df = df[(df['DepTime'].str[:2].astype('int64') >= 5) & (df['DepTime'].str[:2].astype('int64') < 12)]
                new_df.index = np.arange(1, len(new_df) + 1)
                return new_df
            elif(dt_time_range == 2):
                new_df = df[(df['DepTime'].str[:2].astype('int64') >= 12) & (df['DepTime'].str[:2].astype('int64') < 17)]
                new_df.index = np.arange(1, len(new_df) + 1)
                return new_df          
            elif(dt_time_range == 3):
                new_df = df[(df['DepTime'].str[:2].astype('int64') >= 17) & (df['DepTime'].str[:2].astype('int64') < 20)]
                new_df.index = np.arange(1, len(new_df) + 1)
                return new_df
            elif(dt_time_range == 4):
                new_df = df[ (((df['DepTime'].str[:2].astype('int64') >= 20) & (df['DepTime'].str[:2].astype('int64') < 24)) | ((df['DepTime'].str[:2].astype('int64') >= 0) & (df['DepTime'].str[:2]) < 5)) ]
                new_df.index = np.arange(1, len(new_df) + 1)
                return new_df

    def arr_option(self,df, dt_time_range):
        if(dt_time_range == 1):
            new_df = df[(df['ArrTime'].str[:2].astype('int64') >= 5) & (df['ArrTime'].str[:2].astype('int64') < 12)]
            new_df.index = np.arange(1, len(new_df) + 1)
            return new_df
        elif(dt_time_range == 2):
            new_df = df[(df['ArrTime'].str[:2].astype('int64') >= 12) & (df['ArrTime'].str[:2].astype('int64') < 17)]
            new_df.index = np.arange(1, len(new_df) + 1)
            return new_df          
        elif(dt_time_range == 3):
            new_df = df[(df['ArrTime'].str[:2].astype('int64') >= 17) & (df['ArrTime'].str[:2].astype('int64') < 20)]
            new_df.index = np.arange(1, len(new_df) + 1)
            return new_df
        elif(dt_time_range == 4):
            new_df = df[ (((df['ArrTime'].str[:2].astype('int64') >= 20) & (df['ArrTime'].str[:2].astype('int64') < 24)) | ((df['DepTime'].str[:2].astype('int64') >= 0) & (df['DepTime'].str[:2]) < 5)) ]
            new_df.index = np.arange(1, len(new_df) + 1)
            return new_df

    def dt_not_found(self, dt_time_range):
        if(dt_time_range == 1):
            print('Not able to found the flights in the moring')
        elif(dt_time_range == 2):
            print('Not able to found the flights in the afternoon')
        elif(dt_time_range == 3):
            print('Not able to found the flights in the evening')

        elif(dt_time_range == 4):
            print('Not able to found the flights in the night')

    def arr_not_found(self, arr_time_range):
        if(arr_time_range == 1):
            print('Not able to found the flights in the moring')
        elif(arr_time_range == 2):
            print('Not able to found the flights in the afternoon')
        elif(arr_time_range == 3):
            print('Not able to found the flights in the evening')

        elif(arr_time_range == 4):
            print('Not able to found the flights in the night')     

    def pick_flight(self,choice,df):
    
        #if error, use the original table again, or keep filtering
        new_df = df.copy()

        new_df.index = np.arange(1, len(new_df) + 1)

        while(True):
            print('After you pick a filter option, you can exit the option and filter again by input 0')
            print("")
            try:
                if(choice == 1):
                    #break because only left one row
                    try:
                        index = int(input("Enter the index: "))
                        new_df = self.index_option(new_df,index)
                        if(new_df.shape[0] == 1):
                            break
                        elif(index == '0'):
                            break
                        elif(new_df.empty):
                            new_df = df.copy()
                            print("No match index in the searching result, please filter again!")
                            print(new_df)
                            choice = int(input(self.select_airline))
                            
                    except:
                        print("Your search is invalid. Please enter again!")
                        pass

                elif(choice == 2):
                    airline = input("Enter the airline: ")
                    new_df = self.airline_option(new_df, airline)
                    if(new_df.shape[0] == 1):
                        break
                    #no match
                    elif(new_df.empty):
                        new_df = df.copy()
                        print("Can't find %s airline, please filter again!"%(airline))
                        print("Flights")
                        print(new_df)
                        choice = int(input(self.select_airline))
                    elif(airline == '0' or airline == 0):
                        break
                    else:
                        print("After select the airline you prefer, the searching result is: ")
                        print(new_df)
                        choice = int(input(self.select_airline))

                elif(choice == 3):
                    min_price = input("Enter the min price you accept: ")
                    max_price = input("Enter the max price you accept: ")

                    if(int(max_price) > int(min_price)):   
                        new_df = self.price_option(new_df,int(max_price),int(min_price))
                        if(new_df.shape[0] == 1):
                            break
                        elif(new_df.empty):
                            new_df = df.copy()
                            print("Can't find data of price between %s and %s, please filter again!"%(min_price,max_price))
                            print("Flights")
                            print(new_df)
                            choice = int(input(self.select_airline))
                        elif(min_price == '0' or max_price == '0'):
                            break
                        else:
                            print("After select the price range you prefer, the searching result is: ")
                            print(new_df)
                            choice = int(input(self.select_airline))
                    else:
                        print("The price range is invalid. Please enter again!")
                
                elif(choice == 4):
                    dt_time_range = input(self.prefer_dt)
                    new_df = self.dt_option(new_df, int(dt_time_range))
                        
                    if(new_df.shape[0] == 1):
                        break
                    elif(new_df.empty):
                        new_df = df.copy()
                        self.dt_not_found(int(dt_time_range))
                        print("Please filter again!")
                        print("Flights")
                        print(new_df)
                        choice = int(input(self.select_airline))
                    elif(dt_time_range == '0'):
                        break
                    else:
                        print("After select the range of departure time, the searching result is: ")
                        print(new_df)
                        choice = int(input(self.select_airline))


                elif(choice == 5):
                    arr_time_range = input(self.prefer_arr)
                    new_df = self.arr_option(new_df, int(arr_time_range))
                        
                    if(new_df.shape[0] == 1):
                        break
                    elif(new_df.empty):
                        new_df = df.copy()
                        self.arr_not_found(int(arr_time_range))
                        print("Please filter again!")
                        print("Flights")
                        print(new_df)
                        choice = int(input(self.select_airline))
                    elif(arr_time_range == '0'):
                        break
                    else:
                        print("After select the range of arrival time, the searching result is: ")
                        print(new_df)
                        choice = int(input(self.select_airline))

            except Exception as e:
                print(e)
                print("Your search is invalid. Please enter again!")
                pass
        return new_df

    #round trip pick filght
    def pick_round_flight(self,choice,df):
    
        #if error, use the original table again, or keep filtering
        new_df = df.copy()

        new_df.index = np.arange(1, len(new_df) + 1)

        while(True):
            print('After you pick a filter option, you can exit the option and filter again by input 0')
            print("")
            try:
                if(choice == 1):
                    #break because only left one row
                    try:
                        index = int(input("Enter the index: "))
                        new_df = self.index_option(new_df,index)
                        if(new_df.shape[0] == 1):
                            break
                        elif(index == '0'):
                            break
                        elif(new_df.empty):
                            new_df = df.copy()
                            print("No match index in the searching result, please filter again!")
                            print(new_df)
                            choice = int(input(self.select_round_airline))
                            
                    except:
                        print("Your search is invalid. Please enter again!")
                        pass

                elif(choice == 2):
                    airline = input("Enter the airline: ")
                    new_df = self.airline_option(new_df, airline)
                    if(new_df.shape[0] == 1):
                        break
                    #no match
                    elif(new_df.empty):
                        new_df = df.copy()
                        print("Can't find %s airline, please filter again!"%(airline))
                        print("Flights")
                        print(new_df)
                        choice = int(input(self.select_round_airline))
                    elif(airline == '0' or airline == 0):
                        break
                    else:
                        print("After select the airline you prefer, the searching result is: ")
                        print(new_df)
                        choice = int(input(self.select_round_airline))

                elif(choice == 3):
                    min_price = input("Enter the min price you accept: ")
                    max_price = input("Enter the max price you accept: ")

                    if(int(max_price) > int(min_price)):   
                        new_df = self.price_option(new_df,int(max_price),int(min_price))
                        if(new_df.shape[0] == 1):
                            break
                        elif(new_df.empty):
                            new_df = df.copy()
                            print("Can't find data of price between %s and %s, please filter again!"%(min_price,max_price))
                            print("Flights")
                            print(new_df)
                            choice = int(input(self.select_round_airline))
                        elif(min_price == '0' or max_price == '0'):
                            break
                        else:
                            print("After select the price range you prefer, the searching result is: ")
                            print(new_df)
                            choice = int(input(self.select_round_airline))
                    else:
                        print("The price range is invalid. Please enter again!")
                


            except Exception as e:
                print(e)
                print("Your search is invalid. Please enter again!")
                pass
        return new_df
