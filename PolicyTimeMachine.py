#################import all the needed packages
import customtkinter
from tkcalendar import Calendar
from tkinter import *
import pandas as pd  #first try install latest version of Pandas → pip install pandas; if there are any issues related to pandas versions, try to install the old version: pandas 1.2.3 →  pip install pandas==1.2.3
import requests
from lxml import etree
import json
import datetime
import re
import time
import random
import os
import io
import darkdetect
from threading import Thread
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from tqdm import tqdm
from retrying import retry
import difflib
from nltk.tokenize import sent_tokenize
#######################################################################################################################

#set headers to skip the scraping limitation of targeted websites
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
    #'Connection': 'keep-alive'
}
headers_2 = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36',
                     'Accept-Language': 'en'}
user_agent = headers['User-Agent']

'''
[Part 1] 
Codes for scraping platforms' terms + privacy policies

From this part, we wrote different codes for scraping different platforms due to their various website structures. 
The codes for each platform will be defined as a function. For example, the whole codes of Douyin will be put into a function Douyin().
If we call this function Douyin(), we can directly obtain all the terms/privacy policies data.
Douyin only has terms+policis, some other platforms may have more pages to be scraped (e.g., teenager/driver policies)
Frist, each function will create a folder "Data_DayByDay" for saving data. Each platform's data will be saved in the subfolder (naming it as the plaform's name).
Second, each function will loop to get all the data from targeted pages.
Last, before saving into the subfolders, data should be put in a dataframe using pandas. The dataframe contains at least four columns: ['platform', 'date', 'content', 'url'].
(platform: the name of the platform; date: the date for scraping this time; content: the text of the policies; url: the link of the targeted pages)

For future users/RAs/project members:
If you find the WaybackScraper APP cannot scrape data for certain platforms, there may be two reasons:
1. network issue. You can try to rerun the app to exclude this possibility.
2. always-updating websites. Many platforms will update their pages for displaying policies documents. If the webpage structure change, we also need to revise the codes.
If 2. is the case, we don't need to rewrite all the codes, we just need to revise the function for that platform.  
'''

#the codes for scraping Douyin
def Douyin():
    name = "Douyin"
    path = 'Data_DayByDay/' + name + '/'
    if not os.path.exists(path):
        os.makedirs(path)
    # the urls that need to be scraped
    id = [("terms","6773906068725565448"), ("privacy","6773901168964798477")]
    for i in id:
        url = 'https://www.douyin.com/agreements/?id=' + i[1]
        res = requests.get(url, headers=headers)
        res_text = res.text
        selector = etree.HTML(res_text.encode('utf-8-sig'))
        infos = selector.xpath('//*[@class="draft-container"]//text()')
        content = '\n'.join(infos).replace(" +"," ").replace(" \n","\n").replace("\n，","，").replace("\n：","：").replace("\n。","。").replace("\n《","《").replace("\n》","》").replace("\n【\n","【").replace("\n】","】").replace("\n）","）").replace("\n、","、").replace("\n\n","\n").replace("  "," ").replace(")\n",")").replace("\n （","（").replace("\n；","；")
        print(content)
        date = datetime.date.today().strftime('%Y%m%d')  # get today's date
        df = pd.DataFrame(data=[[name, date, content, url]],
                          columns=['platform', 'date','content', 'url'])

        df.to_csv(path + name + "_" + i[0] + "_" + date + ".csv", index=False)


#the codes for scraping TikTok
def TikTok():
    name = "TikTok"  # name of the platform
    path = 'Data_DayByDay/' + name + '/'
    if not os.path.exists(path):
        os.makedirs(path)

    subpage = ["community-guidelines", "legal/terms-of-service", "legal/cookie-policy",
               "legal/privacy-policy-for-younger-users", "legal/privacy-policy-us",
               "legal/open-source", "legal/virtual-items", "legal/copyright-policy", "legal/law-enforcement"]

    urls = ['https://www.tiktok.com/{}?lang=en'.format(number) for number in subpage]
    for url, single_subpage in zip(urls, subpage):
        res = requests.get(url, headers=headers)
        selector = etree.HTML(res.text.encode('utf-8'))
        if single_subpage == "community-guidelines":
            c_list = ["https://www.tiktok.com/community-guidelines/en/overview",
                      "https://www.tiktok.com/community-guidelines/en/community-principles",
                      "https://www.tiktok.com/community-guidelines/en/youth-safety",
                      "https://www.tiktok.com/community-guidelines/en/safety-civility",
                      "https://www.tiktok.com/community-guidelines/en/mental-behavioral-health",
                      "https://www.tiktok.com/community-guidelines/en/sensitive-mature-themes",
                      "https://www.tiktok.com/community-guidelines/en/integrity-authenticity",
                      "https://www.tiktok.com/community-guidelines/en/regulated-commercial-activities",
                      "https://www.tiktok.com/community-guidelines/en/privacy-security",
                      "https://www.tiktok.com/community-guidelines/en/fyf-standards",
                      "https://www.tiktok.com/community-guidelines/en/accounts-features",
                      "https://www.tiktok.com/community-guidelines/en/enforcement"]

            content3 = ""
            for c in c_list:
                res_c = requests.get(c, headers=headers)
                selector = etree.HTML(res_c.text.encode('utf-8'))
                content2 = selector.xpath('//div[@class="css-1dtybk6 e4uzr091"]//text()')

                formatted_infos = ""
                for element in content2:
                    if element.getparent().tag not in ["a", "strong"]:
                        formatted_infos += "\n"
                    else:
                        formatted_infos += " "
                    formatted_infos += element
                formatted = formatted_infos[1:]

                content3 = content3 + formatted + "\n\n"
                content3 = content3.replace(
                    ".css-1nyymor{-webkit-text-decoration:underline;text-decoration:underline;}", "")

        else:
            try:
                content = selector.xpath('//section[@data-testid="policy-card-pre-content"]')[0]
                content2 = content.xpath(".//text()")
                content_post = selector.xpath('//section[@data-testid="policy-card-post-content"]')[0]
                content_post2 = content_post.xpath(".//text()")
                content2 = content2 + content_post2
                content3 = ' '.join(content2).strip()
                content3 = content3.encode('cp1252','backslashreplace').decode('utf-8','backslashreplace').replace("\\xe2\\x80\\x9c", '"').replace("\\xe2\\x80\\x9d", '"').replace("\\xe2\\x80\\x99", "'").replace("\\xe2\\x80\\x93","-").replace("\n", " ")
                print(content3)
            except IndexError as e:
                content3 = "none"
        up_time = [x for x in content2 if ('dated') in x]
        try:
            up_time = re.split(': |; |, |\*|\n', up_time[0])[1]
        except Exception as e:
            up_time = "none"
        p_time = "none"
        date = datetime.date.today().strftime('%Y%m%d')
        url = res.url
        df = pd.DataFrame(data=[[date, p_time, up_time, content3, url]],
                          columns=['date', 'published_date', 'last_updated', 'content', 'url'])
        df.to_csv(path + "TikTok" + "_" + single_subpage.replace("legal/", "") + "_" + date + ".csv", index=False)
        time.sleep(random.uniform(0.2, 0.5))


#the codes for scraping FindTaxi
def FindTaxi():
    name = "FindTaxi"
    path = 'Data_DayByDay/' + name + '/'
    if not os.path.exists(path):
        os.makedirs(path)

    url = 'https://findtaxi.io/terms_of_service.html'
    res = requests.get(url, headers=headers)
    res.encoding = "utf-8"
    selector = etree.HTML(res.text)
    infos = selector.xpath('//section//text()')
    print(infos)
    content = '\n'.join(infos).replace("\t","").replace("\n\n","").strip()
    clean_format = (("\t", "\n"), ("\n+", "\n"), (r"1. \n", "1. "), (r"2. \n", "2. "), (r"3. \n", "3. "))
    for element in clean_format:
        content = re.sub(element[0], element[1], content)
    print(content)
    date = datetime.date.today().strftime('%Y%m%d')
    df = pd.DataFrame(data=[[name, date, content, url]], columns=['platform', 'date', 'content', 'url'])
    df.to_csv(path + name + "_" + "使用者授權合約暨隱私權條款" + "_" + date + ".csv", index=False)


#the codes for scraping LineTaxi
def LineTaxi():
    name = "LINE TAXI"
    path = 'Data_DayByDay/' + name + '/'
    if not os.path.exists(path):
        os.makedirs(path)

    id = ["使用者條款", "privacy-policy", "driver-privacy-policy", "line-taxi-privacy-policy"]
    for i in id:
        url = 'https://linetaxi.com.tw/' + i

        res = requests.get(url, headers=headers)
        selector = etree.HTML(res.text)
        infos = selector.xpath('//article[starts-with(@id,"post-")]//text()')
        content = '\n'.join(infos).strip()
        clean_format = (
            (r"\t", "\n"), (' +', ' '), ("\n+", "\n"), ("\n +", "\n"), (r"\n+", "\n"), (r"、\n", "、"), (r"「\n", "「"),
            (r"\n」", "」"), (u'\xa0', ' '),('\n。','。'),('\n，','，'))
        for element in clean_format:
            content = re.sub(element[0], element[1], content)
        date = datetime.date.today().strftime('%Y%m%d')
        print(content)
        df = pd.DataFrame(data=[[name, date, content, url]],
                          columns=['platform', 'date', 'content', 'url'])
        df.to_csv(path + name + "_" + i + "_" + date + ".csv", index=False)
        time.sleep(random.uniform(0.1, 0.2))


#the codes for scraping Meituan
def Meituan():
    name = "Meituan"
    path = 'Data_DayByDay/' + name + '/'
    if not os.path.exists(path):
        os.makedirs(path)
    id = ["4", "759", "2", "511", "755", "834"]
    for i in id:
        url = 'https://rules-center.meituan.com/cap-rules-center/api/rules/detail?id=' + i
        res = requests.get(url, headers=headers)
        json_data = json.loads(json.loads(res.text)['data'])
        content = json_data['title'] + ' ' + json_data['detail']
        content = etree.HTML(text=content)
        content = content.xpath('string(.)')
        print(content)
        date = datetime.date.today().strftime('%Y%m%d')
        df = pd.DataFrame(data=[[name, date, content, url]],
                          columns=['platform', 'date', 'content', 'url'])
        df.to_csv(path + name + "_" + json_data['title'] + "_" + date + ".csv", index=False)


#the codes for scraping Foodpanda
def Foodpanda():
    name = "foodpanda"
    path = 'Data_DayByDay/' + name + '/'
    if not os.path.exists(path):
        os.makedirs(path)
    urls = ["contents/terms-and-conditions.htm", "contents/privacy.htm", "zh/contents/terms-and-conditions.htm",
            "zh/contents/privacy.htm"]
    urls2 = ['terms_en', 'privacy_en', 'terms_zh', 'privacy_zh']
    for url, url2 in zip(urls, urls2):
        url = 'https://www.foodpanda.hk/' + url
        print(url)
        if url2.__contains__("_zh"):
            headers['Cookie'] = "hl=zh; Path=/; Secure"
            res = requests.get(url, headers=headers)
            res.encoding = "utf-8"
            selector = etree.HTML(res.text)
            infos = selector.xpath('//div[starts-with(@class, "box-flex content-wrapper")]//text()')
            if url2.__contains__("privacy"):
                try:
                    index = infos.index("\r\n私隱政策\r\n")
                except:
                    index = infos.index("\r\nPrivacy Policy\r\n")
                infos = infos[index:]
            else:
                infos = infos
        else:
            res = requests.get(url, headers=headers)
            res.encoding = "utf-8"
            selector = etree.HTML(res.text)
            infos = selector.xpath('//div[starts-with(@class, "box-flex content-wrapper")]//text()')
            if url2.__contains__("privacy"):
                try:
                    index = infos.index("\r\nPrivacy Policy\r\n")
                except:
                    index = infos.index("\r\n私隱政策\r\n")
                infos = infos[index:]
            else:
                infos = infos
        content = ''.join(infos).strip()
        content = content.replace(u'\xa0', ' ')
        content = re.sub(r"\r", "\n", content)
        content = re.sub(r"\n+", "\n", content)
        date = datetime.date.today().strftime('%Y%m%d')
        print(content)
        df = pd.DataFrame(data=[[name, date, content, url]],
                          columns=['platform', 'date', 'content', 'url'])
        df.to_csv(path + name + "_" + url2 + "_" + date + ".csv", index=False)


#the codes for scraping Lalamove
def Lalamove():
    name = "Lalamove"
    path = 'Data_DayByDay/' + name + '/'
    if not os.path.exists(path):
        os.makedirs(path)

    urls = ["en-hk/terms-and-conditions", "en-hk/privacy-policy", "zh-hk/terms-and-conditions", "zh-hk/privacy-policy"]
    urls2 = ['terms_en', 'privacy_en', 'terms_zh', 'privacy_zh']
    for url, url2 in zip(urls, urls2):
        url = 'https://www.lalamove.com/' + url
        res = requests.get(url, headers=headers)
        time.sleep(1)
        selector = etree.HTML(res.text)
        if url2.__contains__("privacy_"):
            infos = selector.xpath('//div[@class="detail-page-content"]//text()')
            content = ''.join(infos).strip()
            content = content.replace(u'\xa0', ' ')
            content = content.replace(u'\u200E', ' ').strip()
            content = re.sub(r" +", " ", content)
            content = re.sub(r"\n +", "\n", content)
            content = re.sub(r"\n+", "\n", content)
            date = datetime.date.today().strftime('%Y%m%d')
            print(content)
            df = pd.DataFrame(data=[[name, date, content, url]],
                              columns=['platform', 'date', 'content', 'url'])
            df.to_csv(path + name + "_" + url2 + "_" + date + ".csv", index=False)

        else:
            terms = selector.xpath(
                '//div[@data-subsection="Terms and Conditions"]//text()|//div[@data-subsection="用戶條款及守則"]//text()')
            terms2 = ''.join(terms).strip()
            terms2 = terms2.replace(u'\xa0', ' ')
            terms2 = re.sub(r" +", " ", terms2)
            terms2 = re.sub(r"\n +", "\n", terms2)
            terms2 = re.sub(r"\n+", "\n", terms2)
            date = datetime.date.today().strftime('%Y%m%d')
            df = pd.DataFrame(data=[[name, date, terms2, url]],
                              columns=['platform', 'date', 'content', 'url'])
            df.to_csv(path + name + "_" + url2 + "_" + date + ".csv", index=False)

            d_terms = selector.xpath(
                '//div[@data-subsection="Lalamove Delivery Partner Terms of Use"]//text()|//div[@data-subsection="使用條款"]//text()')
            d_terms2 = ''.join(d_terms).strip()
            d_terms2 = d_terms2.replace(u'\xa0', ' ')
            d_terms2 = re.sub(r" +", " ", d_terms2)
            d_terms2 = re.sub(r"\n +", "\n", d_terms2)
            d_terms2 = re.sub(r"\n+", "\n", d_terms2)
            date = datetime.date.today().strftime('%Y%m%d')
            print(d_terms2)
            df = pd.DataFrame(data=[[name, date, d_terms2, url]],
                              columns=['platform', 'date', 'content', 'url'])
            df.to_csv(path + name + "_" + url2 + "_Delivery_" + date + ".csv", index=False)

            if url2.__contains__("_en"):
                comm = selector.xpath('//div[@data-subsection="Community Guidelines"]//text()') \
                       + ["Respect\n"] + selector.xpath('//div[@data-subsection="Respect"]/div[2]//text()') \
                       + ["Safety\n"] + selector.xpath('//div[@data-subsection="Safety"]/div[2]//text()') \
                       + ["Follow the law\n"] + selector.xpath(
                    '//div[@data-subsection="Follow the law"]/div[2]//text()') \
                       + ["Feedback\n"] + selector.xpath('//div[@data-subsection="Feedback"]/div[2]//text()')
            else:
                comm = selector.xpath('//div[@data-subsection="社群指引 "]//text()') \
                       + ["尊重\n"] + selector.xpath('//div[@data-subsection="尊重"]/div[2]//text()') \
                       + ["安全\n"] + selector.xpath('//div[@data-subsection="安全"]/div[2]//text()') \
                       + ["守法\n"] + selector.xpath('//div[@data-subsection="守法"]/div[2]//text()') \
                       + ["回饋\n"] + selector.xpath('//div[@data-subsection="回饋"]/div[2]//text()')
            comm2 = ''.join(comm).strip()
            comm2 = comm2.replace(u'\xa0', ' ')
            comm2 = re.sub(r" +", " ", comm2)
            comm2 = re.sub(r"\n +", "\n", comm2)
            comm2 = re.sub(r"\n+", "\n", comm2)
            comm2 = comm2.replace("1\n", "1").replace("2\n", "2").replace("3\n", "3").replace("4\n", "4").replace(
                "5\n", "5").replace("6\n", "6").replace("7\n", "7").replace("8\n", "8").replace("9\n", "9")
            print(comm2)
            date = datetime.date.today().strftime('%Y%m%d')
            df = pd.DataFrame(data=[[name, date, comm2, url]],
                              columns=['platform', 'date', 'content', 'url'])
            df.to_csv(path + name + "_" + url2 + "_Community_" + date + ".csv", index=False)


