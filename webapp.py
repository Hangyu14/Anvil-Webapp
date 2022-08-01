
import numpy as np
import webbrowser
import pandas as pd
import os
import io
import datetime
from matplotlib import pyplot as plt
import anvil.mpl_util
import anvil.pdf
import anvil.media


import anvil.server
anvil.server.connect("server_54AGEMOLPZMGKERYU6ZUOAPQ-JBNBF6UC2YUUSXZN")
app_link = 'https://JBNBF6UC2YUUSXZN.anvil.app/EFZRRF2I5MDNKUOIEXWQ266I'

webbrowser.open(app_link)

# get the drop down list of authors
@anvil.server.callable
def get_author():   
    # read data from CMATRIX.DAT
    cmatrix = pd.read_csv('DATA/CMATRIX.DAT',encoding='latin-1',sep='\t',header=None)
    Header=['counter','test number','Author','w/c', 'a/c', 'c', 'cem','SiO2','FlyAsh','WR (kg)','Re (kg)','AEA (kg)',
                'fc28','E28', 'Geometry','2A/u', "te",'H0',"t'",'T', 'Heat','RH_test','sigma/fct0', 'sigma','J_ue','Region',
                'Year','File']
    # set the header of dataframe for later searching
    cmatrix = pd.DataFrame(cmatrix.values[2:], columns= Header)
    cmatrix.drop(cmatrix.columns[0],axis=1,inplace=True)
    cmatrix.reset_index(drop=True,inplace=True)

    # get the author list
    authorlist = cmatrix['Author'].to_list()
    # remove duplicate authors
    authorlist1 = []
    for item in authorlist:
        if not item in authorlist1:
            authorlist1.append(item)
    # set the first element of drop dowm menu as "please select"
    authorlist1.insert(0,'please select')

    return authorlist1

# get the drop down list of files
@anvil.server.callable
def get_file(selected_para1,selectedvalue_para1,selected_para2,min_para2,max_para2):
    # read data from CMATRIX.DAT
    cmatrix = pd.read_csv('DATA/CMATRIX.DAT',encoding='latin-1',sep='\t',header=None)
    Header=['counter','test number','Author','w/c', 'a/c', 'c', 'cem','SiO2','FlyAsh','WR (kg)','Re (kg)','AEA (kg)',
                'fc28','E28', 'Geometry','2A/u', "te",'H0',"t'",'T', 'Heat','RH_test','sigma/fct0', 'sigma','J_ue','Region',
                'Year','File']
    # set the header of dataframe for later searching
    cmatrix = pd.DataFrame(cmatrix.values[2:], columns= Header)
    cmatrix.drop(cmatrix.columns[0],axis=1,inplace=True)
    cmatrix.reset_index(drop=True,inplace=True)

    # get the file list based on parameter1's value and parameter2's range
    column_para2 = cmatrix[selected_para2]
    column_para2 = pd.to_numeric(column_para2, errors='coerce')
    file1 = cmatrix.loc[cmatrix[selected_para1] == selectedvalue_para1]
    file2 = file1.loc[(min_para2 <= file1[selected_para2]) & (file1[selected_para2] <= max_para2)]
    filelist = file2['File'].to_list()

    filelist.insert(0,'please select')
    return filelist


# get drop down menu of selected parameter1
@anvil.server.callable
def get_para1_value(selected_para1):
    # read data from CMATRIX.DAT
    cmatrix = pd.read_csv('DATA/CMATRIX.DAT',encoding='latin-1',sep='\t',header=None)
    Header=['counter','test number','Author','w/c', 'a/c', 'c', 'cem','SiO2','FlyAsh','WR (kg)','Re (kg)','AEA (kg)',
                'fc28','E28', 'Geometry','2A/u', "te",'H0',"t'",'T', 'Heat','RH_test','sigma/fct0', 'sigma','J_ue','Region',
                'Year','File']
    # set the header of dataframe for later searching
    cmatrix = pd.DataFrame(cmatrix.values[2:], columns= Header)
    cmatrix.drop(cmatrix.columns[0],axis=1,inplace=True)
    cmatrix.reset_index(drop=True,inplace=True)
    # replace k.A. with -1
    cmatrix = cmatrix.replace(to_replace='k.A.', value='-1')

    # get values of parameter1
    para1list = cmatrix[selected_para1].to_list()
    # remove duplicate values
    para1_list = []
    for item in para1list:
        if not item in para1_list:
            para1_list.append(item)
    para1_list.insert(0,'please select')
    return para1_list

