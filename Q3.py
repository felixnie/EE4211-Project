# -*- coding: utf-8 -*-
"""
Created on Sun Nov  8 14:13:25 2020

@author: Jie
"""

### EE4211 Project - Question 1

# Group name: WeUsOurs (Group No.26)

# Group members: Liu Tianshu, Nie Hongtuo, Pan Jie, Zhang Chenxi

# The whole code takes ~3 mins to finish running.

# Please read our annotations while running the code:)

## Question 1.1 - Part 1 Calculate house number

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import seaborn as sns

# First of all, let's take a look inside the dataset. Then we can get the number and meter IDs of all the houses.

df = pd.read_csv('D:/Work/NUS/EE4211/Project/dataport-export_gas_oct2015-mar2016.csv')
grouped = df.groupby(['dataid'])
len(grouped)
keys = pd.Series(df.dataid.values)
keys = keys.unique()
keys = np.sort(keys)


def find_decrease(df):
    grouped = df.groupby(['dataid'])
    decrease_meter_id = []
    for key,group in grouped:
        val = group.meter_value.values
        diff = np.diff(val)
        decrease_time_id = np.where(diff < 0)[0] + 1
        if len(decrease_time_id):
            decrease_meter_id.append(key)
            decrease_time = group.localminute.values[decrease_time_id]
            print('The glitches of gas meter No.', key, 'happened in the moments below:\n')
            print(decrease_time, '\n')
    return decrease_meter_id


def plot_group(key,df):
    grouped = df.groupby(['dataid'])
    group = grouped.get_group(key)
    t = group.localminute.values
    val = group.meter_value.values
    # keep the date
    t = map(lambda s : s[0:10], t)
    t = np.array(list(t))
    
    s = pd.Series(val, index=t)
    s.plot(figsize=(16, 8))
    plt.rcParams['figure.dpi'] = 300
    plt.xticks(rotation=-20)
    plt.title('Gas Meter No.' + str(key))
    return



def time_interval(time1,time2):
    year1 = int(time1[:4])
    year2 = int(time2[:4])
    month1 = int(time1[5:7])
    month2 = int(time2[5:7])
    day1 = int(time1[8:10])
    day2 = int(time2[8:10])
    hour1 = int(time1[11:13])
    hour2 = int(time2[11:13])
    interval = hour2-hour1 + 24*(day2-day1) + 24*30*(month2-month1) + 24*30*12*(year2-year1)
    return interval



def long_time_no_update(List,interval_hours):
    
    IDnum = len(List)
    List_unchanged_id = []
    List_unchanged_time = []
    for i in range(IDnum):
        idnum = len(List[i][1])
        unchanged_time = []
        for j in range(idnum-1):
            t1 = List[i][1].iat[j,0]
            t1 = t1[:19]
            t2 = List[i][1].iat[j+1,0]
            t2 = t2[:19]
            if time_interval(t1,t2) > interval_hours:
                unchanged_time.append([t1,t2])
        if unchanged_time != []:
            List_unchanged_id.append(List[i][0])
            List_unchanged_time.append(unchanged_time)
    return [List_unchanged_id,List_unchanged_time]




def find_decrease_details(df):
    decrease_details = []
    grouped = df.groupby(['dataid'])
    for key,group in grouped:
        val = group.meter_value.values
        diff = val[1:] - val[:-1]
        decrease_time_id = np.where(diff < 0)[0] + 1
        if len(decrease_time_id):
            for id in decrease_time_id:
                decrease_details.append([key, id, val[id-3], val[id-2], val[id-1], val[id], val[id+1]])
    labels = ['Gas Meter ID', 'Sample ID', 'ID - 3','ID - 2', 'ID - 1', 'ID + 0', 'ID + 1']
    decrease_details_df = pd.DataFrame(decrease_details, columns=labels)
    return decrease_details_df



def rectify(df):
    grouped = df.groupby(['dataid'])
    for key,group in grouped:
        val = group.meter_value.values
        diff = val[1:] - val[:-1]
        defect_time = np.where(diff < 0)[0] + 1
        if len(defect_time):
            for i in range(1,len(val)):
                if val[i] > val[-1]:
                    val[i] = val[i - 1]
                elif val[i] < val[i - 1]:
                    val[i] = val[i - 1]
            df.loc[df['dataid'] == key, 'meter_value'] = val
    return df

df = rectify(df)
rec_df = df



defect_id = find_decrease(df)
len(defect_id)


def local2utc(time):
    return pd.Timestamp(time)