#the codes for scraping GoGoVan
def GoGoVan():
    name = "GoGOVan"
    path = 'Data_DayByDay/' + name + '/'
    if not os.path.exists(path):
        os.makedirs(path)

    id = ["terms", "privacy", "hk/terms", "hk/privacy"]
    for i in id:
        url = 'https://www.gogox.com/' + i + "/"
        res = requests.get(url, headers=headers)
        # res.encoding = "utf-8"
        selector = etree.HTML(res.text)
        infos = selector.xpath('//div[@class="elementor-text-editor elementor-clearfix"]//text()')
        if 'hk/' in url:
            content = ''.join(infos).strip()
        else:
            content = ' '.join(infos).strip()
        content = content.replace(u'\xa0', '')
        content = re.sub(r"\n+", "\n", content)
        print(content)
        date = datetime.date.today().strftime('%Y%m%d')
        df = pd.DataFrame(data=[[name, date, content, url]],
                          columns=['platform', 'date', 'content', 'url'])
        df.to_csv(path + name + "_" + i.replace("/", "_") + "_" + date + ".csv", index=False)


#the codes for scraping Signal
def Signal():
    name = "Signal"
    path = 'Data_DayByDay/' + name + '/'
    if not os.path.exists(path):
        os.makedirs(path)

    url = 'https://signal.org/legal/'
    res = requests.get(url, headers=headers)
    selector = etree.HTML(res.text)
    infos = selector.xpath('//div[@class="columns is-centered"]//text()')
    content = ' '.join(infos).strip()
    date = datetime.date.today().strftime('%Y%m%d')
    print(content)
    df = pd.DataFrame(data=[[name, date, content, url]], columns=['platform', 'date', 'content', 'url'])
    df.to_csv(path + name + "_" + "Terms & Privacy Policy" + "_" + date + ".csv", index=False)


#the codes for scraping Telegram
def Telegram():
    name = "Telegram"
    path = 'Data_DayByDay/' + name + '/'
    if not os.path.exists(path):
        os.makedirs(path)
    id = ["tos", "privacy"]
    for i in id:
        url = 'https://telegram.org/' + i
        res = requests.get(url, headers=headers)
        selector = etree.HTML(res.text)
        infos = selector.xpath('//div[@id="dev_page_content_wrap"]//text()')
        content = ''.join(infos).strip()
        content = re.sub(r"\n +", "\n", content).strip()
        content = re.sub(r"\n+", "\n", content).strip()
        #content = re.sub(r"\n", "\n", content).strip()
        #content = re.sub('\n“', '“', content).strip()
        date = datetime.date.today().strftime('%Y%m%d')
        print(content)
        df = pd.DataFrame(data=[[name, date, content, url]],
                          columns=['platform', 'date', 'content', 'url'])
        df.to_csv(path + name + "_" + i + "_" + date + ".csv", index=False)


#the codes for scraping LINE
def LINE():
    name = "LINE"
    path = 'Data_DayByDay/' + name + '/'
    if not os.path.exists(path):
        os.makedirs(path)
    urls = ["https://terms.line.me/line_terms?lang=en", "https://terms.line.me/line_terms?lang=zh-Hant",
            "https://line.me/en/terms/policy/", "https://line.me/zh-hant/terms/policy/"]
    urls2 = ['terms_en', 'terms_zh', 'privacy_en', 'privacy_zh']
    for url, url2 in zip(urls, urls2):
        res = requests.get(url, headers=headers)
        selector = etree.HTML(res.text)
        infos = selector.xpath('//section[@class="details"]//text()|//div[@class="MdTerms01"]//text()')
        content = ''.join(infos).strip()
        content = content.replace(u'\xa0', ' ')
        clean_format = ((r"\t", "\n"), (' +', ' '), (r"\n+", "\n"), (r"\n +", "\n"), (r"\n+", "\n"))
        for element in clean_format:
            content = re.sub(element[0], element[1], content)
        date = datetime.date.today().strftime('%Y%m%d')
        print(content)
        df = pd.DataFrame(data=[[name, date, content, url]],
                          columns=['platform', 'date', 'content', 'url'])
        df.to_csv(path + name + "_" + url2 + "_" + date + ".csv", index=False)
        time.sleep(0.1)


#the codes for scraping WhatsApp
def WhatsApp():
    name = "WhatsApp"
    path = 'Data_DayByDay/' + name + '/'
    if not os.path.exists(path):
        os.makedirs(path)
    id = ["terms-of-service?lang=en", "terms-of-service/?lang=zh_hk",
          "privacy-policy?lang=en", "privacy-policy/?lang=zh_hk"]
    urls2 = ['terms_en', 'terms_zh', 'privacy_en', 'privacy_zh']
    for i, url2 in zip(id, urls2):
        url = 'https://www.whatsapp.com/legal/' + i
        res = requests.get(url, headers=headers_2)
        selector = etree.HTML(res.text)
        infos = selector.xpath('//div[@class="_9t2g _9t2c _a1fe"]//text()')
        content = ' '.join(infos).strip()
        date = datetime.date.today().strftime('%Y%m%d')
        print(content)
        df = pd.DataFrame(data=[[name, date, content, url]],
                          columns=['platform', 'date', 'content', 'url'])
        df.to_csv(path + name + "_" + url2 + "_" + date + ".csv", index=False)


#the codes for scraping Xiaohongshu
def Xiaohongshu():
    name = "Xiaohongshu"
    path = 'Data_DayByDay/' + name + '/'
    if not os.path.exists(path):
        os.makedirs(path)
    ids = ["ZXXY20220331001", "ZXXY20220509001", "ZXXY20221213003", "ZXXY20230215001"]
    urls2 = ['terms_zh', 'privacy_zh', 'community_zh', 'complaint_zh']
    for id, url2 in zip(ids, urls2):
        url = 'https://oacontract.xiaohongshu.com/oacontract/v1/contract/findContractContent?id=-1&contractNo=' + id
        res = requests.post(url)
        res_string = json.loads(res.text)['data']
        selector = etree.HTML(res_string)
        infos = selector.xpath('//text()')
        content = ''.join(infos).strip()
        content = content.replace(u'\xa0', ' ').strip()
        content = re.sub(r"\n \n", "\n", content).strip()
        content = re.sub(r"\n+", "\n", content).strip()
        date = datetime.date.today().strftime('%Y%m%d')
        print(content)
        df = pd.DataFrame(data=[[name, date, content, url]], columns=['platform', 'date', 'content', 'url'])
        df.to_csv(path + name + "_" + url2 + "_" + date + ".csv", index=False)

    ids = ["en/privacy_protection", "en/intellectual_property"]
    urls2 = ['privacy_en', 'intellectual_property_en']
    for id, url2 in zip(ids, urls2):
        url = 'https://www.xiaohongshu.com/' + id
        res = requests.get(url, headers=headers)
        selector = etree.HTML(res.text)
        infos = selector.xpath('//div[@class="main-pattern"]//text()')
        content = '\n'.join(infos).strip()
        #content = content.replace(u'\xa0', ' ').strip()
        content = re.sub(r"\nshuduizhang@xiaohongshu.com\n", "", content).strip()
        content = re.sub(r"\nXiaohongshu User Privacy Policy\n", "", content).strip()
        #content = re.sub(r"\n+", "\n", content).strip()
        date = datetime.date.today().strftime('%Y%m%d')
        print(content)
        df = pd.DataFrame(data=[[name, date, content, url]], columns=['platform', 'date', 'content', 'url'])
        df.to_csv(path + name + "_" + url2 + "_" + date + ".csv", index=False)


#the codes for scraping Vine
def Vine():
    name = "Vine"
    path = 'Data_DayByDay/' + name + '/'
    if not os.path.exists(path):
        os.makedirs(path)
    id = ["terms", "privacy"]
    for i in id:
        url = 'https://vine.co/' + i
        res = requests.get(url, headers=headers)
        selector = etree.HTML(res.text)
        infos = selector.xpath('//div[@class="container legal"]//text()')
        content = ''.join(infos).strip()
        content = re.sub(r"\n +", "\n", content).strip()
        content = re.sub(r'\n“', '“', content).strip()
        content = re.sub(r'\n"', '"', content).strip()
        content = re.sub(r"\n+", "\n", content).strip()
        content = re.sub(r"\nhere.", " here.", content).strip()
        content = re.sub(r"\nArchive.", " Archive.", content).strip()
        date = datetime.date.today().strftime('%Y%m%d')
        print(content)
        df = pd.DataFrame(data=[[name, date, content, url]],
                          columns=['platform', 'date', 'content', 'url'])
        df.to_csv(path + name + "_" + i + "_" + date + ".csv", index=False)


#the codes for scraping Tumblr
def Tumblr():
    name = "Tumblr"
    path = 'Data_DayByDay/' + name + '/'
    if not os.path.exists(path):
        os.makedirs(path)
    ids = ["policy/en/terms-of-service", "privacy/en", "policy/en/community"]
    urls2 = ['terms', 'privacy', 'community']
    for id, url2 in zip(ids, urls2):
        url = 'https://www.tumblr.com/' + id
        res = requests.get(url, headers=headers)
        selector = etree.HTML(res.text)
        infos = selector.xpath('//*[@id="left_column"]//text()')
        if url2 == "terms" or url2 == "privacy":
            infos.insert(1, "\n")
            infos.insert(3, "\n")
        content = ''.join(infos).strip()
        content = re.sub(r" +", " ", content).strip()
        content = re.sub(r"\n +", "\n", content).strip()
        print(content)
        date = datetime.date.today().strftime('%Y%m%d')
        df = pd.DataFrame(data=[[name, date, content, url]], columns=['platform', 'date', 'content', 'url'])
        df.to_csv(path + name + "_" + url2 + "_" + date + ".csv", index=False)


#the codes for scraping Pinterest
def Pinterest():
    name = "Pinterest"
    path = 'Data_DayByDay/' + name + '/'
    if not os.path.exists(path):
        os.makedirs(path)
    ids = ["en/terms-of-service", "zh-hant/terms-of-service", "en/privacy-policy", "zh-hant/privacy-policy"]
    urls2 = ['terms_en', 'terms_zh', 'privacy_en', 'privacy_zh']
    for id, url2 in zip(ids, urls2):
        url = 'https://policy.pinterest.com/' + id
        res = requests.get(url, headers=headers)
        selector = etree.HTML(res.text)
        infos = selector.xpath('//article//text()')
        content = ''.join(infos).replace("\n	","\n").replace("\t","\n").replace("\n\n","\n").replace("\\n\\n","\n").strip()
        content = content.replace(u'\xa0', ' ').strip()
        content = re.sub(r" +", " ", content).strip()
        content = re.sub("\n +", "\n", content).strip()
        content = re.sub("\n+", "\n", content).strip()
        print(content)
        date = datetime.date.today().strftime('%Y%m%d')
        df = pd.DataFrame(data=[[name, date, content, url]], columns=['platform', 'date', 'content', 'url'])
        df.to_csv(path + name + "_" + url2 + "_" + date + ".csv", index=False)


#the codes for scraping WeChat
def WeChat():
    name = "WeChat"
    path = 'Data_DayByDay/' + name + '/'
    if not os.path.exists(path):
        os.makedirs(path)
    ids = ["en/service_terms.html", "en/privacy_policy.html", "en/acceptable_use_policy.html",
           "zh_CN/service_terms.html", "zh_CN/privacy_policy.html", "zh_CN/acceptable_use_policy.html"]

    urls2 = ['terms_en', 'privacy_en', 'acceptable_use_policy_en',
             'terms_zh', 'privacy_zh', 'acceptable_use_policy_zh']

    for id, url2 in zip(ids, urls2):
        url = 'https://www.wechat.com/' + id
        res = requests.get(url, headers=headers)
        selector = etree.HTML(res.text)
        infos = selector.xpath('//div[@id="agreement"]//text()|//div[@id="agreement6"]//text()')
        formatted_infos = ""
        for element in infos:
            if element.getparent().tag in ["p", "h1", "h2", "h3", "h4", "li"]:
                formatted_infos += "\n"
            formatted_infos += element
        content = formatted_infos[1:]
        content = re.sub("Last modified", "\nLast modified", content).strip()
        content = re.sub("Last Updated", "\nLast Updated", content).strip()
        content = re.sub("Last updated", "\nLast updated", content).strip()
        content = re.sub("最后修订日期", "\n最后修订日期", content).strip()
        content = re.sub("最后更新时间", "\n最后更新时间", content).strip()
        print(content)
        date = datetime.date.today().strftime('%Y%m%d')
        df = pd.DataFrame(data=[[name, date, content, url]], columns=['platform', 'date', 'content', 'url'])
        df.to_csv(path + name + "_" + url2 + "_" + date + ".csv", index=False)


#the codes for scraping Weixin
def Weixin():
    name = "Weixin"
    path = 'Data_DayByDay/' + name + '/'
    if not os.path.exists(path):
        os.makedirs(path)
    ids = ["lang=en_US&t=weixin_agreement&s=default&cc=CN&head=true",
           "lang=en_US&t=weixin_agreement&s=privacy&cc=CN&head=true",
           "&t=page/agreement/personal_account&lang=en_US&head=true",
           "lang=zh_CN&t=weixin_agreement&s=default",
           "lang=zh_CN&t=weixin_agreement&s=privacy&head=true",
           "&t=page/agreement/personal_account&lang=zh_CN"]

    urls2 = ['terms_en', 'privacy_en', 'Account Usage_en',
             'terms_zh', 'privacy_zh', 'Account Usage_zh']

    for id, url2 in zip(ids, urls2):
        url = 'https://weixin.qq.com/cgi-bin/readtemplate?' + id
        res = requests.get(url, headers=headers)
        selector = etree.HTML(res.text)
        infos = selector.xpath('//div[@id="js_content"]//text()')
        formatted_infos = ""
        for element in infos:
            if element.getparent().tag not in ["strong", "a"]:
                formatted_infos += "\n"
            formatted_infos += element
        content = formatted_infos[1:]
        content = re.sub(r" +", " ", content).strip()
        content = re.sub(r"\n +", "\n", content).strip()
        content = re.sub(r" \n+", "\n", content).strip()
        content = re.sub(r"\n+", "\n", content).strip()
        print(content)
        date = datetime.date.today().strftime('%Y%m%d')
        df = pd.DataFrame(data=[[name, date, content, url]], columns=['platform', 'date', 'content', 'url'])
        df.to_csv(path + name + "_" + url2 + "_" + date + ".csv", index=False)


#the codes for scraping Snapchat
@retry
def Snapchat():
    name = "Snapchat"
    path = 'Data_DayByDay/' + name + '/'
    if not os.path.exists(path):
        os.makedirs(path)
    ids = ["https://snap.com/en-US/terms", "https://snap.com/zh-Hant/terms",
           "https://values.snap.com/privacy/privacy-policy?lang=en-US",
           "https://values.snap.com/zh-Hant/privacy/privacy-policy"]
    urls2 = ['terms_en', 'terms_zh', 'privacy_en', 'privacy_zh']
    for id, url2 in zip(ids, urls2):
        url = id
        res = requests.get(url, headers=headers)
        selector = etree.HTML(res.text)
        infos = selector.xpath('//div[@dir="ltr"]//text()')
        formatted_infos = ""
        for element in infos:
            if element.getparent().tag not in ["a", "span"]:
                formatted_infos += "\n"
            formatted_infos += element
        content = formatted_infos[1:]
        content = content.replace(u'\xa0', ' ').strip()
        content = re.sub("Privacy PolicyEffective", "Privacy Policy\nEffective", content).strip()
        content = re.sub("Snap Inc. is a camera company", "\nSnap Inc. is a camera company.", content).strip()
        content = re.sub("隱私政策生效日期", "隱私政策\n生效日期", content).strip()
        content = re.sub("Snap Inc. 是一間相機公司。", "\nSnap Inc. 是一間相機公司。", content).strip()
        content = re.sub("\n參引納入本條款\n的\n倫敦國際仲裁院", "參引納入本條款的倫敦國際仲裁院", content).strip()
        content = re.sub("\nLCIA Arbitration Rules\n", "LCIA Arbitration Rules", content).strip()
        content = re.sub("4. \n", "4. ", content).strip()
        content = re.sub("6. \n", "6. ", content).strip()
        date = datetime.date.today().strftime('%Y%m%d')
        print(content)
        df = pd.DataFrame(data=[[name, date, content, url]], columns=['platform', 'date', 'content', 'url'])
        df.to_csv(path + name + "_" + url2 + "_" + date + ".csv", index=False)


