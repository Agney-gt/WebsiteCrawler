#!/usr/bin/env python
"""
Email scanner: prints all email addresses found on a domain.
Joe Kamibeppu | 10 Oct 2016
Dependencies:
    Beautiful Soup (pip install beautifulsoup4)
    Requests (pip install requests)
Usage:
    python find_email_addresses.py [domain name]
"""
import pandas as pd
# importing libraries
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
import os
from transformers import pipeline
import PyPDF2
from nltk.tokenize.treebank import TreebankWordDetokenizer
import fitz
from transformers import GPT2Tokenizer
import re
import sys
import argparse
from urllib.parse import urljoin, urlparse
import requests
from bs4 import BeautifulSoup, SoupStrainer
from seleniumwire import webdriver
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import InvalidArgumentException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd
from selenium.webdriver.firefox.options import Options
import time
summarizer = pipeline("summarization")
#option = uc.ChromeOptions()
driver = webdriver.Chrome(executable_path='c:/users/agney/desktop/chromedriver.exe')
driver.set_page_load_timeout(300)
#df=pd.read_csv("D:/Python/DB/FindEMails/Verified-USA-Jobs-1.csv")
df=pd.DataFrame()
c="contact"
ig="instagram"
fb="facebook"
yt="youtube"
li="linkedin"
tw="twitter"
x=0
lis=["https://www.exaloan.com/","https://www.ankr.com","https://www.apexsystems.com" ]
query=[]
def sumarrizers(text):
    duplicates = set()
    cleaned = []
    stopWords = set(stopwords.words("english"))
    words = word_tokenize(text)
    sentences = sent_tokenize(text)
    for s in sentences:
                #print(s)
        sent=s.replace('\n','')
                #print(sent)
                
                
        if sent not in duplicates:
            duplicates.add(sent.replace('\n',''))
            cleaned.append(sent.replace('\n',''))
            #count=0
            #for page in f:
           
                #count=count+1
    z=int(len(cleaned))
    print(z)        
    text= TreebankWordDetokenizer().detokenize(cleaned[:z])
    tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
    x = tokenizer.encode(text,truncation=True, max_length=1020)
    y=tokenizer.decode(x)
    z=summarizer(y, max_length=330, min_length=130, do_sample=False)
    summary="\n"+str(z[0])+"\n"
    return summary
for i in lis:
    string="https://www."+i
    query.append(string)

test=["https://www.turnberrysolutions.com"]
def find_emails(base_url, about):
    ''' finds email addresses by iteratively traversing through pages '''
    emails = set()
    to_visit = set()
    visited = set()
    
    to_visit.add(base_url)
    df.at[x,"DOMAIN"]=base_url

    while len(to_visit) and len(visited)<5 > 0:
        page = to_visit.pop()
        print(page)
    
        
        #response = requests.get(page, timeout=10)
        #time.sleep(5)
        driver.get(page)
        visited.add(page)
        time.sleep(3)
        #soup = BeautifulSoup(response.text, 'lxml')
        #soup = BeautifulSoup(driver.page_source, 'lxml')
        #soup=driver.execute_script("return document.documentElement.outerHTML")
        soups=driver.find_element_by_xpath("//*").get_attribute("outerHTML")
        
        soup1=BeautifulSoup(soups, 'lxml')
        text=soup1.get_text().strip()
        #print(int(len(text)))
        if (base_url == page):
            summary2=sumarrizers(text)
            print(summary2)
            df.at[x,"Summary"]=summary2.strip()
        if "about" in page:
            summary1=sumarrizers(text)
            about=about+summary1#print(summary1)
            df.at[x,"About Us"]=about.strip()
        #print("Debug-Email")
        emailz = re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", soup1.text)
        try:
            df.at[x,"Email-0"]=[emailz[0]]
            print(emailz[0])
        except (NameError, ValueError, KeyError,IndexError,TypeError) as e:
            print(e)
            #df.at[y,"Errors"]=e
            pass
        numberz = re.findall('[\d]{10}',soup1.text)
        number=re.findall('\(?\d[- \d()]*\d',soup1.text)
        #print(number)
        
        #print("Debug-Number")
        try:
            df.at[x,"Number-0"]=[numberz[0]]
            print(numberz[0])
        except (NameError, ValueError, KeyError,IndexError,TypeError) as e:
            print(e)
            #df.at[y,"Errors"]=e
            pass
        count=0
        for i in number:
            if(len(i)>9):
                count=count+1
                print(i)
                df.at[x,"number-"+str(count)]=i
                
        #hrefs = BeautifulSoup(response.text, 'lxml',
                              #parse_only=SoupStrainer('a'))
        #print("Debug-Links-0")
        hrefs = BeautifulSoup(soups, 'lxml', parse_only=SoupStrainer('a'))
        #print("Debug-Links")
        for email_href in hrefs.select('a[href^=mailto]'):
            emails.add(email_href.get('href').replace('mailto:', ''))
        tc=0
        for k in soup1.find_all('a', href=True):
            #print("here")
            #print(k['href'])
            if ig in k['href']:
                #print(k['href'])
                df.at[x,ig]=[k['href']]
            if fb in k['href']:
                df.at[x,fb]=[k['href']]
            if tw in k['href']:
                #print(k['href'])
                df.at[x,tw]=[k['href']]
            if yt in k['href']:
                df.at[x,yt]=[k['href']]
            if li in k['href']:
                df.at[x,li]=[k['href']]
            if "tel:" in k['href']:
                tc=tc+1
                #print(k['href'])
                df.at[x,"tel"+str(tc)]=[k['href']]
            try:
                if "contact" in k['href']:
                    #print(k['href'])
                    if k['href'] not in visited:
                        if "https://" in k['href']:
                            #print(k['href'])
                            to_visit.add(k['href'])
            except Exception as e:
                print(e)
                pass
            try:
                if "about" in k['href']:
                    #print(k['href'])
                    if "news" not in k['href']:
                        if k['href'] not in visited:
                            if "https://" in k['href']:
                                #print(k['href'])
                                to_visit.add(k['href'])
            except Exception as e:
                print(e)
                pass
            
            new_url = urljoin(base_url, k['href'])
            
            if urlparse(new_url).hostname == urlparse(base_url).hostname:
                if "contact" in new_url:
                    
                    if new_url not in visited:
                        #if "https://" in k['href']:
                        #print(new_url)
                        to_visit.add(new_url)
                if "about" in new_url:
                    if "news" not in new_url:
                    
                        if new_url not in visited:
                            #if "https://" in k['href']:
                            #print(new_url)
                            to_visit.add(new_url)
                        
                        
                            
                
        print("To Visit:",to_visit)
        print("Visited=",visited)#print(to_visit)
        if len(to_visit) > 500:
            print("More than 500 subpages have been found so far.") 
            print("Terminating the program.") 
            print_emails(emails)
            #sys.exit()
        
    print_emails(emails)
    #df.at[y,"Errors"]=e

def print_emails(emails):
    ''' prints all email addresses found '''
    print("Found these email addresses:")
    
    y=1
    e="Email-"
    for email in emails:
        n=(e+str(y))
        df.at[x,n]=email
        print(email)
        y=y+1
    df.to_csv("Competitors.csv", index=False)

for k in lis:
    try:
        about=''
        find_emails(k, about)
        x=x+1
        
    except Exception as e: #(selenium.common.exceptions.WebDriverException,requests.exceptions.Timeout, NameError, ValueError, KeyError,IndexError,TypeError, OSError, ConnectionError) as e:
            print(e)
            df.at[x,"Errors"]=e
            x=x+1
            print(x)
            
            continue