df.localminute = df.apply(lambda r: local2utc(r.localminute), axis=1)

def select_data(df, month) -> pd.DataFrame:
    column_names = df.columns.values
    values = df.values
    values = filter(lambda x: x[0].month == month, values)
    values = pd.DataFrame(values)
    for i in range(len(column_names)):
        values = values.rename(columns={i:column_names[i]})
    return values

# select Oct data
month_data = select_data(df, 10)
month_data

def hourly_data_by_group(df, month) -> set():
    month_dict = {1:31,2:28,3:31,4:30,5:31,6:30,7:31,8:31,9:30,10:31,11:30,12:31}
    groups = df.groupby(['dataid'], sort=['localminute'])
    processed_group = {}
    for key in groups.groups.keys():
        new_group = []
        current_group = groups.get_group(key).values
        # init_first_point
        first_point = current_group[0]
        first_point[0] = first_point[0].replace(day = 1, hour = 0, minute = 0, second = 0)
        index_current_group = 0
        tmp = []
        # replace all time on the hour
        for row in current_group:
            row[0] = row[0].replace(minute = 0, second = 0)
            tmp.append(row)
        current_group = tmp
        # interpolate data 24 hour for 30 day
        for day in range(1, month_dict[month] + 1):
            for hour in range(0, 24):
                # make sure its the last data of the current time
                while (True):
                    if (index_current_group >= len(current_group)):
                        break
                    current_row = current_group[index_current_group]
                    time = current_row[0]
                    if (time.day == day and time.hour == hour):
                        index_current_group += 1
                    else:
                        break
                # assign data
                current_row = current_group[index_current_group - 1]
                time = current_row[0]
                date = pd.Timestamp(year = time.year, month = time.month, day = time.day, hour = time.hour, minute = 0, second = 0)
                current_row = [date, current_row[1], current_row[2]]
                if (time.day == day and time.hour == hour):
                    if (len(new_group) > 0 and new_group[-1][0].day == day and new_group[-1][0].hour == hour):
                        new_group[-1] = current_row
                    else:
                        new_group.append(current_row)
                else:
                    date = pd.Timestamp(year = time.year, month = time.month, day = day, hour = hour, minute = 0, second = 0)
                    row = [date,new_group[-1][1],new_group[-1][2]]
                    new_group.append(row)
        processed_group[key] = new_group
    return processed_group



import calendar

def to_data_frame(data_list):
    labels = ['localminute', 'dataid', 'meter_value']
    df = pd.DataFrame(data_list, columns=labels)
    return df

def plot_month(key,month,df):
    month_data = select_data(df, month)
    hourly_data_groups = hourly_data_by_group(month_data, month)
    month_df = to_data_frame(hourly_data_groups[key])
    
    grouped = month_df.groupby(['dataid'])
    group = grouped.get_group(key)
    t = group.localminute.values
    val = group.meter_value.values
    
    s = pd.Series(val, index=t)
    s.plot(figsize=(16, 8))
    plt.xticks(rotation=-20)
    plt.title('Gas Meter No.' + str(key) + ' in ' + calendar.month_name[month])
    return

# set the key and month as you like

month = 10 # data from Oct
#key = 35 # gas meter no.35
#plot_month(key,month,df)



def hourly_range_month(df, start_month, end_month):
    month_dict = {1:31,2:28,3:31,4:30,5:31,6:30,7:31,8:31,9:30,10:31,11:30,12:31}
    groups = df.groupby(['dataid'], sort=['localminute'])
    processed_group = {}
    for key in groups.groups.keys():
        new_group = []
        current_group = groups.get_group(key).values
        # init_first_point
        first_point = current_group[0]
        first_point[0] = first_point[0].replace(month = start_month, day = 1, hour = 0, minute = 0, second = 0)
        index_current_group = 0
        tmp = []
        # replace all time on the hour
        for row in current_group:
            row[0] = row[0].replace(minute = 0, second = 0)
            tmp.append(row)
        current_group = tmp
        # interpolate data 24 hour for 30 day
        for month in range(start_month, end_month + 1):
            month = month % 12 if month % 12 != 0 else 12 
            for day in range(1, month_dict[month] + 1):
                for hour in range(0, 24):
                    # make sure its the last data of the current time
                    while (True):
                        if (index_current_group >= len(current_group)):
                            break
                        current_row = current_group[index_current_group]
                        time = current_row[0]
                        if (time.month == month and time.day == day and time.hour == hour):
                            index_current_group += 1
                        else:
                            break
                    # assign data
                    current_row = current_group[index_current_group - 1]
                    time = current_row[0]
                    date = pd.Timestamp(year = time.year, month = time.month, day = time.day, hour = time.hour, minute = 0, second = 0)
                    current_row = [date, current_row[1], current_row[2]]
                    if (time.month == month and time.day == day and time.hour == hour):
                        if (len(new_group) > 0 and new_group[-1][0].month == month and new_group[-1][0].day == day and new_group[-1][0].hour == hour):
                            new_group[-1] = current_row
                        else:
                            new_group.append(current_row)
                    else:
                        date = pd.Timestamp(year = time.year, month = month, day = day, hour = hour, minute = 0, second = 0)
                        row = [date,new_group[-1][1],new_group[-1][2]]
                        new_group.append(row)
        processed_group[key] = new_group
    return processed_group