#the codes for scraping Tencent
def Tencent():
    name = "Tencent"
    path = 'Data_DayByDay/' + name + '/'
    if not os.path.exists(path):
        os.makedirs(path)
    ids = ["en-us/service-agreement.html", "en-us/privacy-policy.html",
           "zh-cn/service-agreement.html", "zh-cn/privacy-policy.html"]
    urls2 = ['terms_en', 'privacy_en', 'terms_zh', 'privacy_zh']
    for id, url2 in zip(ids, urls2):
        url = 'https://www.tencent.com/' + id
        res = requests.get(url, headers=headers)
        selector = etree.HTML(res.text)
        infos = selector.xpath('//div[@class="box"]//text()|//div[@class="box zh-cn"]//text()')
        content = ''.join(infos).strip()
        content = content.replace(u'\xa0', ' ').strip()
        content = re.sub(r" +", " ", content).strip()
        content = re.sub(r"\n +", "\n", content).strip()
        content = re.sub(r"\n+", "\n", content).strip()
        print(content)
        date = datetime.date.today().strftime('%Y%m%d')
        df = pd.DataFrame(data=[[name, date, content, url]], columns=['platform', 'date', 'content', 'url'])
        df.to_csv(path + name + "_" + url2 + "_" + date + ".csv", index=False)


#the codes for scraping Twitter
def Twitter():
    name = "Twitter"
    path = 'Data_DayByDay/' + name + '/'
    if not os.path.exists(path):
        os.makedirs(path)
    ids = ["en/tos", "en/privacy"]
    urls2 = ['terms_en', 'privacy_en']
    for id, url2 in zip(ids, urls2):
        url = 'https://twitter.com/' + id
        res = requests.get(url, headers=headers)
        res.encoding = "utf-8"
        selector = etree.HTML(res.text)
        infos = selector.xpath('//div[@class="root responsivegrid"]//text()')
        content = ''.join(infos).strip()
        content = content.replace(u'\xa0', ' ').strip()
        content = re.sub(r"\n +", "\n", content).strip()
        content = re.sub(r"\n+", "\n", content).strip()
        date = datetime.date.today().strftime('%Y%m%d')
        print(content)
        df = pd.DataFrame(data=[[name, date, content, url]], columns=['platform', 'date', 'content', 'url'])
        df.to_csv(path + name + "_" + url2 + "_" + date + ".csv", index=False)


#the codes for scraping Uber
def Uber():
    name = "Uber"
    path = 'Data_DayByDay/' + name + '/'
    if not os.path.exists(path):
        os.makedirs(path)
    ids = ["general-terms-of-use&country=hong-kong&lang=zh-hk", "general-terms-of-use&country=hong-kong&lang=en",
           "privacy-notice&country=hong-kong&lang=zh-hk", "privacy-notice&country=hong-kong&lang=en",
           "general-terms-of-use&country=united-states&lang=en", "privacy-notice&country=united-states&lang=en", "privacy-notice&country=united-states&lang=zh"]
    urls2 = ['terms_HK_zh', 'terms_HK_en', 'privacy_HK_zh', 'privacy_HK_en',
             'terms_USA_en', 'privacy_USA_en', 'privacy_USA_zh']
    for id, url2 in zip(ids, urls2):
        url = 'https://www.uber.com/legal/en/document/?name=' + id
        headers_2['Accept']='text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
        res = requests.get(url, headers=headers_2)
        selector = etree.HTML(res.text)
        infos = selector.xpath('//*[@id="legal-info"]/div/div[2]/div/div/div/div/div/div/div[1]/div/div//text()')
        content = '* '.join(infos).strip()
        print(content)
        date = datetime.date.today().strftime('%Y%m%d')
        df = pd.DataFrame(data=[[name, date, content, url]], columns=['platform', 'date', 'content', 'url'])
        df.to_csv(path + name + "_" + url2 + "_" + date + ".csv", index=False)


#the codes for scraping OpenAI
@retry
def OpenAI():
    name = "OpenAI (ChatGPT)"
    path = 'Data_DayByDay/' + name + '/'
    if not os.path.exists(path):
        os.makedirs(path)
    id = ["terms-of-use", "privacy-policy"]
    for i in id:
        url = 'https://openai.com/policies/' + i

        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument(f'user-agent={user_agent}')
        options.add_argument('--ignore-certificate-errors')
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
        driver.get(url)
        res = driver.page_source
        selector = etree.HTML(res)

        infos = selector.xpath('//div[@id="content"]//text()')

        content = '\n'.join(infos).strip()
        content = content.replace(u'\xa0', ' ').strip()
        content = content.replace(', \n', ', ').strip()
        content = content.replace('\n, ', ', ').strip()
        content = content.replace('\n. ', '. ').strip()
        content = content.replace('\n.', '.').strip()
        content = content.replace('\n: ', ': ').strip()
        for letter in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o',
                       'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']:
            content = content.replace(f'({letter}) \n', f'({letter}) ').strip()
        content = content.replace('(e). \n', '(e) ').strip()

        content = content.replace('\nsupport@openai.com\n', 'support@openai.com').strip()
        content = content.replace('\nsupport@openai.com.', 'support@openai.com.').strip()
        content = content.replace('\nar@openai.com\n', 'ar@openai.com').strip()
        content = content.replace('\nlegal@openai.com\n', 'legal@openai.com').strip()
        content = content.replace('\nAll About Cookies.', 'All About Cookies.').strip()
        content = content.replace('\nService Terms', 'Service Terms').strip()
        content = content.replace('\nPrivacy Policy\n', 'Privacy Policy').strip()
        print(content)
        date = datetime.date.today().strftime('%Y%m%d')
        df = pd.DataFrame(data=[[name, date, content, url]],
                          columns=['platform', 'date', 'content', 'url'])
        df.to_csv(path + name + "_" + i.split("-")[0] + "_" + date + ".csv", index=False)



#the codes for scraping CharacterAI
def CharacterAI():
    name = "Character.AI"
    path = 'Data_DayByDay/' + name + '/'
    if not os.path.exists(path):
        os.makedirs(path)
    id = ["tos", "privacy", "community"]
    res = requests.get('https://beta.character.ai/static/js/main.4f33731d.js', headers=headers_2)
    res_text = res.text
    text_matches = re.findall(r'",\s*\{children:\[?"([^"]*)"\}?', res_text)
    infos_pp = text_matches[text_matches.index("Privacy Policy") + 1:text_matches.index("Terms of Service") - 1]
    infos_terms = text_matches[text_matches.index("Terms of Service") - 1:]
    content_pp = '\n'.join(infos_pp).replace("\\u2019", "'").replace("\\u201c", '"').replace("\\u201d", '"').strip()
    content_terms = '\n'.join(infos_terms).replace("\\u2019", "'").replace("\\u201c", '"').replace("\\u201d", '"').strip()
    text_com = re.findall(r'Guidelines":\{"community-guidelines":"Community Guidelines",(.*?)"reporting-quality-problems-content":"When reporting a Character problem', res_text)
    matches = re.findall(r'"[^"]+":"([^"]+)"', text_com[0])
    extracted_content = [match.replace("<br />", "").replace("</br>", "").replace("<", "").replace(">", "").replace("\\","").replace("/","") for match in matches]
    infos_comm = ["Community Guidelines"]
    for value in extracted_content:
        infos_comm.append(value)
    content_comm = '\n'.join(infos_comm)
    print(content_pp)
    print(content_terms)
    print(content_comm)
    date = datetime.date.today().strftime('%Y%m%d')
    for i in id:
        if "tos" in i:
            content = content_terms
        elif "privacy" in i:
            content = content_pp
        else:
            content = content_comm
        url = 'https://beta.character.ai/' + i
        df = pd.DataFrame(data=[[name, date, content, url]], columns=['platform', 'date', 'content', 'url'])
        df.to_csv(path + name + "_" + i + "_" + date + ".csv", index=False)


#the codes for scraping Jasper
def Jasper():
    name = "Jasper"
    path = 'Data_DayByDay/' + name + '/'
    date = datetime.date.today().strftime('%Y%m%d')
    if not os.path.exists(path):
        os.makedirs(path)
    id = [("terms","https://legal.jasper.ai/?_gl=1"),
          ("privacy","https://privacy.jasper.ai/policies?_gl=1")]
    for i in id[0:1]:
        if i[0] =="terms":
            res = requests.get(i[1], headers=headers_2)
            selector = etree.HTML(res.text.encode('utf-8-sig'))
            infos = selector.xpath('//*[@id="contract-versions-269077"]//text()')
            content = '\n'.join(infos).strip()
            replace_rules = [("\u200d",""),('\n\”\)', '”)'),("“\n","“"),("\n”","”"),("\n\)", ")"),("\(\n", "("),(r" \n", "\n"),("\n,", ","),(" +", " "),("\n+", "\n"),("\n\.", "."),("\n:\n", ":"),("\n ","\n"),(" +", " "),("\n+", "\n"),("\n\n", "\n")]
            for rule in replace_rules:
                content = re.sub(rule[0], rule[1], content)
            content = content.replace("\n*\n", "")
            content = content.replace("* * ", "* ")
            index = content.find("* * * Contracts* * ")
            if index != -1:
                content = content[index + len("Contracts* *")+7:]
            print(content)
            df = pd.DataFrame(data=[[name, date, content, i[1]]], columns=['platform', 'date', 'content', 'url'])
            df.to_csv(path + name + "_" + i[0] + "_" + date + ".csv", index=False)


#the codes for scraping BlenderBot
def BlenderBot():
    name = "BlenderBot"
    path = 'Data_DayByDay/' + name + '/'
    if not os.path.exists(path):
        os.makedirs(path)

    # terms
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument(f'user-agent={user_agent}')
    # options.add_argument('start-maximized')
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    url_1 = 'https://geo-not-available.blenderbot.ai/tos'
    driver.get(url_1)
    res = driver.page_source
    selector = etree.HTML(res)
    infos = selector.xpath('//div[@class="tos-root"]//text()')
    content = '\n'.join(infos).strip()
    content = re.sub(r" \n", " ", content)
    content = re.sub(r"\n\)", ")", content)
    content = re.sub(r"available at\n", "available at ", content)
    date = datetime.date.today().strftime('%Y%m%d')
    df = pd.DataFrame(data=[[name, date, content, url_1]],
                      columns=['platform', 'date', 'content', 'url'])
    df.to_csv(path + name + "_terms_" + date + ".csv", index=False)

    # privacy
    headers_2 = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36',
        'Accept-Language': 'en'
    }
    url_2 = 'https://mbasic.facebook.com/privacy/policy/printable'
    res = requests.get(url_2, headers=headers_2)
    res_text = res.text
    selector = etree.HTML(res_text.encode('utf-8'))
    infos_2 = selector.xpath('//div[@class="t"]//text()')
    content = '* '.join(infos_2).strip()  # seperated by "*+space" for future dividing
    print(content)
    df = pd.DataFrame(data=[[name, date, content, url_2]],
                      columns=['platform', 'date', 'content', 'url'])
    df.to_csv(path + name + "_privacy_" + date + ".csv", index=False)


#the codes for scraping Writesonic
def Writesonic():
    name = "Writesonic"
    path = 'Data_DayByDay/' + name + '/'
    if not os.path.exists(path):
        os.makedirs(path)
    id = ["terms", "privacy-policy"]
    for i in id[1:]:
        url = 'https://writesonic.com/' + i
        print(url)
        res = requests.get(url, headers=headers_2)
        #print(res.text)
        res.encoding = "utf-8"
        selector = etree.HTML(res.text)
        infos = selector.xpath('/html/body/div[1]/main/div/div/div/div[2]/div/div//text()')
        content = '\n'.join(infos).strip()
        content = content.replace(u'\xa0', ' ').strip()
        content = content.replace(u'\u200d', ' ').strip()
        content = re.sub(r" \n", " ", content).strip()
        content = re.sub(r"\n ", " ", content).strip()
        content = re.sub(r"\n“", "“", content).strip()
        content = re.sub(r"\n\)", ")", content).strip()
        content = re.sub(r"\n\(", "(", content).strip()
        content = re.sub("\n,", ",", content).strip()
        content = re.sub("\n\.", ".", content).strip()
        date = datetime.date.today().strftime('%Y%m%d')
        print(content)
        df = pd.DataFrame(data=[[name, date, content, url]],
                          columns=['platform', 'date', 'content', 'url'])
        df.to_csv(path + name + "_" + i + "_" + date + ".csv", index=False)


#the codes for scraping Replika
def Replika():
    name = "Replika"
    path = 'Data_DayByDay/' + name + '/'
    if not os.path.exists(path):
        os.makedirs(path)
    id = ["terms", "privacy"]
    for i in id:
        url = 'https://replika.com/legal/' + i
        res = requests.get(url, headers=headers)
        res.encoding = "utf-8"
        selector = etree.HTML(res.text)
        infos = selector.xpath('//div/div[1]/div/div//text()')
        content = ''.join(infos).strip()
        content = re.sub(r"\n+", "\n", content).strip()
        date = datetime.date.today().strftime('%Y%m%d')
        print(content)
        df = pd.DataFrame(data=[[name, date, content, url]],
                          columns=['platform', 'date', 'content', 'url'])
        df.to_csv(path + name + "_" + i + "_" + date + ".csv", index=False)


#the codes for scraping ELSA
def ELSA():
    name = "ELSA"
    path = 'Data_DayByDay/' + name + '/'
    if not os.path.exists(path):
        os.makedirs(path)
    id = ["terms", "privacy"]
    for i in id:
        url = 'https://elsaspeak.com/en/' + i
        res = requests.get(url, headers=headers)
        selector = etree.HTML(res.text)
        if i == "terms":
            infos = selector.xpath('//div[@class="container"]//text()')
        else:
            infos = selector.xpath('//div[@class="page-container"]//text()')
        content = ''.join(infos).strip()
        content = content.replace(u'\xa0', ' ').strip()
        content = content.replace('\u200E', '').strip()
        content = re.sub(r" +", " ", content).strip()
        content = re.sub(r"\n+", "\n", content).strip()
        date = datetime.date.today().strftime('%Y%m%d')
        print(content)
        df = pd.DataFrame(data=[[name, date, content, url]],
                          columns=['platform', 'date', 'content', 'url'])
        df.to_csv(path + name + "_" + i + "_" + date + ".csv", index=False)


