"""
Andrey Purwanto - 67659

"""
from fastapi import FastAPI, HTTPException
import pandas as pd
import numpy as np
import glob
from datetime import datetime

app = FastAPI()


def read_all_csv(csv_folder = 'csv_files'):
    """read all csv in folder files
    params:
    csv_folder : str
    "target folder"

    return:
    dict
    "if status = 200, return['df'] is concat df inside csv_folder,"
    "if error, return['status'] is error status, return['message'] is message " 
    """
    try:
        list_pd = []
        for file_ in glob.glob(csv_folder+"/*.csv"):
            df = pd.read_csv(file_)
            df.dropna(inplace=True)
            list_pd.append(df)
        df_concat = pd.concat(list_pd)
        df_concat['tanggal'] = pd.to_datetime(df_concat['tanggal'], format='%Y-%m-%d', errors='coerce')
        return {'status':200,'df':df_concat[df_concat['kecamatan'] !='BELUM DIKETAHUI']}
    except (Exception):
        return {'status':400,'message':'no csv found'}

def to_date(x):
    """input str to datetime
    ex x = '20200401'
    to datetime yyyymmdd
    """
    year = x[:4]
    month = x[4:6]
    date = x[6:8]
    return {'year':int(year), 'month':int(month), 'date':int(date)}

def slice_by_tanggal_kecamatan(df,initialdate='20200101',enddate='20201212',kecamatan_='all'):
    """read all csv in folder files
    params:
    df : dataframe
    "dataframe after concat"
    initialdate : str
    "input date in str yyyymmdd"
    enddate : str
    "input date in str yyyymmdd"
    kecamatan_ : str
    "input kecamatan"

    return:
    dict
    "if status = 200, return['df'] is slicing result in df, return['initialdate'] is initial date in datetime, return['enddate'] is end date in datetime, return['kecamatan'] is kecamatan"
    "if error, return['status'] is error status, return['message'] is message " 
    """
    try:
        if enddate == '':
            enddate=initialdate
        initialdate = (int(to_date(initialdate)['year']),int(to_date(initialdate)['month']),int(to_date(initialdate)['date']))
        enddate = (int(to_date(enddate)['year']),int(to_date(enddate)['month']),int(to_date(enddate)['date']))   
        if kecamatan_ == 'all':
            df2 = df[(df.tanggal >= datetime(*initialdate)) & (df.tanggal <= datetime(*enddate))]
        else:
            list_kecamatan = kecamatan_.split(",")
            df2 = df[(df.tanggal >= datetime(*initialdate)) & (df.tanggal <= datetime(*enddate)) & (df.kecamatan.isin(list_kecamatan))]
        df2  = df2.sort_values(by=['tanggal']).reset_index(drop=True)
        return {'status':200,'df' : df2, 'initialdate':str(df2.head(1).reset_index(drop=True).tanggal[0]), 'enddate':str(df2.tail(1).reset_index(drop=True).tanggal[0]), 'kecamatan':kecamatan_}
    except (Exception):
        return {'status':412,'message':'invalid input'}


def percentage_calc(initial,end):
    """return nan if divide by zero, else return ((end-initial)/initial)*100"""
    if initial == 0:
        return np.nan
    else:
        return ((end-initial)/initial)*100

def expand_input_top_rank(x):
    """create list of input str ex: 1 or 1-5
    params:
    x : str
    "ex 1 or 1-5"

    return:
    dict
    "if status = 200, return['return'] is list of int ex input 1 will become [0,1] input 1-5 will become [1,5]"
    "if error, return['status'] is error status, return['message'] is message " 
    """
    try:
        list_x = x.split('-')
        if len(list_x) == 1:
            return {'status' : 200, 'return' : [0,int(list_x[0])]}
        elif len(list_x) == 2:
            print('aaaaa')
            return {'status' : 200, 'return' : [int(list_x[0]),int(list_x[1])]}
        else:
            return {'status' : 412, 'message' : 'invalid input top rank'}
    except (Exception) as e:
        print(e)
        return {'status' : 412, 'message' : 'invalid input top rank'}