# 10 means Oct 2015, 15 means (12 + 3) => March Next Year(2016)
hourly_data_raw = hourly_range_month(df,10,15)



def hourly_data_matrix(hourly_data_raw, keys):
    hourly_data = np.zeros((157, 4368), dtype=int)
    for i in range(157):
        key = keys[i]
        monthly_value = hourly_data_raw[key]
        monthly_value = list(zip(*monthly_value))[2]
        monthly_value = np.array(monthly_value)
        hourly_data[i] = monthly_value

    return hourly_data

hourly_data = hourly_data_matrix(hourly_data_raw, keys)
hourly_data.shape
hourly_corr = np.corrcoef(hourly_data)
hourly_corr.shape
import datetime
df = pd.read_csv('D:/Work/NUS/EE4211/Project/dataport-export_gas_oct2015-mar2016.csv')
def rectify(df):
    
    grouped = df.groupby(['dataid'])
    for key,group in grouped:
        val = group.meter_value.values
        diff = val[1:] - val[:-1]
        defect_time = np.where(diff < 0)[0] + 1
        if len(defect_time):
            for i in range(1,len(val)):
                if val[i] > val[-1]:
                    val[i] = val[i - 1]
                elif val[i] < val[i - 1]:
                    val[i] = val[i - 1]
            df.loc[df['dataid'] == key, 'meter_value'] = val
    return df
df = rectify(df)
def local2utc(time):
    
    return pd.Timestamp(time)
df.localminute = df.apply(lambda r: local2utc(r.localminute), axis=1)
def hourly_origin(df):
    groups = df.groupby(['dataid'], sort=['localminute'])
    processed_group = {}
    for key in groups.groups.keys():
        new_group = []
        current_group = groups.get_group(key).values
        tmp = []
        for row in current_group:
            row[0] = row[0].replace(minute = 0, second = 0, microsecond = 0, nanosecond = 0)
            tmp.append(row)
        current_group = tmp
        # mean
        mean_group = []
        current_time = None
        current_number = 0
        current_count = 0
        for i in current_group:
            if current_time is None:
                current_time = i[0]
                current_number = i[2]
                current_count = 1
            elif current_time.year == i[0].year and current_time.month == i[0].month and current_time.day == i[0].day and current_time.hour == i[0].hour:
                current_number += i[2]
                current_count += 1
            else:
                mean_group.append([current_time, key, (current_number / current_count)])
                current_time = i[0]
                current_number = i[2]
                current_count = 1
        mean_group.append([current_time, key, (current_number / current_count)])
                
        processed_group[key] = mean_group
    return processed_group












# Q3, in this part, we will have a look at the similarity among meters
# based on some machine learing perspective.
# 2 of most classical ML clustering methods are K-means 
# and Gaussian mixture model(GMM)
# So we will do clustering based on these 2 methods and compare the result
# with correalation(Q1.3,top 5 correlated meters)




# to compare with the correlation pespective, we need to collect the top
# 5 correlated meters of each meter for later comparision


Top5 = []
for i in range(157):
    order = np.argsort(hourly_corr[i,:])
    #print('The top 5 relative families of consumer No.', keys[i], 'are:\t', keys[np.flip(order)[1:6]])
    top5 = [keys[i],keys[np.flip(order)[1:6]]]
    Top5.append(top5)
    
    
# you can see every meter and its corresponding top 5 correlated meters    
print(Top5)



# As each meter begins at different value, this may affect result of ML
# we first need to get the hourly usage data of each meter
# we still choose the hourly data from the same month

from sklearn.cluster import KMeans
from sklearn.mixture import GaussianMixture