#the codes for scraping Youchat
"""def YouChat():
    ###########
    name = "YouChat"
    path = 'Data_DayByDay/' + name + '/'
    if not os.path.exists(path):
        os.makedirs(path)
    date = datetime.date.today().strftime('%Y%m%d')
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36',
        #'Cookie': 'uuid_guest=5682fb9a-7d98-4a0b-81b0-071b3144af1c; cf_chl_2=965a39f765bfd8e; cf_clearance=wO10wFzKuBux1u3fGyOYcBJNco2ne0tymkkHXyfPQHM-1678445724-0-250; __cf_bm=SJ1h6ie1zdJsxGrqiaaZ.lYPI0TKQBsHaXeXHkL3K3s-1678445724-0-AdUbaBRW+WUdkS5a9ssOhUisegdvzb5K3dnpj9hi4DizHdi8PcsgFC7hVa1KyoTkZJw8d+Jx0tDsXDt+8891wC8=; ldflags=%7B%22abCodeSnippetEmbeddingSearch%22%3A%22treatment%22%2C%22abCodeSnippetEmbeddingSearchV2%22%3A%22neither%22%2C%22abDegradationSwapTopAppWithBottomApp%22%3A%22neither%22%2C%22abDegradationSwapTopAppWithHighestWeb%22%3A%22neither%22%2C%22abDegradationSwapTopWebWithBottomWeb%22%3A%22neither%22%2C%22abDegradationSwapTopWebWithHighestApp%22%3A%22neither%22%2C%22abDegradeAppRankingForSomeIntents%22%3A%22neither%22%2C%22abFeaturedSnippet%22%3A%22control%22%2C%22abHomePageSearchToYouChat%22%3A%22treatment%22%2C%22abInformationalWebSnippet%22%3A%22neither%22%2C%22abMakeDefaultSerpPageCta%22%3A%22treatment%22%2C%22abOnboardingMovieForGuests%22%3A%22control%22%2C%22abOptimus%22%3A%22neither%22%2C%22abQuickAnswer%22%3A%22control%22%2C%22abReduceAppSearchTimeout%22%3A%22neither%22%2C%22abReduceNumApps%22%3A%22treatment%22%2C%22abRemoveBadUrlsV2%22%3A%22abRemoveBadUrls_v2%22%2C%22abShowLandingPageGradient%22%3A%22neither%22%2C%22abShowSignInButton%22%3A%22treatment%22%2C%22abSkipNavigationalWebIfNotHighPrecision%22%3A%22neither%22%2C%22abStreamAppRankingsAfterApps%22%3A%22control%22%2C%22abThumbsAndDropdownAsSingleButton%22%3A%22control%22%2C%22abUseAppsForYouChat%22%3A%22treatment%22%2C%22abUseBraveSearch%22%3A%22neither%22%2C%22abUseMultitaskLlm%22%3A%22treatment%22%2C%22abUseQueryRewriter%22%3A%22treatment%22%2C%22abYouChatCapGuest%22%3A%22cap_0%22%2C%22abYouChatPrivateAds%22%3A%22neither%22%2C%22chatModelFlag%22%3A%22neither%22%2C%22controlUsedOpenAiModel%22%3A%22default%22%2C%22enableAppRankingV2%22%3Atrue%2C%22enableAppsPreferences%22%3Atrue%2C%22enableChatSpecificHeader%22%3Afalse%2C%22enableClaudeForFinance%22%3Afalse%2C%22enableLlmRanker%22%3A%22ft%22%2C%22enableMinCitationsForYouChat%22%3A%22treatment%22%2C%22enableProfilePage%22%3Atrue%2C%22enableYouChatMobileNudge%22%3Atrue%2C%22llmOrder%22%3A%22fastest%22%2C%22oneClickChatTurnFeedback%22%3A%22neither%22%2C%22shouldShowYouChatRightLine%22%3Atrue%2C%22showSuggestedSearchPills%22%3Afalse%2C%22showYouchat%22%3A%22treatment%22%2C%22useCacheForChatRetrieval%22%3A%22neither%22%2C%22useChatHistoryCache%22%3A%22treatment%22%2C%22usePermChatHistory%22%3A%22treatment%22%2C%22useYouChatConvoImageGen%22%3A%22control%22%2C%22validateUser%22%3A%22on%22%7D; safesearch_guest=Moderate'
    }
    user_agent = headers['User-Agent']
    #cookie = headers['Cookie']
    ###########
    id = ["terms", "privacy"]
    for i in id:
        url = "https://you.com/legal/" + i
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument(f'user-agent={user_agent}')
        #options.add_argument(f'cookie={cookie}')
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
        driver.get(url)
        driver.implicitly_wait(10)
        # print(driver.title)
        res = driver.page_source
        selector = etree.HTML(res)
        infos = selector.xpath(
            '//p//text()|//a//text()|//b//text()|//li//text()|//strong//text()|//div//text()|//h1//text()|//h2//text()|//h3//text()|//h4//text()')
        for l in range(0, len(infos)):
            if infos[l].endswith(' ') or infos[l].endswith(',') or infos[l].endswith('.') or infos[l].endswith(':') or \
                    infos[l].endswith(';'):
                pass
            else:
                try:
                    infos[l - 1] = infos[l - 1] + '\n'
                    infos[l] = infos[l] + '\n'
                except:
                    pass
        content = ''.join(infos).strip()
        removal = ['\u200b', '**', '|', '\xa0', '\u200b']
        for r in removal:
            content = content.replace(r, '')
        clean_format = (
            (r"\t", "\n"), ('-+', ' '), (' +', ' '), (r"\n +", "\n"), (r"\r", "\n"), (r"\\n\\n", "\n"),
            (r" \\n ", "\n"),
            (r"\\n", "\n"), (r"\\t", "\n"), (r"\\", "\n"), (r"\n \n", "\n"), (r"\n+", "\n"), ('"\n', '"'), ('\n"', '"'),
            ("\'s", "'s"), ('â\x80\x9c', '“'), ('â\x80\x9d', '”'), ('â\x80\x93', '-'), ('â\x80\x99', '’'),
            ('â\x80\x98', '‘'))
        for element in clean_format:
            content = re.sub(element[0], element[1], content)
        print(content)
        ###########
        df = pd.DataFrame(data=[[name, date, content, url]], columns=['platform', 'date', 'content', 'url'])
        df.to_csv(path + name + "_" + i + '_' + date + ".csv", index=False)
        driver.close()"""


#the codes for scraping Alexa
def Alexa():
    ###########
    name = "Alexa"
    path = 'Data_DayByDay/' + name + '/'
    if not os.path.exists(path):
        os.makedirs(path)
    date = datetime.date.today().strftime('%Y%m%d')
    headers = {'Connection': 'Keep-Alive',
               'Accept': 'text/html, application/xhtml+xml, */*',
               'Accept-Language': 'en-US,en;q=0.8',
               'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'
               }
    ###########
    id = [('terms','201809740'), ('privacy','GVP69FUJ48X9DK8V')]
    for i in id:
        url = 'https://www.amazon.com/gp/help/customer/display.html?nodeId=' + i[1]
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument(f'user-agent={headers["User-Agent"]}')
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
        driver.get(url)
        driver.implicitly_wait(3)
        res = driver.page_source
        selector = etree.HTML(res)
        infos = selector.xpath('//*[@class="help-service-content"]//text()')
        content = ''.join(infos).strip()
        clean_format = (("'\xa0'",""),(r"\t", "\n"), (' +', ' '), (r"\n +", "\n"), (r"\r", "\n"), (r"\n+", "\n"))
        for element in clean_format:
            content = re.sub(element[0], element[1], content)
        print(content)
        df = pd.DataFrame(data=[[name, date, content, url]], columns=['platform', 'date', 'content', 'url'])
        df.to_csv(path + name + "_" + i[0] + '_' + date + ".csv", index=False)
        driver.close()

#the codes for scraping Cortana
def Cortana():
    name = "Cortana"
    path = 'Data_DayByDay/' + name + '/'
    if not os.path.exists(path):
        os.makedirs(path)
    date = datetime.date.today().strftime('%Y%m%d')
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36'
    }
    ###########
    url = 'https://support.microsoft.com/en-us/windows/cortana-and-privacy-47e5856e-3680-d930-22e1-71ec6cdde231'
    res = requests.get(url, headers=headers)
    selector = etree.HTML(res.text)
    infos = selector.xpath('//*[@id="supArticleContent"]//text()')
    language = selector.get('lang')
    del infos[infos.index('SUBSCRIBE RSS FEEDS') - 1:-1]
    content = ''.join(infos).strip()
    content = content.replace(u'\xa0', ' ').replace(u"\u202F", ' ')
    clean_format = ((r"\t", "\n"), (' +', ' '), (r"\n +", "\n"), (r"Top of page", "\n"), (r"\r", "\n"), (r"\n+", "\n"))
    for element in clean_format:
        content = re.sub(element[0], element[1], content)
    print(content)
    df = pd.DataFrame(data=[[name, date, content, url]], columns=['platform', 'date', 'content', 'url'])
    df.to_csv(path + name + "_" + 'privacy' + '_' + language + '_' + date + ".csv", index=False)


#the codes for scraping Mycroft
def Mycroft():
    name = "Mycroft"
    path = 'Data_DayByDay/' + name + '/'
    if not os.path.exists(path):
        os.makedirs(path)
    date = datetime.date.today().strftime('%Y%m%d')
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36'
    }
    ###########
    id = ['terms-of-use/', 'privacy-policy/']
    for i in id:
        url = 'https://mycroft.ai/embed-' + i
        res = requests.get(url, headers=headers)
        if 'terms-of-use/' in url:
            selector = etree.HTML(res.text)
            infos = selector.xpath('//div/text()')
        else:
            info = res.text[res.text.rfind('\n<html><body><p>'):]
            selector = etree.HTML(info)
            infos = selector.xpath('//*/text()')
        content = ''.join(infos).strip()
        clean_format = ((r"\t", "\n"), (' +', ' '), (r"\n +", "\n"), (r"\r", "\n"), (r"\n+", "\n"))
        for element in clean_format:
            content = re.sub(element[0], element[1], content)
        language = etree.HTML(res.text).get('lang')
        print(content)
        df = pd.DataFrame(data=[[name, date, content, url]], columns=['platform', 'date', 'content', 'url'])
        df.to_csv(path + name + "_" + i[:-1] + '_' + language + '_' + date + ".csv", index=False)


#the codes for scraping Google_Assistant
def Google_Assistant():
    name = "Google Assistant"
    path = 'Data_DayByDay/' + name + '/'
    if not os.path.exists(path):
        os.makedirs(path)
    date = datetime.date.today().strftime('%Y%m%d')
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36'
    }
    ###########
    url = 'https://developers.google.com/assistant/community/terms'
    res = requests.get(url, headers=headers)
    selector = etree.HTML(res.text)
    note = selector.xpath('///*[@id="gc-wrapper"]/main/devsite-content/article/div[1]//text()')[4:-3]
    note.append('.\n')
    info = selector.xpath('//*[@id="gc-wrapper"]/main/devsite-content/article/div[3]//text()')
    infos = note + info
    content = ''.join(infos).strip()
    clean_format = ((r"\t", "\n"), (' +', ' '), (r"\n +", "\n"), (r"\r", "\n"), (r"\n+", "\n"))
    for element in clean_format:
        content = re.sub(element[0], element[1], content)
    language = etree.HTML(res.text).get('lang')
    print(content)
    df = pd.DataFrame(data=[[name, date, content, url]], columns=['platform', 'date', 'content', 'url'])
    df.to_csv(path + name + "_" + 'terms' + '_' + language + '_' + date + ".csv", index=False)


#the codes for scraping Reddit
def Reddit():
    name = "Reddit"
    path = 'Data_DayByDay/' + name + '/'
    if not os.path.exists(path):
        os.makedirs(path)
    date = datetime.date.today().strftime('%Y%m%d')
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36'
    }
    ###########
    id = [('redditinc', 'user-agreement'), ('reddit', 'privacy-policy')]
    for item in id:
        url = 'https://www.{}.com/policies/{}'.format(item[0], item[1])
        res = requests.get(url, headers=headers)
        language = etree.HTML(res.text).get('lang')
        selector = etree.HTML(res.text)
        if 'user-agreement' in url:
            infos = selector.xpath('//*[@id="content"]//text()')
            del infos[:infos.index('Reddit User Agreement')]
        else:
            infos = selector.xpath('//*[@id="main-content"]//text()')
            del infos[:infos.index('Reddit Privacy Policy')]
        content = ''.join(infos).strip()
        removal = ['\u200b', '**', '|']
        for r in removal:
            content = content.replace(r, '')
        clean_format = (
            (r"\t", "\n"), ('-+', ' '), (' +', ' '), (r"\n +", "\n"), (r"\r", "\n"), (r"\\n\\n", "\n"),
            (r" \\n ", "\n"),
            (r"\\n", "\n"), (r"\\t", "\n"), (r"\\", "\n"), (r"\n \n", "\n"), (r"\n+", "\n"), ('"\n', '"'), ('\n"', '"'),
            ("\'s", "'s"))
        for element in clean_format:
            content = re.sub(element[0], element[1], content)
        print(content)
        df = pd.DataFrame(data=[[name, date, content, url]], columns=['platform', 'date', 'content', 'url'])
        df.to_csv(path + name + "_" + item[1] + '_' + date + ".csv", index=False)


#the codes for scraping Twitch
def Twitch():
    ###########
    name = "Twitch"
    path = 'Data_DayByDay/' + name + '/'
    if not os.path.exists(path):
        os.makedirs(path)
    date = datetime.date.today().strftime('%Y%m%d')
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36'
    }
    ###########
    id = ['terms-of-service', 'privacy-notice']
    for i in id:
        url = 'https://www.twitch.tv/p/en/legal/' + i + '/'
        res = requests.get(url, headers=headers)
        selector = etree.HTML(res.text)
        infos = selector.xpath(
            '//*[@id="content__wrapper"]/div/div/div[2]/div[2]/div[1]/div/div//text()|//*[@id="content__wrapper"]/div/div/div[2]/div[2]/div[2]/div//text()')
        content = ''.join(infos).strip()
        removal = ['\u200b', '\xa0', '**', '|']
        for r in removal:
            content = content.replace(r, '')
        clean_format = (
            (r"\t", "\n"), ('-+', ' '), (' +', ' '), (r"\n +", "\n"), (r"\r", "\n"), (r"\\n\\n", "\n"),
            (r" \\n ", "\n"),
            (r"\\n", "\n"), (r"\\t", "\n"), (r"\\", "\n"), (r"\n \n", "\n"), (r"\n+", "\n"), ('"\n', '"'), ('\n"', '"'),
            ("\'s", "'s"), ('â\x80\x9c', '“'), ('â\x80\x9d', '”'), ('â\x80\x93', '-'), ('â\x80\x99', '’'),
            ('â\x80\x98', '‘'))
        for element in clean_format:
            content = re.sub(element[0], element[1], content)
        print(content)
        df = pd.DataFrame(data=[[name, date, content, url]], columns=['platform', 'date', 'content', 'url'])
        df.to_csv(path + name + "_" + i + '_' + date + ".csv", index=False)


#the codes for scraping Snapask
def Snapask():
    ###########
    def cleaning(stringdata):
        x = []
        for num in range(0, 11):
            num = str(num)
            x.append((num + '\.' + '\n', num + '.'))
            x.append(('[(]' + num + '[)]', '\n' + '(' + num + ')'))
            x.append((num + '\n', num + ' '))
            x.append(('\n' + num + ' ', num + ' '))
        y = []
        for i in range(97, 123):
            i = chr(i)
            y.append((" " + i + "[)]", "\n" + i + ")"))
            y.append(("[(]" + i + "[)]", "\n" + "(" + i + ")"))
        z = []
        for num in range(0, 67):
            num = str(num)
            z.append((" " + num + '\.', '\n' + num + '.'))
        clean_format = [
            ("[|]", ""), (r"\\\\", ""), ("-+", "-"), (r"\\t", ""), (r"\\n\\n", ""), (r"\\n", " "), (" +", " "),
            ("\n ", "\n"), ("\n+", "\n"), ("- -", ""), ("-[(]", "- ("), ("- ", " "), (r"\\", ""), (":-", ":"),
            ("[(]e[)]\n", "(e)"), ("\n[(]f[)]\n", "(f)"), ("[(]ii", "\n(ii"), ("[(]iv", "\n(iv"), ("\n“", "“"),
            ("”\n", "” "),
            ("(\\[)(\\])", ""), ('"\}\}\},', ''), ("\n,", ","), ("\n\.", "."), ('\n"', '"'), ('"\n', '"'),
            ("a\. \n", "a. "),
            ("a\.\n", "a. "), ("b\. \n", "b. "), ("c\. \n", "c. ")]
        u = [("US[$]\n5", "US$5"), ("two\n[(]2[)]", "two(2)"), ("six \n[(][)]", "six(6)"), ("part\n[(]s[)]", "part(s)"),
             ("six \n[(][)]", "six(6)"), ("User\n[(]s[)]", "User(s)"), ("plan\n[(]s[)]", "plan(s)"),
             ("service\n[(]s[)]", "service(s)"), ('","tutor"[:]"', '\n'), ("\n5\.00", " 5.00"), ("\n6\.00", " 6.00"),
             ("Total amount ", "\nTotal amount "), ("\n4.8; ", " >= 4.8; "),
             ("\ncs-hk[@]snapask\.com\.\n", "cs-hk@snapask.com."),
             ("\nnext month\.\n", "next month."), ("10 invalidated sessions\n", "10 invalidated sessions "),
             ("have been favourited 10 times, and", "have been favourited >= 10 times, and"),
             ("\n5 questions\n", "5 questions"),
             ("a flat-rate of \n", "a flat-rate of "), ("monthly reward of \nHKD 750 ", "monthly reward of HKD 750\n"),
             ("10 invalidated\nsessions", "10 invalidated sessions"), ("2 levels of", "\n2 levels of"),
             ("5 remaining sessions", "\n5 remaining sessions")]
        clean_format = x + clean_format + y + z + u
        for pattern in clean_format:
            stringdata = re.sub(pattern[0], pattern[1], stringdata)
        return stringdata

    ###########
    name = "Snapask"
    path = 'Data_DayByDay/' + name + '/'
    if not os.path.exists(path):
        os.makedirs(path)
    date = datetime.date.today().strftime('%Y%m%d')
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36'
    }

    ###########
    filename = ["terms", "privacy", "privacy", "community(tutor)"]
    urlparameter = ['https://snapask.com/en-hk/terms', 'https://snapask.com/en-hk/privacy',
                    'https://snapask.com/zh-hk/privacy']
    termsname = list(zip(filename, urlparameter))
    for i in termsname:
        res = requests.get(i[1], headers=headers)
        if 'privacy' in i[0]:
            try:
                info = res.text[res.text.rfind('"en-hk":{"privacy":{"privacy":{"content":{"web":"**'):]
                info = info[:info.rfind(
                    '"seo":{"seo":{"landing":{"title":"A school squeezed into Snapask. 24/7 1-on-1 online tutoring"')]
            except:
                info = res.text[res.text.rfind('"zh-hk":{"privacy":{"privacy":{"content":{"web":"**'):]
                info = info[:info.rfind('"seo":{"seo":{"landing":{"title":"一站式網上補習問功課平台 星級導師 24小時助你學習解難"')]
        elif 'terms' in i[0]:
            info = res.text[res.text.rfind('"terms":{"terms":{"content":{"student":"**'):]
            info = info[:info.rfind('confirmDialog":{"title":"We\'ve updated our Terms of Service and Privacy Policy')]
        else:
            info = res.text[res.text.rfind('</style></head>'):]
            #print(info)
        selector = etree.HTML(info)
        infos = selector.xpath('//*/text()')
        del infos[0]
        content = '\n'.join(infos).strip()
        #  cleaning  #
        p = re.compile(r'[^\x00-\x7f]')
        content = re.sub(p, '', content)
        if i[0] != "community(tutor)":
            content = re.sub("[\*\*]", "", content)
        else:
            pass
        content = cleaning(content)
        #print(content)
        #  saving  #
        df = pd.DataFrame(data=[[name, date, content, i[1]]], columns=['platform', 'date', 'content', 'url'])
        df.to_csv(path + name + "_" + i[0] + '_' + 'en'+ "_" + date + ".csv", index=False)

