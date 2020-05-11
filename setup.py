import pandas as pd
import os
from glob import glob
import shutil
from datetime import datetime
from ftplib import FTP
now = datetime.now()
now = now.strftime("%d%m%Y%H%M%S")
now = str(now)
## Get current dir
current_dir = os.path.dirname(os.path.realpath(__file__))
#Get all csv
find_csv = sorted(glob('*.csv'))
#Merge files
csv_file=pd.concat((pd.read_csv(file,parse_dates=['sTime']).assign(filename=file)
           for file in find_csv), ignore_index=True)
#Looking to csv files and copy them to old then remove the original
for filename in os.listdir(current_dir):
    if filename.endswith(('csv')):
        if not os.path.exists('old'):
            os.mkdir('old')
        shutil.copy(filename,'old')
        os.remove(filename)
        print(filename+ ' File is moved')
#Add hours col
csv_file['hours'] = csv_file.sTime.dt.hour
#check In
csv_file['checktype'] ="I"
x=csv_file.loc[csv_file.hours >= 12, :]
x.to_csv('chkin'+now+'.csv')
#check OUT
csv_file['checktype'] ='O'
x = csv_file.loc[csv_file.hours < 12, :]
x.to_csv('chkout'+now+'.csv')
#Read all csv
find_csv = sorted(glob('*.csv'))
csv_file=pd.concat((pd.read_csv(file).assign(filename=file)
           for file in find_csv), ignore_index=True)
#Looking to csv files and copy them to chk then remove the original
for filename in os.listdir(current_dir):
    if filename.endswith(('csv')):
        if not os.path.exists('chk'):
            os.mkdir('chk')
        shutil.copy(filename,'chk')
        os.remove(filename)
        print(filename+' File is moved')
csv_file.drop(['Unnamed: 0'], axis=1, inplace=True)
csv_file.to_csv('final'+now+'.csv')
#Looking to csv files and copy them to final then remove the original
for filename in os.listdir(current_dir):
    if filename.endswith(('csv')):
        if not os.path.exists('final'):
            os.mkdir('final')
        shutil.copy(filename,'final')
        os.remove(filename)
        print(filename +' File is moved')
        # FTP config
        ftpdir = current_dir+'\\final'
        host = ''
        port = 2112
        ftp = FTP()
        conn = ftp.connect (host,port)
        ftp.login('Username', 'password')
        ffile = str(ftpdir+'\\'+filename)
        #FTP Upload
        with open(ffile, "rb") as f:
            upload = ftp.storbinary('STOR ' + os.path.basename(ffile), f)
            f.close()
            if upload:
                print('File '+filename+ '  is uploaded')
                #Move uploaded file to up and remove the original
                for ffile in os.listdir(ftpdir):
                    print(ftpdir)
                    if not os.path.exists('final/up'):
                        os.mkdir('final/up')
                    shutil.copy(ftpdir+'\\'+filename, 'final/up')
                    os.remove(ftpdir+'\\'+filename)
                    print('File '+filename+ ' moved to up')
            else:
                print('Upload ERROR')