if month >= 10:
    start_hour = (month - 10)*728
    end_hour = start_hour + 728 - 1
if month <10:
    start_hour = (month + 12 - 10)*728
    end_hour = start_hour + 728 - 1


hourly_data = hourly_data[:,start_hour:end_hour]

meter_num,hour_num = hourly_data.shape
hourly_usage = np.zeros(shape=(meter_num,hour_num))

for i in range(157):
    hourly_usage[i] = hourly_data[i] - hourly_data[i][0]   



# first let's have a looke at K-means
# by experiments, to set the number of clusters be 4 is proper
Clusters = 4

kmeans = KMeans(n_clusters=Clusters)
kmeans.fit(hourly_usage)
cluster = kmeans.predict(hourly_usage)
cluster = np.c_[cluster,keys]
Clus = []

for i in range(Clusters):
    idx = np.where(cluster[:,0] == i)
    l = cluster[idx[0]][:,1]
    Clus.append(list(l))
 
print(Clus)
YK = []
Not_match_num = 0
for i in range(len(Top5)):
    print('For meted id '+str(Top5[i][0])+':')
    Idx =  np.where(cluster[:,1] == Top5[i][0])
    label = cluster[Idx,0]
    No = []
    yk = []
    for j in Top5[i][1]:
        if j not in Clus[label[0][0]]:
            No.append(j)
            Not_match_num = Not_match_num + 1
        else:
            yk.append(j)
    YK.append(yk)
    if No == []:
        print('All its top 5 correlated meters are in the same clusters')
    else:
        print('The meter(s) is(are) of top 5 correlated but not the same cluster:')
        print(No)
    print('------------------------')


print('#################')
print('#################')
print('#################')
print(str(round(100-100*Not_match_num/(157*5),3))+
      '% of the K-means result can match with top 5 correlation')
    









# now let's try another method, GMM

GMM = GaussianMixture(n_components=Clusters,covariance_type='tied',reg_covar=0.1)
GMM.fit(hourly_usage)
cluster = GMM.predict(hourly_usage)
cluster = np.c_[cluster,keys]
Clus = []

for i in range(Clusters):
    idx = np.where(cluster[:,0] == i)
    l = cluster[idx[0]][:,1]
    Clus.append(list(l))
 
print(Clus)
YG = []
Not_match_num = 0
for i in range(len(Top5)):
    print('For meted id '+str(Top5[i][0])+':')
    Idx =  np.where(cluster[:,1] == Top5[i][0])
    label = cluster[Idx,0]
    No = []
    yg = []
    for j in Top5[i][1]:
        if j not in Clus[label[0][0]]:
            No.append(j)
            Not_match_num = Not_match_num + 1
        else:
            yg.append(j)
    YG.append(yg)
    if No == []:
        print('All its top 5 correlated meters are in the same clusters')
    else:
        print('The meter(s) is(are) of top 5 correlated but not the same cluster:')
        print(No)
    print('------------------------')


print('#################')
print('#################')
print('#################')
print(str(round(100-100*Not_match_num/(157*5),3))+
      '% of the GMM result can match with top 5 correlation')



# Now let's see after using correlation, K-means and GMM
# which meters still remain
# in other words, which meters are in the top 5 and can still
# lie in the same clusters based on K-means and GMM




The_same = []
for i in range(len(YG)):
    l = []
    l.append(cluster[i,1])
    if YG[i] != []:
        if YK[i]!= []:
            the_same = [x for x in YG[i] if x in YK[i]]
            if the_same != []:
                print('Based on correlation,K-means and GMM')
                print(cluster[i,1])
                print('and')
                print(the_same)
                print('are very closed')
                print(' ')
                l.append(the_same)
    The_same.append(l)
    
for i in range(157):
    if len(The_same[i]) == 1:
        The_same[i].append([])


TOP5 = []
ALL = []
for i in range(157):
    TOP5.append(Top5[i][1])
    ALL.append(The_same[i][1])

all_match = 0
for i in range(157):
    all_match = all_match + len(ALL[i])


print(str(round(100*Not_match_num/(157*5),3))+
      '% result of these 3 methods can match up')

    
# we can see that when we measure the similarity among meters through
# total different perspective, the result can still match a lot
# you can also see the summary table below  
    

    
    
    
meter_close = {'meterid':keys,'TOP5':TOP5,'K-means':YK,'GMM':YG,'all':ALL}
meter_close = pd.DataFrame(meter_close)

print(meter_close)