#the codes for scraping Upwork
def Upwork():
    name = "Upwork"
    path = 'Data_DayByDay/' + name + '/'
    if not os.path.exists(path):
        os.makedirs(path)
    date = datetime.date.today().strftime("%Y%m%d")
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 '
                      'Safari/537.36'
    }
    user_agent = headers['User-Agent']
    id = [("user_agreement","useragreement"),("terms","terms-of-use"),("privacy","privacy"),("community","")]
    for i in id:
        if i[0] == "community":
            url="https://community.upwork.com/t5/FAQs/Community-Guidelines/ta-p/" \
                "1064768#:~:text=Your%20posts%20may%20be%20permanent,organized%20and%20helpful%20for%20everyone"
        else:
            url = "https://www.upwork.com/legal#" +i[1]+"/"
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument(f'user-agent={user_agent}')
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
        driver.get(url)
        res = driver.page_source
        selector = etree.HTML(res)
        infos = selector.xpath('//*[@id="contract-id-15858"]//text()|//*[@id="contract-id-17439"]//text()|'
                               '//*[@id="contract-id-15859"]//text()|//*[@id="link_2"]//text()|//*[@id="messageview2"]//text()')
        trash = selector.xpath('//*[@id="messageview2"]/div[2]/div/div[2]/div[1]/div/style/text()')
        #print(trash)
        if i[0]=='community':
            if trash[0] in infos:
                infos.remove(trash[0])
        infos = [eachinfos.encode('utf-8').decode('utf-8').replace('\xa0','') for eachinfos in infos]
        #print(infos)
        content = '\n'.join(infos).strip()
        a = selector.xpath('//a//text()|//u//text()')
        em = selector.xpath('//*/span/em//text()|//*/strong/em//text()')
        strong = selector.xpath('//*/span/em/strong//text()')
        pattern = [('\n' + A + '\n', A + ' ') for A in a] + [('\n' + A + ', ' + '\n', A + ', ') for A in a] + \
                  [('\n' + A.strip() + '\n', A) for A in a] + [('\n' + A.strip() + ', ' + '\n', A + ', ') for A in a] + \
                  [('\n' + A + '\n', A) for A in em] + [('\n' + A, A) for A in em] + \
                  [('\n' + A + '\n+', A + ' ') for A in strong] + \
                  [('\t','\n'),("\n“Notify Moderator” \n","“Notify Moderator” "),("\nhere","here"),("\nclient","client"),("\nClients , Freelancers", " Clients, Freelancers"),
                   ("\nAgencies, or Site Visitors\n", "Agencies, or Site Visitors ")]+\
                  [("[(]“\n","(“"),("\n”[)]","”)"),("\n”[)].\n","”). "),("\n“\n","“"),("\n”\n","”"),("\n,",","),("\n“","“"),("\n”","”"),
                   ("\n\. ",". \n"),("\.\.+","."),("\n: ",": \n"),("\n\.” ",".” "),("\n\.\n",""),(" +"," "),("\n +","\n"),
                   ("\n+","\n")]
        for p in pattern:
            content = re.sub(p[0],p[1],content)
        print(content)
        df = pd.DataFrame(data=[[name, date, content, url]],
                          columns=['platform', 'date', 'content', 'url'])
        df.to_csv(path + name + "_" + i[0] + "_" + date + ".csv", index=False)
        driver.close()

def Meetup():
    def cleaning(stringdata):
        clean_format = [
            ("\n\t+", " "), ("\t+", "\n"), ("\xa0", ""),
            ("[|]", ""), (r"\\\\", ""), ("-+", "-"), (r"\\t", ""), (r"\\n\\n", ""), (r"\\n", " "), (" +", " "),
            ("\n ", "\n"), ("\n+", "\n"), ("- -", ""), ("-[(]", "- ("), ("- ", " "), (r"\\", ""),
            (":-", ":"), ("\n:", ":"),("\n;", ";"), ('<! ', ''), (' ->', ''),
            ("\n“", "“"), ("“\n", "“"), ("”\n", "” "), ("\n”", "”"), ("\n[)]", ")"),
            ("(\\[)(\\])", ""), ('"\}\}\},', ''), ("\n,", ","), ("\n\.", "."), ('\n"', '"'), ('"\n', '"'),(' +', ' '),('\n+', '\n')]
        for number in range(0, 16):
            number = str(number)
            clean_format.append((number + '\.' + '\n', number + '.'))
            clean_format.append((number + '\n', number + ' '))
            clean_format.append((number + '\. ' + '\n', number + '. '))
            clean_format.append((number + ' \n', number + ' '))
        for cha in range(97, 115):  # 122 is z
            clean_format.append(("[(]" + chr(cha) + "[)]", "\n" + "(" + chr(cha) + ")"))
        for cha in range(65, 91):
            clean_format.append(("[(]" + chr(cha) + "[)]", "\n" + "(" + chr(cha) + ")"))
        RN = ["i", "ii", "iii", "iv", "v", "vi", "vii", "viii", "ix", "x"]
        RN = RN + [r.upper() for r in RN]
        for r in RN:
            clean_format.append(("[(]" + r + "[)]", "\n" + "(" + r + ")"))
        clean_format.append(("\n+", "\n"))
        clean_format.append(("\.\.", "."))
        for pattern in clean_format:
            stringdata = re.sub(pattern[0], pattern[1], stringdata)
        return stringdata

    ###########
    name = "Meetup"
    path = 'Data_DayByDay/' + name + '/'
    if not os.path.exists(path):
        os.makedirs(path)
    date = datetime.date.today().strftime('%Y%m%d')
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36'}
    user_agent = headers['User-Agent']
    ###########
    # terms + privacy#
    filename = ['terms', 'privacy', 'community']
    urlparameter = ['https://help.meetup.com/hc/en-us/articles/360027447252',
                    'https://help.meetup.com/hc/en-us/articles/360044422391-Privacy-Policy',
                    'https://help.meetup.com/hc/en-us/sections/360000683791-Community-Guidelines']
    termsname = list(zip(filename, urlparameter))
    for i in termsname[0:2]:
        #print(i)
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument(f'user-agent={user_agent}')
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
        driver.get(i[1])
        driver.implicitly_wait(2)
        # test = driver.find_elements(By.CLASS_NAME, "nav-link")
        res = driver.page_source
        selector = etree.HTML(res)
        infos = selector.xpath('//*[@id="article-container"]/article//text()')
        content = '\n'.join(infos).strip()
        p = re.compile(r'[^\x00-\x7f]')
        content = re.sub(p, '', content)
        content = cleaning(content)
        print(content)
        df = pd.DataFrame(data=[[name, date, content, i[1]]], columns=['platform', 'date', 'content', 'url'])
        df.to_csv(path + name + "_" + i[0] + "_" + date + ".csv", index=False)
        # driver.close()
    ###########
    # community#
    driver.get(termsname[2][1])
    driver.implicitly_wait(5)
    ress = driver.page_source
    link = etree.HTML(ress).xpath(
        '//*[@id="section-wrapper-id-360000683791"]/div/div[4]/div/div/section/ul/li/a//@href')
    linkname = etree.HTML(ress).xpath(
        '//*[@id="section-wrapper-id-360000683791"]/div/div[4]/div/div/section/ul/li/a//text()')

    urllist = ["https://help.meetup.com" + i for i in link]
    urllist_name = list(zip(linkname, urllist))
    namelist = []
    datelist = []
    for i in urllist_name:
        driver.get(i[1])
        driver.implicitly_wait(5)
        res = driver.page_source
        infos = etree.HTML(res).xpath('//*[@id="article-container"]/article/header//text()|//*[@id="article-container"]/article/section//text()')
        content = '\n'.join(infos).strip()
        content = cleaning(content)
        content = content.replace("\n\n","\n")
        print(content)
        namelist.append(name + i[0])
        datelist.append(date)
        df = pd.DataFrame(data=[[namelist, datelist, content, i[1]]], columns=['platform', 'date', 'content', 'url'])
        df.to_csv(path + name + "_" + 'community' + '_' + date + ".csv", index=False)
    driver.close()


#the codes for scraping Didi
def DiDi():
    #############
    def recleaning(patterns, stringdata):
        for pattern in patterns:
            stringdata = re.sub(pattern[0], pattern[1], stringdata)
        return stringdata

    def cleaning(stringdata):
        clean_format = [
            ("\t+", "\n"), ("\xa0", ""),
            ("[|]", ""), (r"\\\\", ""), ("-+", "-"), (r"\\t", ""), (r"\\n\\n", ""), (r"\\n", " "), (" +", " "),
            ("\n ", "\n"), ("\n+", "\n"), ("- -", ""), ("-[(]", "- ("), ("- ", " "), (r"\\", ""),
            (":-", ":"), ("\n:", ":"),
            ("\n“", "“"), ("“\n", "“"), ("”\n", "” "), ("\n”", "”"), ("\n[)]", ")"),
            ("(\\[)(\\])", ""), ('"\}\}\},', ''), ("\n,", ","), ("\n\.", "."), ('\n"', '"'), ('"\n', '"'),
            ("\n-\n", "\n")
        ]
        for number in range(0, 16):
            number = str(number)
            clean_format.append((number + '\.' + '\n', number + '.'))
            clean_format.append((number + '\n', number + ' '))
            clean_format.append((number + '\. ' + '\n', number + '. '))
            clean_format.append((number + ' \n', number + ' '))
        for cha in range(97, 115):  # 122 is z
            clean_format.append((chr(cha) + "\.\n", chr(cha) + ". "))
            clean_format.append(("[(]" + chr(cha) + "[)]", "\n" + "(" + chr(cha) + ")"))
        for cha in range(65, 91):
            clean_format.append(("[(]" + chr(cha) + "[)]", "\n" + "(" + chr(cha) + ")"))
        RN = ["i", "ii", "iii", "iv", "v", "vi", "vii", "viii", "ix", "x"]
        for r in RN:
            clean_format.append((r + "\.\n", r + ". "))
        RN = RN + [r.upper() for r in RN]
        for r in RN:
            clean_format.append(("[(]" + r + "[)]", "\n" + "(" + r + ")"))
        clean_format.append(("\n+", "\n"))
        clean_format.append(("\.\.", "."))
        for pattern in clean_format:
            stringdata = re.sub(pattern[0], pattern[1], stringdata)
        return stringdata

    def lan(line):
        if '\u4e00' <= line <= '\u9fff':
            language = "zh"
        elif ('\u0041' <= line <= '\u005a') or ('\u0061' <= line <= '\u007a'):
            language = "en"
        else:
            language = ""
        return language

    #############
    name = "DiDi"
    path = 'Data_DayByDay/' + name + '/'
    if not os.path.exists(path):
        os.makedirs(path)
    date = datetime.date.today().strftime('%Y%m%d')
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36'
    }

    ###########
    # 香港及其他境外地区隐私及服务条款 #
    filename = ["terms", "privacy"]
    urlparameter = ['https://web.didiglobal.com/hk/legal/terms-of-service/',
                    'https://web.didiglobal.com/hk/legal/privacy-policy/', ]
    termsname = list(zip(filename, urlparameter))
    for i in termsname:
        res = requests.get(i[1], headers=headers)
        selector = etree.HTML(res.text)
        language = selector.get('lang')
        infos = selector.xpath('//*[@id="gatsby-focus-wrapper"]/section[2]//text()|'
                               '//*[@id="gatsby-focus-wrapper"]/section[1]/div[1]/div/h1//text()')
        b = [(" 在該等第三", "在該等第三")]
        #print(infos)
        content = '\n'.join(infos).strip()
        p = re.compile(r'[^\x00-\x7f]')
        content = re.sub(p, '', content)
        content = cleaning(content)
        content = recleaning(b, content)
        print(content)
        ###########
        df = pd.DataFrame(data=[[name, date, content, i[1]]], columns=['platform', 'date', 'content', 'url'])
        df.to_csv(path + name + "_" + i[0] + '_' + language + '_' + date + ".csv", index=False)
    ###########

    ###########
    # 司机服务条款及乘客服务条款 #
    html_terms = [
        ('driver_terms', 'https://img0.didiglobal.com/static/dpubimg/817178249ccdb3de62825ba80bb57bde/index.html'),
        ('passenger_terms', 'https://img0.didiglobal.com/static/dpubimg/dpub2_project_24777/index_24777.html')]
    for item in html_terms[1:2]:
        res = requests.get(item[1], headers=headers)
        selector = etree.HTML(res.text)
        language = selector.get('lang')
        head = selector.xpath('//*[@id="yy-text_2_6925388405"]/div/b//text()|'
                              '//*[@id="yy-text_3_9871576297"]/div/b//text()')
        infos = selector.xpath('//*[@id="scene_0"]//text()')
        infos = head + infos
        if item[0] == 'driver_terms':
            a = selector.xpath('//*[@id="yy-text_1_1278583891"]/div/div[17]/b//text()|'
                               '//*[@id="yy-text_1_1278583891"]/div/div[15]/b//text()|'
                               '//*[@id="yy-text_1_1278583891"]/div/div[11]/b//text()|'
                               '//*[@id="yy-text_1_1278583891"]/div/div[9]/b//text()|'
                               '//*[@id="yy-text_1_1278583891"]/div/div[7]/b//text()|'
                               '//*[@id="yy-text_1_1278583891"]/div/div[5]/b//text()|'
                               '//*[@id="yy-text_1_1278583891"]/div/div[3]/b//text()|'
                               '//*[@id="yy-text_1_1278583891"]/div/div[1]/span/b//text()|'
                               '//*[@id="yy-text_1_1278583891"]/div/div[73]/b//text()')
        else:
            a = selector.xpath('//*[@id="yy-text_2"]/div/div[4]/b//text()|'
                               '//*[@id="yy-text_2"]/div/div[6]/b//text()|'
                               '//*[@id="yy-text_2"]/div/div[97]/b//text()')
        p = re.compile(r'[^\x00-\x7f]')
        a = [re.sub(p, '', aa) for aa in a]
        b = [("\n" + aa + "\n", aa + " ") for aa in a] + \
            [("\n" + aa + "\.\n", aa + ".\n") for aa in a] + \
            [("\n" + aa + "\. \n", aa + ". \n") for aa in a] + \
            [("\n" + aa + "\. ", aa + ". ") for aa in a] + \
            [("\n" + aa + "[)]", aa + ")") for aa in a] + \
            [("\n" + aa + "[)]\.", aa + ").") for aa in a] + \
            [("\nDiDi Driver. ", "DiDi Driver. \n")] + \
            [("4\.Obligations", "4.bligations ")] + \
            [("DiDi Mobility Information", "\nDiDi Mobility Information")]
        content = '\n'.join(infos).strip()
        content = re.sub(p, '', content)
        content = cleaning(content)
        content = recleaning(b, content)
        print(content)
        ###########
        df = pd.DataFrame(data=[[name, date, content, item[1]]], columns=['platform', 'date', 'content', 'url'])
        df.to_csv(path + name + "_" + item[0] + '_' + language + '_' + date + ".csv", index=False)


