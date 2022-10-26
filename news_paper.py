from bs4 import BeautifulSoup
import requests
import webbrowser
from tqdm import tqdm
from datetime import date
import os
import time
import re

def remove_html_tags(text):
    """Remove html tags from a string"""
    text = str(text)
    text  = text.strip()
    clean = re.compile('<.*?>')
    text = " ".join(text.split())
    text = re.sub(clean, '', text).strip()
    return text

def download_pdf(url, file_name, headers):
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        with open(file_name, "wb") as f:
            print("Downloading..........................")
            f.write(response.content)
            print("Downloaded Succesfully...............")
    else:
        print(response.status_code)

def url_maker(url , header):
    global txt
    response=requests.get(url,headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    pap = soup.find_all("span", style="font-size: 16px;")[0]
    txt = remove_html_tags(str(pap)).split(":")[1]
    link = re.findall(r'href=[\'"]?([^\'" >]+)', str(pap))[0]
    response=requests.get(link,headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    paper = soup.find_all("iframe")[0]
    pdf_link = re.findall(r'src=[\'"]?([^\'" >]+)', str(paper))[0]
    return pdf_link



if __name__ == "__main__":

    headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9'}
    url = 'https://dailyepaper.in/hindu-analysis-notes-in-pdf-download-2022//'
    today = date.today()
    file_name = "F:\\CAT\\epaper\\" + str(today.strftime("%b-%d-%Y")) + ".pdf"
    try:
        pdf_link = url_maker(url , headers)
        download_pdf(pdf_link, file_name, headers)
        time.sleep(3)
        webbrowser.open_new(f'{file_name}')
        os.system('cls')
    except IndexError as e:
        print("Paper is not published Yet Please Try again later............" + "Reason is :" + txt)