def expand_input_sort_by(df_temp,ascending_,sort_by):
    """sort df with input sort_by and ascending
    0 sort by kecamatan
    1 sort by positif_selisih_nilai
    2 sort by positif_selisih_persentase
    3 sort by sembuh_selisih_nilai
    4 sort by sembuh_selisih_persentase
    5 sort by meninggal_selisih_nilai
    6 sort by meninggal_selisih_persentase
    
    params:
    params:
    df : dataframe
    "dataframe"
    sort_by : str
    "0-6 refer to columns from the left"
    ascending_ : str
    "0 or 1"

    return:
    dict
    "if status = 200, return['df'] is df temp sorted"
    "if error, return['status'] is error status, return['message'] is message " 
    """
    try:
        if ((int(ascending_) != 0) and (int(ascending_) != 1)):
            return {'status' : 412, 'message' : 'invalid input ascending_'}        
        if int(sort_by) == 1: 
            df_temp = df_temp.sort_values(by=['positif_selisih_nilai'],ascending=int(ascending_)).reset_index(drop=True)
            sort_by = 'positif_selisih_nilai'
            return {'status' : 200, 'df' : df_temp, 'sort_by':sort_by}
        elif int(sort_by) == 2: 
            df_temp = df_temp.sort_values(by=['positif_selisih_persentase'],ascending=int(ascending_)).reset_index(drop=True)
            sort_by = 'positif_selisih_persentase'
            return {'status' : 200, 'df' : df_temp, 'sort_by':sort_by}
        elif int(sort_by) == 3: 
            df_temp = df_temp.sort_values(by=['sembuh_selisih_nilai'],ascending=int(ascending_)).reset_index(drop=True)
            sort_by = 'sembuh_selisih_nilai'
            return {'status' : 200, 'df' : df_temp, 'sort_by':sort_by}
        elif int(sort_by) == 4: 
            df_temp = df_temp.sort_values(by=['sembuh_selisih_persentase'],ascending=int(ascending_)).reset_index(drop=True)
            sort_by = 'sembuh_selisih_persentase'
            return {'status' : 200, 'df' : df_temp, 'sort_by':sort_by}
        elif int(sort_by) == 5: 
            df_temp = df_temp.sort_values(by=['meninggal_selisih_nilai'],ascending=int(ascending_)).reset_index(drop=True)
            sort_by = 'meninggal_selisih_nilai'
            return {'status' : 200, 'df' : df_temp, 'sort_by':sort_by}
        elif int(sort_by) == 6: 
            df_temp = df_temp.sort_values(by=['meninggal_selisih_persentase'],ascending=int(ascending_)).reset_index(drop=True)
            sort_by = 'meninggal_selisih_nilai'
            return {'status' : 200, 'df' : df_temp, 'sort_by':sort_by}
        elif int(sort_by) == 0:  
            df_temp = df_temp.sort_values(by=['kecamatan'],ascending=int(ascending_)).reset_index(drop=True)
            sort_by = 'kecamatan'
            return {'status' : 200, 'df' : df_temp, 'sort_by':sort_by}
        else:
            return {'status' : 412, 'message' : 'invalid input sort_by'}
    except (Exception) as e:
        print(e)
        return {'status' : 412, 'message' : 'invalid input sort_by'}