#the codes for scraping Discord
def Discord():
    ###########
    def recleaning(patterns, stringdata):
        for pattern in patterns:
            stringdata = re.sub(pattern[0], pattern[1], stringdata)
        return stringdata

    def cleaning(stringdata):
        clean_format = [
            ("\t+", "\n"), ("\xa0", ""),
            ("[|]", ""), (r"\\\\", ""), ("-+", "-"), (r"\\t", ""), (r"\\n\\n", ""), (r"\\n", " "), (" +", " "),
            ("\n ", "\n"), ("\n+", "\n"), ("- -", ""), ("-[(]", "- ("), ("- ", " "), (r"\\", ""),
            (":-", ":"), ("\n:", ":"),
            ("\n“", "“"), ("“\n", "“"), ("”\n", "” "), ("\n”", "”"), ("\n[)]", ")"),
            ("(\\[)(\\])", ""), ('"\}\}\},', ''), ("\n,", ","), ("\n\.", "."), ('\n"', '"'), ('"\n', '"'),
        ]
        for number in range(0, 16):
            number = str(number)
            clean_format.append((number + '\.' + '\n', number + '.'))
            clean_format.append((number + '\n', number + ' '))
            clean_format.append((number + '\. ' + '\n', number + '. '))
            clean_format.append((number + ' \n', number + ' '))
        for cha in range(97, 115):  # 122 is z
            clean_format.append(("[(]" + chr(cha) + "[)]", "\n" + "(" + chr(cha) + ")"))
        for cha in range(65, 91):
            clean_format.append(("[(]" + chr(cha) + "[)]", "\n" + "(" + chr(cha) + ")"))
        RN = ["i", "ii", "iii", "iv", "v", "vi", "vii", "viii", "ix", "x"]
        RN = RN + [r.upper() for r in RN]
        for r in RN:
            clean_format.append(("[(]" + r + "[)]", "\n" + "(" + r + ")"))
        clean_format.append(("\n+", "\n"))
        clean_format.append(("\.\.", "."))
        for pattern in clean_format:
            stringdata = re.sub(pattern[0], pattern[1], stringdata)
        return stringdata

    #############
    name = "Discord"
    path = 'Data_DayByDay/' + name + '/'
    if not os.path.exists(path):
        os.makedirs(path)
    date = datetime.date.today().strftime('%Y%m%d')
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 '
                      'Safari/537.36'
    }
    user_agent = headers['User-Agent']

    ###########
    filename = ["terms", "privacy", "community"]
    urlparameter = ['https://discord.com/terms',
                    'https://discord.com/privacy',
                    'https://discord.com/guidelines']
    termsname = list(zip(filename, urlparameter))
    for i in termsname[2:3]:
        res = requests.get(i[1], headers=headers)
        selector = etree.HTML(res.text)
        infos = selector.xpath('//html/body/div[2]/div[2]//text()')
        a = selector.xpath('//p/a//text()|li/a//text()|//li/em//text()')
        b = [("\n" + aa + "\n", aa) for aa in a] + \
            [("\n" + aa + ", \n", aa + ", ") for aa in a] + \
            [("\n" + aa + "\.\n", aa + ".\n") for aa in a] + \
            [("\nretain and display certain data\n", "retain and display certain data")] + \
            [("contact us at \n", "contact us at ")] + \
            [("1\. Welcome!", "\n1. Welcome!")] + \
            [("1\. Who we are", "\n1. Who we are")] + \
            [("\n16\. 17\. Welcome!", "")] + \
            [("1\. 2\. 3\. 4\. 5\. 6\. 7\. 8\. 9\. 10\. 11\. 12\. 13\. 14\. 15\. 16\. 17\. ", "\n")] + \
            [("\nNational Center for Missing & Exploited Children.",
              "National Center for Missing & Exploited Children.")]
        content = '\n'.join(infos).strip()
        p = re.compile(r'[^\x00-\x7f]')
        content = re.sub(p, '', content)
        content = cleaning(content)
        content = recleaning(b, content)
        print(content)

        ###########
        df = pd.DataFrame(data=[[name, date, content, i[1]]], columns=['platform', 'date', 'content', 'url'])
        df.to_csv(path + name + "_" + i[0] + '_' + date + ".csv", index=False)


#the codes for scraping Socratic
def Socratic():
    #############
    def recleaning(patterns, stringdata):
        for pattern in patterns:
            stringdata = re.sub(pattern[0], pattern[1], stringdata)
        return stringdata

    def cleaning(stringdata):
        clean_format = [
            ("\t+", "\n"), ("\xa0", ""),
            ("[|]", ""), (r"\\\\", ""), ("-+", "-"), (r"\\t", ""), (r"\\n\\n", ""), (r"\\n", " "), (" +", " "),
            ("\n ", "\n"), ("\n+", "\n"), ("- -", ""), ("-[(]", "- ("), ("- ", " "), (r"\\", ""),
            (":-", ":"), ("\n:", ":"),
            ("\n“", "“"), ("“\n", "“"), ("”\n", "” "), ("\n”", "”"), ("\n[)]", ")"),
            ("(\\[)(\\])", ""), ('"\}\}\},', ''), ("\n,", ","), ("\n\.", "."), ('\n"', '"'), ('"\n', '"'),
        ]
        for number in range(0, 16):
            number = str(number)
            clean_format.append((number + '\.' + '\n', number + '.'))
            clean_format.append((number + '\n', number + ' '))
            clean_format.append((number + '\. ' + '\n', number + '. '))
            clean_format.append((number + ' \n', number + ' '))
        for cha in range(97, 115):  # 122 is z
            clean_format.append(("[(]" + chr(cha) + "[)]", "\n" + "(" + chr(cha) + ")"))
        for cha in range(65, 91):
            clean_format.append(("[(]" + chr(cha) + "[)]", "\n" + "(" + chr(cha) + ")"))
        RN = ["i", "ii", "iii", "iv", "v", "vi", "vii", "viii", "ix", "x"]
        RN = RN + [r.upper() for r in RN]
        for r in RN:
            clean_format.append(("[(]" + r + "[)]", "\n" + "(" + r + ")"))
        clean_format.append(("\n+", "\n"))
        clean_format.append(("\.\.", "."))
        for pattern in clean_format:
            stringdata = re.sub(pattern[0], pattern[1], stringdata)
        return stringdata

    def lan(line):
        if '\u4e00' <= line <= '\u9fff':
            language = "zh"
        elif ('\u0041' <= line <= '\u005a') or ('\u0061' <= line <= '\u007a'):
            language = "en"
        else:
            language = ""
        return language

    #############
    name = "Socratic"
    path = 'Data_DayByDay/' + name + '/'
    if not os.path.exists(path):
        os.makedirs(path)
    date = datetime.date.today().strftime('%Y%m%d')
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 '
                      'Safari/537.36'
    }
    user_agent = headers['User-Agent']

    #############
    # terms + privacy #
    filename = ["terms", "privacy", "community"]
    urlparameter = ["https://policies.google.com/terms",
                    "https://policies.google.com/privacy",
                    "https://socratic.org/socratic/the-socratic-model/community-guidelines"]
    termsname = list(zip(filename, urlparameter))
    number1 = [str(num) for num in range(2, 14)]
    #print(number1)
    for i in termsname[0:2]:
        #print("-----" + i[0] + "-----")
        res = requests.get(i[1], headers=headers)
        selector = etree.HTML(res.text)
        if i[0] == 'terms':
            number1.remove("2")
            del number1[number1.index("9"):]
            infos = selector.xpath('//*[@id="yDmH0d"]/c-wiz/div/div[2]/div[2]/div[3]/c-wiz/div[1]/div//text()')
            for n in number1:
                infos = infos + selector.xpath(
                    '//*[@id="yDmH0d"]/c-wiz/div/div[2]/div[2]/div[3]/c-wiz/div[{}]/div//text()'.format(n))
            c = selector.xpath('//a//text()')  # remove the "/n" form the word with hyperlink
            d = selector.xpath('//li/b//text()')  # remove the "/n" from the word with strong font format
            d = d[2:]
            c = c[c.index("Archived versions"):]
            del c[c.index("Introduction"):c.index("About these terms") + 1]
            while 'Google' in c:
                c.remove('Google')
            head = selector.xpath('//h1//text()|//h2//text()|//h3//text()')
            head = head[head.index("What’s covered in these terms"):head.index("Definitions")]
            a = [A for A in c if A in c and A not in head]
            b = [('\n' + A + '\n ', A + ' ') for A in a] + \
                [('\n' + A + '\n,', A + ',') for A in a] + \
                [('\n' + A + '\n\.', A + '.') for A in a] + \
                [('\n' + A + '\n:', A + ':') for A in a] + \
                [('\n' + A + '\n', A + ' ') for A in a] + \
                [('\n' + A, A) for A in a] + \
                [(D + '\n', D + ' ') for D in d]
            e = [(" \nservices\n", " services "), ("\nservices\.", "services."),
                 ("\nservices,", "services,"), ("Removing your content", "\nRemoving your content"),
                 ("we’re required to do so to comply with a legal requirement or a court order",
                  "\nwe’re required to do so to comply with a legal requirement or a court order"),
                 ("\nsection;", " section;"), ("[(]1[)] the \n", "\n(1) the "),
                 ("See the \n", "See the "), ("these termsservice", "these terms\nservice"),
                 ("\nsection", " section"), ("See the \n", "See the "),
                 ("\nPurpose section below", "Purpose section below"),
                 ("Feedback is covered in the \n", "Feedback is covered in the "),
                 ("\nremains yours,", " remains yours,")]
        else:
            number1.remove("3")
            number2 = [str(numm) for numm in range(5, 12)]
            c = []
            for numm in number2:
                c = c + selector.xpath(
                    '//*[@id="yDmH0d"]/c-wiz/div/div[2]/div[2]/div[3]/c-wiz/div[' + numm + ']/div/ul/li/a//text()')
            infos = selector.xpath('//*[@id="yDmH0d"]/c-wiz/div/div[2]/div[2]/div[3]/c-wiz/div[1]/div//text()')
            for n in number1:
                infos = infos + selector.xpath(
                    '//*[@id="yDmH0d"]/c-wiz/div/div[2]/div[2]/div[3]/c-wiz/div[{}]/div//text()'.format(n))
            a = selector.xpath('//p/a//text()') + c
            while "Delete your information" in a:
                a.remove("Delete your information")
            while "Export your data" in a:
                a.remove("Export your data")
            while "Go to Google Account" in a:
                a.remove("Go to Google Account")
            b = [('\n' + A + '\n ', A + ' ') for A in a] + \
                [('\n' + A + '\n,', A + ',') for A in a] + \
                [('\n' + A + '\n\.', A + '.') for A in a] + \
                [('\n' + A + '\n:', A + ':') for A in a] + \
                [('\n' + A + '\n', A + ' ') for A in a] + \
                [('\n' + A, A) for A in a]
        content = '\n'.join(infos).strip()
        # cleaning #
        content = cleaning(content)
        content = recleaning(b, content)
        content = cleaning(content)
        if i[0] == 'terms':
            content = recleaning(e, content)
        print(content)
        #  saving  #
        df = pd.DataFrame(data=[[name, date, content, i[1]]], columns=['platform', 'date', 'content', 'url'])
        df.to_csv(path + name + "_" + i[0] + '_' + lan(content[0]) + "_" + date + ".csv", index=False)

    #############
    # community #
    #print("-----" + termsname[2][0] + "-----")
    res = requests.get(termsname[2][1], headers=headers)
    selector = etree.HTML(res.text)
    suburl = selector.xpath('//div/a//@href')
    subtext = selector.xpath('//div/a//text()')
    subtext = subtext[3:subtext.index('View all chapters')]
    #print(subtext)
    suburl = suburl[2:-3]
    suburll = ['https://socratic.org' + url for url in suburl]
    suburlname = list(zip(subtext, suburll))
    contentlist = []
    namelist = []
    datelist = []
    for url in suburlname:
        #print(url)
        ress = requests.get(url[1], headers=headers)
        selector = etree.HTML(ress.text)
        infos = selector.xpath('//div[@class="answerText"]//text()')
        a = selector.xpath('//p/em//text()|//p/strong//text()|//a//text()')
        b = [('\n' + aa + '\n', aa + ' ') for aa in a] + [("The less obvious: ", "\nThe less obvious:\n")] + \
            [("The obvious: ", "\nThe obvious:\n")] + [("kindSpamming", "kind\nSpamming")] + \
            [("basicsExplanation:", "basics\nExplanation:")] + [("\nwriting answers", "writing answers")] + \
            [("\ncommunity guidelines, but it does", "community guidelines, but it does")] + \
            [('"Googling"', '\n"Googling"')] + \
            [("https://creativecommons\.org/licenses/by[-]nc[-]sa/4\.0/ ",
              "\nhttps://creativecommons.org/licenses/by-nc-sa/4.0/\n")] + \
            [("https://socratic\.org/answering[-]basics ", "\nhttps://socratic.org/answering-basics\n")]
        content = ''.join(infos).strip()
        # cleaning #
        content = cleaning(content)
        content = recleaning(b, content)
        contentlist.append(content)
        namelist.append(name + '_' + url[0])
        datelist.append(date)
    #  saving  #
    df = pd.DataFrame(data=[[namelist, datelist, contentlist, suburll]], columns=['platform', 'date', 'content', 'url'])
    df.to_csv(path + name + "_" + termsname[2][0] + '_' + lan(contentlist[0][0]) + "_" + date + ".csv", index=False)


#the codes for scraping Siri
def Siri():
    ###########
    name = "Siri"
    path = 'Data_DayByDay/' + name + '/'
    if not os.path.exists(path):
        os.makedirs(path)
    date = datetime.date.today().strftime('%Y%m%d')
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 '
                      'Safari/537.36'
    }
    user_agent = headers['User-Agent']

    ###########
    url = 'https://www.apple.com/legal/privacy/data/en/ask-siri-dictation/'
    res = requests.get(url, headers=headers)
    selector = etree.HTML(res.text)
    infos = selector.xpath(
        '//*[@id="beforepresent"]/dl/section/div/div/dd/h2//text()|//*[@id="beforepresent"]/dl/section/div/div/div/div/dd/div//text()|//*[@id="beforepresent"]/dl/section/div/div/div/div/dd/p[2]/text()|//*[@id="beforepresent"]/dl//text()')
    a = selector.xpath('//p/a//text()')
    language = selector.xpath('/html/body/main/section/div/div/div[2]/span[1]//text()')
    del infos[infos.index('Apple Footer') - 1:-1]
    #print(a)
    #print(infos)
    content = '\n'.join(infos).strip()
    # cleaning #
    p = re.compile(r'[^\x00-\x7f]')
    content = re.sub(p, '', content)
    clean_format = (("\n +", "\n"), (" +", " "), ('\n+', '\n'), ('\n' + a[0] + '\n', a[0]), ('\n' + a[1] + '\n', a[1]))
    for element in clean_format:
        content = re.sub(element[0], element[1], content)
    print(content)

    ###########
    df = pd.DataFrame(data=[[name, date, content, url]], columns=['platform', 'date', 'content', 'url'])
    df.to_csv(path + name + "_" + 'privacy' + '_' + language[0] + '_' + date + ".csv", index=False)


#the codes for scraping Mewe
def Mewe():
    name = "Mewe"
    path = 'Data_DayByDay/' + name + '/'
    if not os.path.exists(path):
        os.makedirs(path)
    date = datetime.date.today().strftime("%Y%m%d")
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 '
                      'Safari/537.36'
    }
    id = ["terms", "privacy"]
    for i in id:
        url = 'https://api-us.storyblok.com/v2/cdn/stories/cms/' + i +'?version=draft&language=zh-HK&token=WvpMvnI0MDS4VQc3ag1jfgtt&cv=undefined'
        response = requests.get(url, headers = headers)
        resstr = str(response.json())
        matchlist = re.findall("text': ('|\")(.*?)(',|\",)", resstr)
        content = ''
        for item in matchlist:
            content = content + item[1] + '\n'
        pattern = [('\\xa0', ''),('\n ', ' '),('\n: ', ': '),('\n, ', ', '),('\n"','"'),('"\n','"'),('\n.\n','.\n'),
                  ('\nprivacy@mewe.com.','privacy@mewe.com.'),
                  ('\nhttps','https'),
                  ('\ncopyright@mewe.com\n','copyright@mewe.com'),
                  ('\nTerms of Use\n.','Terms of Use.')]
        for p in pattern:
            content = content.replace(p[0],p[1])
        print(content)
        df = pd.DataFrame(data=[[name, date, content, url]],
                          columns=['platform', 'date', 'content', 'url'])
        df.to_csv(path + name + "_" + i + "_" + date + ".csv", index=False)

#the codes for scraping Kuaishou_en
def Kuaishou_en():
    def recleaning(patterns, stringdata):
        for pattern in patterns:
            stringdata = re.sub(pattern[0], pattern[1], stringdata)
        return stringdata

    def cleaning(stringdata):
        clean_format = [
            ("\xa0", ""),
            (r"\\n", ""), (" +", " "),
            ("\n \n", "\n"), ("\n ", "\n"), (" \n", "\n"),
            ("{}+".format("\n"), "\n"),
            ("\n,\n", ","), ("\n,", ","),
            ("\n”\n", "”"), ("\n”", "”"), ("”\n", "”"),
            ("\n“\n", "“"), ("\n“", "“"), ("“\n", "“"),
            ('\n"\n', '" '), ('\n"', '" '), ('"\n', '" '),
            ('\n:\n', '" '), ('\n:', '" '),
            ("\n\.\n", "."), ("\n\.", "."),
            ("\n;\n", "; "),
            ("[)]\n", ") ")]
        for number in range(0, 10):
            number = str(number)
            clean_format.append((number + '\.' + '\n', number + '.'))
            clean_format.append((number + '\n', number + ' '))
        for element in clean_format:
            stringdata = re.sub(element[0], element[1], stringdata)
        return stringdata
    name = "Kuaishou_en"
    path = 'Data_DayByDay/' + name + '/'
    if not os.path.exists(path):
        os.makedirs(path)
    date = datetime.date.today().strftime('%Y%m%d')
    # terms + privacy + community #
    filename = ["terms", "privacy", "community"]
    urlist = ["https://www.kwai.com/rest/kibtWwwNode/getTermsService",
              "https://ppg.m.kwai-pro.com/block/n/activity/page/drBgGzPP?hyId=doodle_drBgGzPP&webview=yoda&share_item_type=jimu_drBgGzPP",
              "https://ppg.m.kwai-pro.com/block/n/activity/page/ktCMzneF?hyId=doodle_ktCMzneF&webview=yoda&share_item_type=jimu_ktCMzneF"]
    termname = list(zip(filename, urlist))
    for i in termname:
        #print("{:=^50s}".format(i[0]))
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument(f'user-agent={user_agent}')
        options.add_experimental_option("detach", True)
        # options.add_argument(f'cookie={cookie}')
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
        driver.get(i[1])
        res = driver.page_source
        if i[0] == "terms":
            selector = etree.HTML(etree.HTML(res).xpath("/html/body/pre//text()")[0])
            infos = selector.xpath('//*[@class="protocol-box"]//text()')
        elif i[0] == "privacy":
            selector = etree.HTML(res)
            infos = selector.xpath('//*[@id="E8a9bc69b"]/div//text()')
        else:
            selector = etree.HTML(res)
            infos = selector.xpath('//*[@id="Ee1b69f50"]/div//text()')
        content = '\n'.join(infos).strip()
        #  cleaning  #
        if i[0] == "terms":
            content = content.split("Termos de Serviço", 1)[0]
        else:pass
        content = cleaning(content)
        print(content)
        #  saving  #
        df = pd.DataFrame(data=[[name, date, content, i[1]]], columns=['platform', 'date', 'content', 'url'])
        df.to_csv(path + name + "_" + i[0] + "_" + date + ".csv", index=False)
        driver.close()


