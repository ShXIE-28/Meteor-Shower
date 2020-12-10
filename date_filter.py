# -*- coding: utf-8 -*-
"""
date filter

@author: shuhui
"""
# check whether date contains letter
def contain_alpha(date):
    for i in date:
        if True == i.isalpha():
            return True
    return False


# change the date input into standard format
def date_standard(date):
    
    temp = date.split("/")
    m = int(temp[0])
    d = int(temp[1])
    y = int(temp[2])
    string = str(m)+"/"+str(d)+"/"+str(y)
    
    return string
    

# filter records when using date filter(change date into standard format first)
def date_filter(dt,date_list,date_s,date_e):
    
    id_s = date_list[date_list['Date']==date_s].index[0]
    id_e = date_list[date_list['Date']==date_e].index[0]
    
    if (id_e < id_s):
        temp = id_e
        id_e = id_s
        id_s = temp
    
    dt_list = date_list.loc[id_s:(id_e+1),'Date'].to_list()
    dt['tf'] = dt['Start Date'].apply(lambda x:x in dt_list)
    dt = dt[dt['tf']==True]
    del dt['tf']
    
    return dt
        
    