def difference(df,kecamatan,sort_by,ascending_,top_rank):
    """read all csv in folder files
    params:
    df : dataframe
    "dataframe after slicing"
    sort_by : str
    "0-6 refer to columns from the left"
    ascending_ : str
    "0 or 1"
    top_rank : str
    "ex 1-5 or 1 "

    return:
    dict
    "if status = 200, return['df'] is 
    dict_result = {
            'query' : {
                'tanggal_awal':str(initialdate),
                'tanggal_akhir':str(enddate), 
                'kecamatan' :str(kecamatan),
                'sort_by' : str(sort_by),
                'ascending_' : int(ascending_),
                'top_rank' : str(top_rank)
                }
            'data' : "data": {
                "1": {
                "kecamatan": "TANJUNG PRIOK",
                "positif_selisih_nilai": 287,
                "positif_selisih_persentase": 5740,
                "sembuh_selisih_nilai": 67,
                "sembuh_selisih_persentase": 6700,
                "meninggal_selisih_nilai": 26,
                "meninggal_selisih_persentase": "undefined"
                },
                "2": {
                "kecamatan": "TANAH ABANG",
                "positif_selisih_nilai": 336,
                "positif_selisih_persentase": 8400,
                "sembuh_selisih_nilai": 85,
                "sembuh_selisih_persentase": 4250,
                "meninggal_selisih_nilai": 17,
                "meninggal_selisih_persentase": "undefined"
                }}
            }
    
    "
    "if error, return['status'] is error status, return['message'] is message " 
    """
    try:
        temp_list = []
        for kecamatan_ in df['kecamatan'].unique():
            df_temp = df[df.kecamatan == kecamatan_]
            temp = []
            temp.append(kecamatan_)
            temp.append(int(df_temp.tail(1).positif) - int(df_temp.head(1).positif))
            temp.append(percentage_calc(int(df_temp.head(1).positif),int(df_temp.tail(1).positif)))
            temp.append(int(df_temp.tail(1).sembuh) - int(df_temp.head(1).sembuh))
            temp.append(percentage_calc(int(df_temp.head(1).sembuh),int(df_temp.tail(1).sembuh)))
            temp.append(int(df_temp.tail(1).meninggal) - int(df_temp.head(1).meninggal))
            temp.append(percentage_calc(int(df_temp.head(1).meninggal),int(df_temp.tail(1).meninggal)))
            temp_list.append(temp)
        initialdate = str(str(df_temp.head(1).reset_index(drop=True).tanggal[0]))
        enddate = str(str(df_temp.tail(1).reset_index(drop=True).tanggal[0]))
        df_temp = pd.DataFrame(temp_list,columns=['kecamatan','positif_selisih_nilai','positif_selisih_persentase','sembuh_selisih_nilai','sembuh_selisih_persentase','meninggal_selisih_nilai','meninggal_selisih_persentase'])
        return_sort_by = expand_input_sort_by(df_temp,ascending_,sort_by)
        if return_sort_by['status'] == 200:
            df_temp = return_sort_by['df']
            sort_by = return_sort_by['sort_by']
        else:
            return {'status' : return_sort_by['status'], 'message' : return_sort_by['message']}
        return_top_rank = expand_input_top_rank(top_rank)
        if return_top_rank['status'] == 200:
            if int(return_top_rank['return'][1]) < len(df_temp):
                df_temp = df_temp.loc[((return_top_rank['return'])[0]-1): ((return_top_rank['return'])[1]-1)]
            else:
                df_temp = df_temp.loc[((return_top_rank['return'])[0]-1):(len(df_temp)-1)]
        else:
            return {'status' : return_top_rank['status'], 'message' : return_top_rank['message']}
        df_temp.fillna('undefined', inplace=True)
        dict_result = {
            'query' : {
                'tanggal_awal':str(initialdate),
                'tanggal_akhir':str(enddate), 
                'kecamatan' :str(kecamatan),
                'sort_by' : str(sort_by),
                'ascending_' : int(ascending_),
                'top_rank' : str(top_rank)
                }
            }
        
        dict_result['data'] = df_temp.to_dict('index')
        return {'status' : 200, 'return' : dict_result}
    except (Exception) as e:
        print(e)
        return {'status' : 412, 'message' : 'invalid input'}

@app.get("/")
def read_item():
    """return active endpoint"""
    return {'1':'/selisih/','2':'/pilihdata/'}
  
@app.get("/selisih/")
async def selisih(initialdate: str = '20200325', enddate: str = '20200603', kecamatan_: str = 'all', sort_by: str = '1', ascending_: str = '0', top_rank: str = "10"):
    """
    return analysis with differences between initial and end date with parameters of : initialdate, enddate, kecamatan_, sort_by, ascending_, top_rank
    """
    return_read_csv = read_all_csv()
    if return_read_csv['status'] == 200:
        df_concat = return_read_csv['df']
    else:
        raise HTTPException(
            status_code=return_read_csv['status'],
            detail=return_read_csv['message']
        )

    dict_sliced = slice_by_tanggal_kecamatan(df_concat,kecamatan_=kecamatan_,initialdate=initialdate,enddate=enddate)
    if dict_sliced['status'] != 200:
        raise HTTPException(
            status_code=dict_sliced['status'],
            detail=dict_sliced['message']
        )

    result = difference(dict_sliced['df'],dict_sliced['kecamatan'],sort_by,ascending_,top_rank)
    if result['status'] == 200:
        return result['return']
    else:
        raise HTTPException(
            status_code=result['status'],
            detail=result['message']
        )

@app.get("/pilihdata/")
async def pilihdata(initialdate: str = '20200401', enddate: str = '20200401', kecamatan_: str = 'all'):
    """
    return sliced data with parameters of : initialdate, enddate, kecamatan_
    """
    return_read_csv = read_all_csv()
    if return_read_csv['status'] == 200:
        df_concat = return_read_csv['df']
    else:
        raise HTTPException(
            status_code=return_read_csv['status'],
            detail=return_read_csv['message']
        )
    dict_sliced = slice_by_tanggal_kecamatan(df_concat,kecamatan_=kecamatan_,initialdate=initialdate,enddate=enddate)
    if dict_sliced['status'] == 200:
        return {'query' : {'kecamatan':dict_sliced['kecamatan'],'initialdate' : dict_sliced['initialdate'], 'enddate': dict_sliced['enddate']},'data ': dict_sliced['df'].to_dict('index')}
    else:
        raise HTTPException(
            status_code=dict_sliced['status'],
            detail=dict_sliced['message']
        )