#the codes for scraping Kuaishou_zh
"""def Kuaishou_zh():
    name = "Kuaishou_zh"
    path = 'Data_DayByDay/' + name + '/'
    if not os.path.exists(path):
        os.makedirs(path)
    date = datetime.date.today().strftime('%Y%m%d')
    #terms + privacy
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 '
                      'Safari/537.36',
        'Accept': 'application/json',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-CN;q=0.6',
        'Connection': 'keep-alive',
        'Content-Length': '23',
        'Content-Type': 'application/json;charset=UTF-8',
        'Cookie': 'did=web_ff71778fd959e07dc25340304f9f588d; didv=1684999088808',
        'Host': 'app.m.kuaishou.com',
        'Origin': 'https://app.m.kuaishou.com',
        'Referer': 'https://app.m.kuaishou.com/public/index.html'
    }
    id = ['terms','privacy']
    for i in id:
        if i == 'terms':
            d = json.dumps({"id": "14", "draft": "false"})
        else:
            d = json.dumps({"id": "1269", "draft": "false"})
            headers['Content-Length'] = '25'
        url = 'https://app.m.kuaishou.com/rest/w/cms/detail'
        res = json.loads(requests.post(url, data=d, headers=headers).text)
        selector = etree.HTML(res['detail']['content'])
        infos = selector.xpath('//*//text()')
        content = '\n'.join(infos).strip()
        pattern = list(
            zip(['\n' + word + '\n' for word in selector.xpath('//a//text()')], selector.xpath('//a//text()'))) \
                  + [('\n \n', '\n'), ('\n，', '，'), ('\n。', '。'), ('\n《', '《'), ('\n》', '》'), ('\n（', '（'),
                     ('\n）', '）'),
                     ('\n：', '：'), ('\n、\n', '、'), ('\n、', '、'), ('.\n', '. '), ("\n向\n", "向",),
                     ('\nGPS信息', 'GPS信息'), ('\n通讯录', '通讯录'), ('\n人脸', '人脸'), ('\n权益', '权益'),
                     ('\n及', '及'), ('\n等', '等'),
                     ('\n电话', '电话'), ('\n相机', '相机'), ('\n相册', '相册'), ('\n指纹', '指纹'), ('\n真实', '真实'),
                     ('\n密码', '密码'), ('\n以', '以'),
                     ('\n麦克风', '麦克风'), ('\n地理', '地理'), ('\n第三方支付账号信息\n', '第三方支付账号信息'),
                     ('\n银行', '银行'), ('\n账户', '账户'),
                     ('\n订单', '订单'), ('\n充值', '充值'), ('\n日历', '日历'), ('\n剪切板', '剪切板'),
                     ('\n精准', '精准'), ('\n位置', '位置'),
                     ('\n的', '的'), ('（一', '\n（一'), ('（二', '\n（二'), ('（三', '\n（三'), ('（四', '\n（四'),
                     ('（五', '\n（五'), ('（六', '\n（六')] + \
                  list(zip([n + '\n' for n in [str(number) for number in range(1, 10)]],
                           [str(number) + ' ' for number in range(1, 10)]))
        for p in pattern:
            content = content.replace(p[0], p[1])
        print(content)
        df = pd.DataFrame(data=[[name, date, content, url]], columns=['platform', 'date', 'content', 'url'])
        df.to_csv(path + name + "_" + i + "_" + date + ".csv", index=False, encoding="utf_8_sig")

    #community guidelines
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 '
                      'Safari/537.36'}
    termname1 = ['community', 'live', 'userInfo', 'comment', 'liveCover']
    com_content = str()
    com_url = str()
    for i in termname1:
        url = 'https://www.kuaishou.com/norm?tab=' + i
        res = requests.get(url, headers=headers)
        res.encoding = 'utf-8'
        selector = etree.HTML(res.text)
        infos = selector.xpath('//*[@id="body-wrap"]/div[2]/div/div/div/div//text()')
        content = '\n'.join(infos).strip()
        content = content.replace('\n ','')
        com_content = com_content + content + '\n'
        com_url = com_url + url + '\n'
    print(com_content)
    df = pd.DataFrame(data=[[name, date, com_content, com_url]], columns=['platform', 'date', 'content', 'url'])
    df.to_csv(path + name + '_' + 'community guidelines' + '_' + date + '.csv', index=False, encoding="utf_8_sig")
"""

#the codes for scraping Linkdin
def Linkdin():
    name = "Linkedin"
    path = 'Data_DayByDay/' + name + '/'
    if not os.path.exists(path):
        os.makedirs(path)
    date = datetime.date.today().strftime("%Y%m%d")
    # terms + privacy + community #
    filename = ["terms", "privacy", "community"]
    urlparameter = ["user-agreement", "privacy-policy", "professional-community-policies"]
    termname = list(zip(filename, urlparameter))
    for i in termname:
        url = "https://www.linkedin.com/legal/" + i[1]
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument(f'user-agent={user_agent}')
        options.add_experimental_option("detach", True)
        # options.add_argument(f'cookie={cookie}')
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
        driver.get(url)
        res = driver.page_source
        selector = etree.HTML(res)
        infos = selector.xpath('//*[@id="component-container"]//text()')
        content = '\n'.join(infos).replace("\n ","").replace("     ","").replace("\n\n","").replace("\n   ","").replace("\n  ","").replace("\n.",".").replace("\n,",",").replace("\n "," ").replace("\n;",";").strip()
        print(content)
        #  saving  #
        df = pd.DataFrame(data=[[name, date, content, url]], columns=['platform', 'date', 'content', 'url'])
        df.to_csv(path + name + '_' + i[0] + '_' + date + ".csv", index=False)
        driver.close()

def Flickr():
    name = "Flickr"
    date = datetime.date.today().strftime('%Y%m%d')
    path = 'Data_DayByDay/' + name + '/'
    if not os.path.exists(path):
        os.makedirs(path)
    id = ["terms", "privacy", "community"]
    for i in id:
        if i == "community":
            import pdfplumber
            url = 'https://combo.staticflickr.com/ap/build/pdfs/help/en-us/guidelines.pdf'
            response = requests.get(url, headers=headers_2)
            bytes_io = io.BytesIO(response.content)
            pdf_name = name + '_' + i
            with open(path + "%s.PDF" % pdf_name, mode='wb') as f:
                f.write(bytes_io.getvalue())
            with pdfplumber.open(path + "%s.PDF" % pdf_name) as pdf:
                content = ''
                for page in pdf.pages:
                    content = content + page.extract_text() + '\n'
            pattern = [
                ('\n', ''),
                ('Every day, the global Flickr community,', '\nEvery day, the global Flickr community,'),
                ('These community guidelines are meant', '\nThese community guidelines are meant'),
                ('Thank you for being here', '\nThank you for being here'), ('●', '\n●')]
        else:
            url = "https://www.flickr.com/help/" + i
            options = webdriver.ChromeOptions()
            options.add_argument("--headless")
            options.add_argument(f'user-agent={user_agent}')
            options.add_experimental_option("detach", True)
            driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
            driver.get(url)
            driver.implicitly_wait(5)
            # test = driver.find_elements(By.CLASS_NAME, "nav-link")
            res = driver.page_source
            selector = etree.HTML(res)
            infos = selector.xpath('//h1//text()|//h2//text()|//p//text()|ol//text()')
            a = selector.xpath('//p/a/text()')
            content = '\n'.join(infos).strip()
            pattern = list(zip(['\n' + aa + '\n' for aa in a], [aa for aa in a])) + \
                      [("\t", ""), ("\n+", "\n"), ("\n: ", ": "), (":\n ", ": ")]
            driver.close()
        for p in pattern:
            content = re.sub(p[0], p[1], content)
        print(content)
        df = pd.DataFrame(data=[[name, date, content, url]], columns=['platform', 'date', 'content', 'url'])
        df.to_csv(path + name + "_" + i + "_" + date + ".csv", index=False)
        driver.close()


def Facebook():
        headers_2 = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36',
            'Accept-Language': 'en'}
        name = "Facebook"
        path = 'Data_DayByDay/' + name + '/'
        if not os.path.exists(path):
            os.makedirs(path)
        date = datetime.date.today().strftime("%Y%m%d")
        id = [("terms","https://www.facebook.com/legal/terms/plain_text_terms"),
              ("privacy","https://mbasic.facebook.com/privacy/policy/printable/#"),
              ("community","https://transparency.fb.com/en-gb/policies/community-standards/")]
        for i in id:
            # terms
            if i[0] == "terms":
                options = webdriver.ChromeOptions()
                options.add_argument("--headless")
                options.add_argument(f'user-agent={headers_2["User-Agent"]}')
                options.add_experimental_option("detach", True)
                options.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})
                options.add_argument("Accept-Language=en")
                #options.add_argument("--lang=en_US")
                driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
                driver.get(i[1])
                res = driver.page_source
                selector = etree.HTML(res)
                infos = selector.xpath('//a/text()|//i/text()|//div/text()|//br/text()|//li/text()|//h2/text()|//h3/text()'
                                           '|//h1/text()|//u/text()|//b/text()|//span/text()')
                content = '\n'.join(infos)
                clean_format = [("\xa0",""),("·",""),(" +", " "),("\t","\n"),("\n +", "\n"),("\n+", "\n")]
                for element in clean_format:
                    content = re.sub(element[0], element[1], content)
                content = content.replace('\n', '* ')
                print(content)
                driver.close()
            #privacy
            if i[0] == "privacy":
                res = requests.get(i[1], headers=headers_2)
                res_text = res.text
                selector = etree.HTML(res_text.encode('utf-8'))
                infos_2 = selector.xpath('//div[@class="t"]//text()')
                content = '* '.join(infos_2).strip()  # seperated by "*+space" for future dividing
                print(content)
            #community
            if i[0] == "community":
                res = requests.get(i[1], headers=headers_2)
                res_text = res.text
                selector = etree.HTML(res_text.encode('utf-8'))
                infos = selector.xpath('//*[@class="_9nu3"]//text()')
                href = selector.xpath('//a//@href')
                href_a = href[href.index("/en-gb/policies/community-standards/violence-incitement/"):href.index("/en-gb/policies/community-standards/additional-protection-minors/") + 1]
                href = ["https://transparency.fb.com" + sublink for sublink in href_a]
                content = '\n'.join(infos).strip()
                for link in href:
                    res_sub = requests.get(link, headers=headers_2)
                    res_sub_text = res_sub.text
                    selector = etree.HTML(res_sub_text.encode('utf-8'))
                    subinfos = selector.xpath('//*[@class="_9nu3"]//text()')
                    try:
                        subinfos = subinfos[subinfos.index('Policy rationale'):(len(subinfos) - subinfos[::-1].index('User experiences'))]
                    except:
                        subinfos = subinfos[subinfos.index('Current version'):(len(subinfos) - subinfos[::-1].index('Read more'))]
                    subcontent = '\n'.join(subinfos).strip()
                    content = content + '\n*\n' + href_a[href.index(link)].split("/")[-2] + '\n' + subcontent
                    clean_format = [("\n +", "\n"), ("\n:", ":"), ("\n\.", "."), ("\n,", ","), ("\n\(", "("),
                                    ("\n\)", ")"), ("\n，", "，"), (" +", " "), ("\n+", "\n")]
                    for element in clean_format:
                        content = re.sub(element[0], element[1], content)
                print(content)
            df = pd.DataFrame(data=[[name, date, content, i[1]]], columns=['platform', 'date', 'content', 'url'])
            df.to_csv(path + name + "_" + i[0] + "_" + date + ".csv", index=False)



#Instagram
def Instagram():
        name = "Instagram"
        path = 'Data_DayByDay/' + name + '/'
        if not os.path.exists(path):
            os.makedirs(path)
        date = datetime.date.today().strftime("%Y%m%d")
        filename = ["terms", "community"]
        urlparameter = ["https://help.instagram.com/581066165581870/?helpref=hc_fnav",
                        "https://help.instagram.com/477434105621119/?helpref=hc_fnav"]
        termname = list(zip(filename, urlparameter))
        for i in termname:
            url = i[1]
            options = webdriver.ChromeOptions()
            options.add_argument("--headless")
            options.add_argument(f'user-agent={user_agent}')
            options.add_experimental_option("detach", True)
            driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
            driver.get(url)
            res = driver.page_source
            selector = etree.HTML(res)
            infos = selector.xpath('//i/text()|//a/text()|//span/text()|//b/text()|//p/text()|//h1/text()|//div/text()|//h2/text()')
            try:
                infos = infos[infos.index('Instagram Purchase Protection Policy')+2:]
            except: pass
            infos = [i.strip() for i in infos]
            content = '\n'.join(infos).strip()
            content = content.replace("\n"," ")
            print(content)
            df = pd.DataFrame(data=[[name, date, content, url]], columns=['platform','date', 'content', 'url'])
            df.to_csv(path + name + "_" + i[0] + "_" + date + ".csv", index=False)
            driver.close()



'''this function All_platforms() is for scraping all the platforms at once.
If we choose "all" in the APP, it will call this function, to run a loop and obtain data for each platforms one by one.'''

def All_platforms():
    p_list = {'Douyin': Douyin, 'TikTok': TikTok, 'Line Taxi': LineTaxi, 'Find Taxi (呼叫小黃)': FindTaxi,
              'Meituan (美團)': Meituan, 'Foodpanda': Foodpanda, 'Lalamove': Lalamove, 'GoGOVan (GoGoX)': GoGoVan,
              'Signal': Signal, 'Telegram': Telegram, 'LINE': LINE, 'WhatsApp': WhatsApp, 'Xiaohongshu (小红书)': Xiaohongshu,
              'Vine': Vine, 'Tumblr': Tumblr, 'Pinterest': Pinterest, 'WeChat': WeChat, 'Weixin': Weixin,
              'Snapchat':Snapchat, 'Tencent': Tencent, 'Twitter': Twitter, 'Uber': Uber,
              'OpenAI': OpenAI, 'Character.AI': CharacterAI, 'Jasper': Jasper,
              'BlenderBot': BlenderBot, 'Writesonic': Writesonic, 'Replika': Replika, 'ELSA': ELSA,
              'Alexa': Alexa, 'Cortana': Cortana, 'Mycroft': Mycroft,
              'Google Assistant': Google_Assistant, 'Reddit': Reddit, 'Twitch': Twitch, 'Snapask':Snapask,
              'Upwork':Upwork, 'Meetup': Meetup, 'DiDi': DiDi, 'Discord': Discord, 'Socratic': Socratic, 'Siri': Siri,
              'Mewe':Mewe, 'Kuaishou_en': Kuaishou_en,
              'Linkdin': Linkdin, 'Flickr': Flickr, 'Facebook': Facebook, 'Instagram': Instagram}




    loop_obj3 = tqdm(p_list)
    for i in loop_obj3:
        loop_obj3.set_description(f"Scraping→ {i}")
        p_list[i]()


def count_ch_str(content):
    count = 0
    for s in content:
        if '\u4e00' <= s <= '\u9fff':
            count += 1
    return count / len(content)

