# -*- coding: utf-8 -*-
"""
Created on Fri Apr 13 14:08:26 2018

@author: Lee
"""

#coding=utf-8
import requests
from bs4 import BeautifulSoup
import re
import string
import os
import time
import PyPDF2


def getHTMLText(url):
    try:
        kv={'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50'}
        r = requests.get(url,timeout=30,headers=kv)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return "error"

def getUrl(html):
    
    url = re.findall('/page.*?\.pdf',html)
    print(url)
    return url

def downloadUrl(url,root1):   
    kv={'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50'}
    for i in url:
        root=root1

        for j in i.split('/')[1:-2]:
            root = root + j+ '//'
            
        path = root+str(i).split('/')[-1]
        try:
            if not os.path.exists(root):
                os.makedirs(root)
            if not os.path.exists(path):
                urli='http://paper.people.com.cn/rmrb'+i
                r = requests.get(urli,timeout=30,headers=kv)
                with open(path,'wb') as f:
                    f.write(r.content)
                    f.close()
                    print(str(i).split('/')[-1]+" saved success!\n")
            else:
                print(str(i).split('/')[-1]+" already exists!\n")
        except:
            print(str(i).split('/')[-1]+" saved unsuccess!\n")
        time.sleep(0.1)
#    return root
    
def PDFMergeFun(root,pdflist,desLocation):
    os.chdir(root)
    print(desLocation)
    print(os.getcwd())
    pdfout=open(desLocation,"wb")
    pdfw=PyPDF2.PdfFileWriter()
    for i in pdflist:
        pdfFile=open(i,'rb')
        print('open '+i)
        pr=PyPDF2.PdfFileReader(pdfFile)
        
        for PageNum in range(pr.numPages):
            pdfw.addPage(pr.getPage(PageNum))
        print(pr.pageMode)

    pdfw.write(pdfout)
    pdfout.close()
    pdfFile.close()

def getFiles(root):
    for root,dirs,files in os.walk(root):
#        print(root)
#        print(dirs)
#        print(files)
        return root,files
    
def downloadMonthPaper():
    inMonth =int(input("please input 1-12 month for download:\n"))
    if inMonth<10:
        month = '0'+str(inMonth)
    else:
        month = str(inMonth)
    for i in range(32):
        if i<10:
            date = '0'+str(i)
        else:
            date=str(i)
                
        rootUrl= 'http://paper.people.com.cn/rmrb/html/2017-'+month+'/'+date+'/nbs.D110000renmrb_01.htm'
        root="D://MyRes//rmrb//"
        html=getHTMLText(rootUrl)
        url=getUrl(html)
#        fileDestination = 
        downloadUrl(url,root)   
    
    

def main():

    
#    fileDestination = root+'page//2017-04//02//'
#    root,files=getFiles(fileDestination)
#    #print(files)
   # PDFMergeFun(root,files,'test1.pdf')
#    PDFMergeFun(pdfFile,des)
#    
    #PDFMergeAll(root)
    downloadMonthPaper()
    print("Work done!")

main()