# get range of selected parameter2
@anvil.server.callable
def get_para2_range(selected_para2):
    # read data from CMATRIX.DAT
    cmatrix = pd.read_csv('DATA/CMATRIX.DAT',encoding='latin-1',sep='\t',header=None)
    Header=['counter','test number','Author','w/c', 'a/c', 'c', 'cem','SiO2','FlyAsh','WR (kg)','Re (kg)','AEA (kg)',
                'fc28','E28', 'Geometry','2A/u', "te",'H0',"t'",'T', 'Heat','RH_test','sigma/fct0', 'sigma','J_ue','Region',
                'Year','File']
    # set the header of dataframe for later searching
    cmatrix = pd.DataFrame(cmatrix.values[2:], columns= Header)
    cmatrix.drop(cmatrix.columns[0],axis=1,inplace=True)
    cmatrix.reset_index(drop=True,inplace=True)
    # replace k.A. with -1
    cmatrix = cmatrix.replace(to_replace='k.A.', value='-1')
    # get range of parameter2
    column_para2 = cmatrix[selected_para2]
    column_para2 = pd.to_numeric(column_para2, errors='coerce')
    max_value = column_para2.max()
    min_value = column_para2.min()

    Range = 'The range of selected parameter 2 is: '+ str(min_value) + '-' + str(max_value)
    return str(Range)
    

# get the data for plot
@anvil.server.callable
def get_plotdata(selectedfile):
    # get plot data from local files
    filepath = 'DATA/'+ selectedfile + '.DAT'
    plotdata = pd.read_csv(filepath,skiprows=1,sep='\t',header=None)
    return plotdata.to_numpy()


# get the figure of selected files
@anvil.server.callable
def get_plot(file_list):
    # set the basic parameters of the figure
    plt.switch_backend('Agg')
    plt.figure(1, figsize=(15,9))
    plt.title('Plot of selected files', fontweight='bold')
    plt.xlabel('Time', fontweight='bold')
    plt.ylabel('Value of E', fontweight='bold')
    # plot different selected files in one figure
    for file in file_list:
        filepath = 'DATA/'+ file + '.DAT'
        plotdata = pd.read_csv(filepath,skiprows=1,sep='\t',header=None)
        plt.plot(plotdata[0], plotdata[1], label = 'line of ' + file, marker="x")
        plt.legend()
    #plt.savefig('test.png')
    return anvil.mpl_util.plot_image()



# write the information from interface to txt file in local computer
@anvil.server.callable
def generate_report(selected_para1,selectedvalue_para1,selected_para2,min_para2,max_para2,selected_files):

    # generate infomation from webapp
    parameter_info_para1 = 'Selected Parameter 1 is: ' + selected_para1 +'. ' + "And it's value is: " + selectedvalue_para1 + '. '+ "\r\n"
    parameter_info_para2 = 'Selected Parameter 2 is: ' + selected_para2 +'. ' + "And it's range is: " + min_para2 + '-' + max_para2 + '. '+ "\r\n"
    fileinfo = 'Selected files are: '
    for file in selected_files:
        fileinfo +=  file + ', '


    # generate non-duplicated file name
    if os.path.exists('report/txt') == False:
        os.mkdir('report/txt')
    k = 1
    time = datetime.datetime.now()
    save_path = 'report/txt/report_'+ str(time.year) + str(time.month) + str(time.day) + '_' +  str(k) +'.txt'
    while os.path.isfile(save_path):
        while True:
            k += 1
            save_path1 = 'report/txt/report_'+ str(time.year) + str(time.month) + str(time.day) + '_' +  str(k) +'.txt'
            if os.path.isfile(save_path1):
                continue
            else:
                save_path = save_path1
                break
    
    # generate non-duplicated file name
    if os.path.exists('report/figure') == False:
        os.mkdir('report/figure')
    m = 1
    time = datetime.datetime.now()
    fig_path = 'report/figure/plot_'+ str(time.year) + str(time.month) + str(time.day) + '_' +  str(m) +'.png'
    while os.path.isfile(fig_path):
        while True:
            m += 1
            fig_path1 = 'report/figure/plot_'+ str(time.year) + str(time.month) + str(time.day) + '_' +  str(m) +'.png'
            if os.path.isfile(fig_path1):
                continue
            else:
                fig_path = fig_path1
                break
    
    # write the info from webapp to txt file
    with open(save_path, 'w+') as f:
        f = io.StringIO()
        f.write(parameter_info_para1)
        f.write(parameter_info_para2)
        f.write(fileinfo)
        #contents = f.getvalue().encode()
        #text_file = anvil.BlobMedia(content_type="text/plain", contents=contents, name="text_file.txt")
    f.close()
    contents = parameter_info_para1+parameter_info_para2+fileinfo
    

    # save generated plot
    plt.switch_backend('Agg')
    plt.figure(1, figsize=(15,9))
    plt.title('Plot of selected files', fontweight='bold')
    plt.xlabel('Time', fontweight='bold')
    plt.ylabel('Value of E', fontweight='bold')

    for file in selected_files:
        filepath = 'DATA/'+ file + '.DAT'
        plotdata = pd.read_csv(filepath,skiprows=1,sep='\t',header=None)
        plt.plot(plotdata[0], plotdata[1], label = 'line of ' + file, marker="x")
        plt.legend()
    plt.savefig(fig_path)
    return contents



anvil.server.wait_forever()