'''
[Part 2]
Codes for comparing policies

This function is defined for comparing the different versions of policies.
The current version:
It will loop to compare all the platforms' policies in Data_DayByDay, the steps:
step 1: for each platform subfolder → combine all the csv files we collected every day.
step 2: use "drop_duplicates()" (pandas package) based on column "content". This will drop all the csv files with completely same content (cannot be a new policy).
step 3: For the rest csv files, they may not be the policies with really different content. Some websites my only changed several punctuations.
To find the real changes, we can use "difflib.HtmlDiff()" (difflib package) to general some html files for mannual review. 
Each html file will compare two polices and hightlighted the differences in different colors. 
'''
def All_compare():
    # 定义文件夹路径
    folder_path = "Data_DayByDay"

    # 获取文件夹及其子文件夹下的所有CSV文件路径
    csv_files = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".csv"):
                csv_files.append(os.path.join(root, file))

    # 根据文件名进行分组
    grouped_files = {}
    for file_path in csv_files:
        file_name = os.path.basename(file_path)
        name_parts = file_name.split("_")
        name = "_".join(name_parts[:-1])  # 去掉日期部分
        if name not in grouped_files:
            grouped_files[name] = []
        grouped_files[name].append(file_path)

    # 合并文件名相同的CSV文件
    loop_obj=tqdm(grouped_files.items())
    for name, files in loop_obj:
        loop_obj.set_description(f"Combining→ {name}")
        #print(name)
        merged_data = pd.concat([pd.read_csv(file) for file in files])
        merged_data = merged_data.dropna(subset=["content"])
        merged_data = merged_data.drop_duplicates(subset=["content"])
        # 根据原始文件的名称模式创建输出文件名
        output_file = name + ".csv"

        # 输出到新的CSV文件
        output_path = 'Data_DayByDay_combine/'
        os.makedirs(output_path, exist_ok=True)
        merged_data.to_csv(output_path + output_file, index=False)

    path_data = "Data_DayByDay_combine/"
    loop_obj2 = tqdm(sorted(os.listdir(path_data)))
    for n in loop_obj2:
        loop_obj2.set_description(f"Comparing→ {n}")
        data = pd.read_csv(path_data + n)
        name = n.split(".")[0]


        for i in range(0, len(data) - 1):
            path_new = 'Data_ComparePolicies/' + name + '/'  # create the folder/path for saving data
            if not os.path.exists(path_new):
                os.makedirs(path_new)

            ch_percent1 = count_ch_str(data["content"][i])
            ch_percent2 = count_ch_str(data["content"][i + 1])
            #print(ch_percent1, ch_percent2)

            if ch_percent1 < 0.7 and ch_percent2 < 0.7:
                text1 = sent_tokenize(data["content"][i])
                text2 = sent_tokenize(data["content"][i + 1])
                text1 = list(filter(None, text1))
                text2 = list(filter(None, text2))
                d = difflib.HtmlDiff(wrapcolumn=65)
                html = d.make_file(text1, text2)
                Html_file = open(path_new + name + "_En_" + str(i) + " vs " + str(i + 1) + "_" + str(
                    data['date'][i]) + "_" + str(data['date'][i + 1]) + ".html", "w", encoding="utf-8")
                Html_file.write(html)
                Html_file.close()

            if ch_percent1 >= 0.7 and ch_percent2 >= 0.7:
                text1 = re.split("。|！|；", data["content"][i])
                text2 = re.split("。|！|；", data["content"][i + 1])
                text1 = list(filter(None, text1))
                text2 = list(filter(None, text2))
                d = difflib.HtmlDiff(wrapcolumn=65)
                html = d.make_file(text1, text2)
                Html_file = open(path_new + name + "_Ch_" + str(i) + " vs " + str(i + 1) + "_" + str(
                    data['date'][i]) + "_" + str(data['date'][i + 1]) + ".html", "w", encoding="utf-8")

                Html_file.write(html)
                Html_file.close()

            else:
                continue



'''
[Part 3]
Codes for WaybackScraper interface

In this part, we built the interface based on the package named "customtkinter" (https://github.com/TomSchimansky/CustomTkinter).
This package provide a framework to build app with modern look.
We can set buttons/widgets/frames on the app, and we could link our codes (e.g., codes for scraping/comparing) to certain buttons.
Finally, we can just click the buttons to run the codes instead of opening python project+running codes in pycharm.
'''

# interface design: set the color and themes for the app.
customtkinter.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


'''
We defined a class to put all the codes for creating te app together.
E.g., the codes for displaying button, or the codes for link the button with our scraping/comparing codes.
'''

class App(customtkinter.CTk):
    # the codes for the first button (left) "Scraping!". This button is used for scraping historical data, which is under development.
    def button_callback_left(self):
        self.my_string_var_left.set(
            "Platform → " + self.combobox_1.get() + "\n" + "Start date → " + self.cal1.get_date()
            + "\n" + "End date → " + self.cal2.get_date())
        self.Platforms_list[self.combobox_1.get()]()

    # the codes for the second button (middle) "Scraping". This button is used for scraping data day by day.
    def button_callback_right(self):
        self.progressbar.start()
        self.label_platform_scraping_start.configure(text="downloading, please wait...")
        self.label_platform_scraping_start.pack(pady=1, padx=1)
        self.my_string_var_right.set("Platform → " + self.combobox_3.get() + "\n" + "Date → "
                                     + datetime.date.today().strftime('%Y%m%d'))
        self.Platforms_list[self.combobox_3.get()]()
        self.progressbar.set(1)
        self.progressbar.stop()
        self.label_platform_scraping_start.configure(text="Finished!")

    # the codes for the third button (right) "Comparing". This button is used for comparing policies to find different versions.
    def button_callback_compare(self):
        self.progressbar2.start()
        self.label_platform_scraping_start2.configure(text="comparing, please wait...")
        self.label_platform_scraping_start2.pack(pady=1, padx=1)
        self.my_string_var_right2.set("Platform → " + self.combobox_4.get())
        self.Platforms_list[self.combobox_4.get()]()
        self.progressbar2.set(1)
        self.progressbar2.stop()
        self.label_platform_scraping_start2.configure(text="Finished!")

    #the codes for set the list in the choice frames. (e.g., Douyin, TikTok...All)
    def __init__(self):
        super().__init__()
        self.Platforms_list = {'Douyin': Douyin, 'TikTok': TikTok, 'Line Taxi': LineTaxi, 'Find Taxi (呼叫小黃)': FindTaxi,
              'Meituan (美團)': Meituan, 'Foodpanda': Foodpanda, 'Lalamove': Lalamove, 'GoGOVan (GoGoX)': GoGoVan,
              'Signal': Signal, 'Telegram': Telegram, 'LINE': LINE, 'WhatsApp': WhatsApp, 'Xiaohongshu (小红书)': Xiaohongshu,
              'Vine': Vine, 'Tumblr': Tumblr, 'Pinterest': Pinterest, 'WeChat': WeChat, 'Weixin': Weixin,
              'Snapchat':Snapchat, 'Tencent': Tencent, 'Twitter': Twitter, 'Uber': Uber,
              'OpenAI': OpenAI, 'Character.AI': CharacterAI, 'Jasper': Jasper,
              'BlenderBot': BlenderBot, 'Writesonic': Writesonic, 'Replika': Replika, 'ELSA': ELSA,
              'Alexa': Alexa, 'Cortana': Cortana, 'Mycroft': Mycroft,
              'Google Assistant': Google_Assistant, 'Reddit': Reddit, 'Twitch': Twitch, 'Snapask':Snapask,
              'Upwork':Upwork, 'Meetup': Meetup, 'DiDi': DiDi, 'Discord': Discord, 'Socratic': Socratic, 'Siri': Siri,
              'Mewe':Mewe, 'Kuaishou_en': Kuaishou_en,
              'Linkdin': Linkdin, 'Flickr': Flickr, 'Facebook': Facebook, 'Instagram': Instagram, 'All': All_platforms,'All_compare': All_compare}

        self.my_string_var_left = StringVar()
        self.my_string_var_right = StringVar()
        self.my_string_var_right2 = StringVar()

        #set the size & name of the app
        self.geometry("800x720")
        self.title("PolicyTimeMachine")

        # create 2x3 grid system (the structure of the app)
        self.grid_rowconfigure(3, weight=1)
        self.grid_columnconfigure((0, 2), weight=1)

        self.frame_1 = customtkinter.CTkFrame(master=self)
        self.frame_1.grid(row=0, column=0, columnspan=1, padx=20, pady=20, sticky="nsew")

        self.frame_2 = customtkinter.CTkFrame(master=self)
        self.frame_2.grid(row=1, column=0, columnspan=1, padx=20, pady=20, sticky="nsew")

        self.frame_3 = customtkinter.CTkFrame(master=self)
        self.frame_3.grid(row=0, column=1, columnspan=1, padx=20, pady=20, sticky="nsew")

        self.frame_4 = customtkinter.CTkFrame(master=self)
        self.frame_4.grid(row=1, column=1, columnspan=1, padx=20, pady=20, sticky="nsew")

        self.frame_5 = customtkinter.CTkFrame(master=self)
        self.frame_5.grid(row=0, column=2, columnspan=1, padx=20, pady=20, sticky="nsew")

        self.frame_6 = customtkinter.CTkFrame(master=self)
        self.frame_6.grid(row=1, column=2, columnspan=1, padx=20, pady=20, sticky="nsew")


        # frame_1: the frame on the left (historical data): set its title, positions and so on.
        self.left_title = customtkinter.CTkLabel(master=self.frame_1, justify=customtkinter.LEFT,
                                                 text="historical data",
                                                 text_color="white", font=customtkinter.CTkFont(size=18, weight="bold"))
        self.left_title.pack(pady=10, padx=10)

        # select platform
        self.label_platform = customtkinter.CTkLabel(master=self.frame_1, justify=customtkinter.LEFT,
                                                     text="Select platforms: ",
                                                     font=customtkinter.CTkFont(size=12, weight="bold"))
        self.label_platform.pack(pady=1, padx=1)
        platform_values=["Douyin", "TikTok", "Line Taxi",
                          "Find Taxi (呼叫小黃)", "Meituan (美團)",
                          "Foodpanda", "Lalamove",
                          "GoGOVan (GoGoX)", "Signal", "Telegram",
                          "LINE", "WhatsApp", "Xiaohongshu (小红书)",
                          "Vine", "Tumblr", "Pinterest", "WeChat",
                          "Weixin", "Snapchat", "Tencent", "Twitter",
                          "Uber", "OpenAI", "Character.AI",
                          "Jasper", "BlenderBot", "Writesonic",
                          "Replika", "ELSA", "Alexa",
                          "Cortana", "Mycroft", "Google Assistant",
                          "Reddit", "Twitch", "Snapask", 'Upwork', "Meetup", "DiDi", "Discord",
                          "Socratic", "Siri", "Mewe", "Kuaishou_en",
                          "Linkdin", "Flickr", "Facebook", "Instagram","All"]

        self.combobox_1 = customtkinter.CTkComboBox(self.frame_1, values=platform_values)
        self.combobox_1.pack(pady=10, padx=10)

        # select sdate
        self.label_sdate = customtkinter.CTkLabel(master=self.frame_1, justify=customtkinter.LEFT, text="Start date: ",
                                                  font=customtkinter.CTkFont(size=12, weight="bold"))
        self.label_sdate.pack(pady=1, padx=1)
        self.cal1 = Calendar(self.frame_1, selectmode='day', locale='en_US', disabledforeground='red',
                             cursor="hand2", background=customtkinter.ThemeManager.theme["CTkFrame"]["fg_color"][1],
                             selectbackground=customtkinter.ThemeManager.theme["CTkButton"]["fg_color"][1])
        self.cal1.pack(fill="both", expand=False, padx=1, pady=1)

        # select edate
        self.label_edate = customtkinter.CTkLabel(master=self.frame_1, justify=customtkinter.LEFT, text="End date: ",
                                                  font=customtkinter.CTkFont(size=12, weight="bold"))
        self.label_edate.pack(pady=1, padx=10)
        self.cal2 = Calendar(self.frame_1, selectmode='day', locale='en_US', disabledforeground='red',
                             cursor="hand2", background=customtkinter.ThemeManager.theme["CTkFrame"]["fg_color"][1],
                             selectbackground=customtkinter.ThemeManager.theme["CTkButton"]["fg_color"][1])
        self.cal2.pack(fill="both", expand=False, padx=1, pady=1)

        # scraping button_1
        self.button_1 = customtkinter.CTkButton(master=self.frame_1,
                                                command=lambda: Thread(target=self.button_callback_left,
                                                                       args=[]).start(),
                                                text="Scraping!")
        self.button_1.pack(pady=10, padx=10)

        # frame_2: the collection information for "historical data"
        self.label_result = customtkinter.CTkLabel(master=self.frame_2, justify=customtkinter.LEFT,
                                                   text="↓ Collect infor: ",
                                                   text_color="white",
                                                   font=customtkinter.CTkFont(size=15, weight="bold"))
        self.label_result.pack()

        self.collect_infor = customtkinter.CTkLabel(master=self.frame_2, justify=customtkinter.LEFT,
                                                    textvariable=self.my_string_var_left)
        self.collect_infor.pack()

        # frame_3: the frame on the middle (dya by day): set its title, positions and so on.
        self.right_title = customtkinter.CTkLabel(master=self.frame_3, justify=customtkinter.LEFT,
                                                  text="day by day",
                                                  text_color="white",
                                                  font=customtkinter.CTkFont(size=18, weight="bold"))
        self.right_title.pack(pady=10, padx=10)

        # select platform
        self.label_platform_right = customtkinter.CTkLabel(master=self.frame_3, justify=customtkinter.LEFT,
                                                           text="Select platforms: ",
                                                           font=customtkinter.CTkFont(size=12, weight="bold"))
        self.label_platform_right.pack(pady=1, padx=1)

        self.combobox_3 = customtkinter.CTkComboBox(self.frame_3, values=platform_values)
        self.combobox_3.pack(pady=10, padx=10)

        self.button_2 = customtkinter.CTkButton(master=self.frame_3,
                                                command=lambda: Thread(target=self.button_callback_right,
                                                                       args=[]).start(),
                                                text="Scraping!")
        self.button_2.pack(pady=10, padx=10)

        # scraping related
        self.label_platform_scraping_start = customtkinter.CTkLabel(master=self.frame_3, justify=customtkinter.LEFT,
                                                                    text=" ",
                                                                    font=customtkinter.CTkFont(size=12))

        # frame_4: the collection information for "day by day"
        self.label_result_right = customtkinter.CTkLabel(master=self.frame_4, justify=customtkinter.LEFT,
                                                         text="↓ Collect infor: ",
                                                         text_color="white",
                                                         font=customtkinter.CTkFont(size=15, weight="bold"))
        self.label_result_right.pack()

        self.collect_infor_right = customtkinter.CTkLabel(master=self.frame_4, justify=customtkinter.LEFT,
                                                          textvariable=self.my_string_var_right)
        self.collect_infor_right.pack()

        # self.progress_label = customtkinter.CTkProgressBar(self.frame_3, fg_color="white", width=100, height=10,
        #                                               corner_radius=100)
        # self.progress_label.pack(pady=50, padx=5)
        # displaying a progress bar for day by day
        self.progressbar = customtkinter.CTkProgressBar(master=self.frame_3, mode="indeterminate")
        self.progressbar.pack(pady=50, padx=5)
        self.progressbar.set(0)
        self.progressbar.configure(indeterminate_speed=1)

        # frame_5: the frame on the right (comparing policies): set its title, positions and so on.
        self.right_title2 = customtkinter.CTkLabel(master=self.frame_5, justify=customtkinter.LEFT,
                                                   text="compare policies",
                                                   text_color="white",
                                                   font=customtkinter.CTkFont(size=18, weight="bold"))
        self.right_title2.pack(pady=10, padx=10)

        # select platform
        self.label_platform_right2 = customtkinter.CTkLabel(master=self.frame_5, justify=customtkinter.LEFT,
                                                            text="Select file path: ",
                                                            font=customtkinter.CTkFont(size=12, weight="bold"))
        self.label_platform_right2.pack(pady=1, padx=1)

        self.combobox_4 = customtkinter.CTkComboBox(self.frame_5, values=["All_compare"])
        self.combobox_4.pack(pady=10, padx=10)

        self.button_3 = customtkinter.CTkButton(master=self.frame_5,
                                                command=lambda: Thread(target=self.button_callback_compare,
                                                                       args=[]).start(),
                                                text="Comparing!")
        self.button_3.pack(pady=10, padx=10)

        # comparing related
        self.label_platform_scraping_start2 = customtkinter.CTkLabel(master=self.frame_5, justify=customtkinter.LEFT,
                                                                    text=" ",
                                                                    font=customtkinter.CTkFont(size=12))

        # frame_6: displaying the comparing information
        self.label_result_right = customtkinter.CTkLabel(master=self.frame_6, justify=customtkinter.LEFT,
                                                         text="↓ Compare infor: ",
                                                         text_color="white",
                                                         font=customtkinter.CTkFont(size=15, weight="bold"))
        self.label_result_right.pack()

        self.collect_infor_right2 = customtkinter.CTkLabel(master=self.frame_6, justify=customtkinter.LEFT,
                                                          textvariable=self.my_string_var_right2)
        self.collect_infor_right2.pack()

        # displaying a progress bar for comparing
        self.progressbar2 = customtkinter.CTkProgressBar(master=self.frame_5, mode="indeterminate")
        self.progressbar2.pack(pady=50, padx=5)
        self.progressbar2.set(0)
        self.progressbar2.configure(indeterminate_speed=1)


if __name__ == "__main__":
    app = App()
    app.mainloop()
