import time
import requests
import re
import pandas as pd
from time import sleep
from bs4 import BeautifulSoup
from lxml import etree
import os


def colossal_pageUrl(url, cont):
    # url = "https://www.thisiscolossal.com/page/1/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"
    }
    #
    resp = requests.get(url=url, headers=headers)
    print("页面加载完毕")
    resp.encoding = "utf-8"

    # with open("index.html", mode="r", encoding="utf-8") as f:
    #     pageSource = f.read()

    pageSource = resp.text
    # page = BeautifulSoup(pageSource, "html.parser")
    tree = etree.HTML(pageSource)
    url = tree.xpath("//*[@id='posts']/h2/a/@href")
    print(url)
    df = pd.DataFrame(url, columns=["page_url"])
    print(df)
    return df


def colossal_content(url):
    print("任务开始")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"
    }
    #
    resp = requests.get(url=url, headers=headers)
    print("页面加载完毕")
    resp.encoding = "utf-8"
    pageSource = resp.text
    # with open("colossal_content.html", mode="r", encoding="utf-8") as f:
    #     pageSource = f.read()

    tree = etree.HTML(pageSource)
    soup = BeautifulSoup(pageSource, 'html.parser')
    title = tree.xpath("//*[@id='posts']/h2/a/text()")[0]
    author = tree.xpath("//*[@id='posts']/div[@class='post_details singlepost']/h3[@class='author']/a/text()")[0]
    date = tree.xpath("//*[@id='posts']/div[@class='post_details singlepost']/h3[@class='date']/a/text()")[0]
    # category = tree.xpath("//*[@id='posts']/h3[1]/a/text()")
    category = ' '.join(tree.xpath("//*[@id='posts']/h3[1]/a/text()"))
    # tags = tree.xpath("//*[@id='posts']/h3[@class='tags']/a/text()")
    tags = ' '.join(tree.xpath("//*[@id='posts']/h3[@class='tags']/a/text()"))
    content_text_list = tree.xpath("//*[@id='posts']/p//text()")
    # content_text_list = soup.find('main', attrs={'id': 'posts'}).find_all('p')[0].text
    str = ''
    content_text = str.join(content_text_list)
    content_img_list = ' '.join(tree.xpath("//*[@id='posts']/div/img/@src") + tree.xpath("//*[@id='posts']/p/img/@src"))
    # df = pd.DataFrame([url,title,date, author, category, tags, content_text, content_img_list])

    zippend = zip([url], [title], [date], [author], [category], [tags], [content_text], [content_img_list])
    dflist = [i for i in zippend]
    columns = ['url', 'title', 'date', 'author', 'category', 'tags', 'content_text', 'content_img_list']
    df = pd.DataFrame(dflist, columns=columns)
    # print(df.info)
    # df.to_csv('1.csv', encoding="utf_8_sig")
    return df


def colossal_content_tocsv(url):
    print("任务开始")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"
    }
    #
    resp = requests.get(url=url, headers=headers)
    print("页面加载完毕")
    resp.encoding = "utf-8"
    pageSource = resp.text
    # with open("colossal_content.html", mode="r", encoding="utf-8") as f:
    #     pageSource = f.read()

    tree = etree.HTML(pageSource)
    soup = BeautifulSoup(pageSource, 'html.parser')
    title = tree.xpath("//*[@id='posts']/h2/a/text()")[0]
    author = tree.xpath("//*[@id='posts']/div[@class='post_details singlepost']/h3[@class='author']/a/text()")[0]
    date = tree.xpath("//*[@id='posts']/div[@class='post_details singlepost']/h3[@class='date']/a/text()")[0]
    # category = tree.xpath("//*[@id='posts']/h3[1]/a/text()")
    category = ' '.join(tree.xpath("//*[@id='posts']/h3[1]/a/text()"))
    # tags = tree.xpath("//*[@id='posts']/h3[@class='tags']/a/text()")
    tags = ' '.join(tree.xpath("//*[@id='posts']/h3[@class='tags']/a/text()"))
    content_text_list = tree.xpath("//*[@id='posts']/p//text()")
    # content_text_list = soup.find('main', attrs={'id': 'posts'}).find_all('p')[0].text
    str = ''
    content_text = str.join(content_text_list)
    content_img_list = ' '.join(tree.xpath("//*[@id='posts']/div/img/@src") + tree.xpath("//*[@id='posts']/p/img/@src"))
    # df = pd.DataFrame([url,title,date, author, category, tags, content_text, content_img_list])

    zippend = zip([url], [title], [date], [author], [category], [tags], [content_text], [content_img_list])
    dflist = [i for i in zippend]
    columns = ['url', 'title', 'date', 'author', 'category', 'tags', 'content_text', 'content_img_list']
    df = pd.DataFrame(dflist, columns=columns)
    # print(df.info)
    # df.to_csv('1.csv', encoding="utf_8_sig")
    return df


def main():
    frames = []
    for i in range(50):
        cont = i + 1
        url = f"https://www.thisiscolossal.com/page/{cont}/"
        df = colossal_pageUrl(url, cont)
        frames.append(df)
        time.sleep(1)
    dfs = pd.concat(frames, ignore_index=True, )
    dfs.to_csv("colossal_pageUrl.csv", encoding="utf_8_sig")


def colossal_downloads():
    frames = []
    dfpage = pd.read_csv("colossal_pageUrl.csv")
    cont = 0
    for i in dfpage['page_url'][:]:
        cont += 1
        url = i
        df = colossal_content(url)
        frames.append(df)
        print(f"已完成第{cont}个")
        print(i)
        print("-" * 10)
        time.sleep(1)
    dfs = pd.concat(frames, ignore_index=True, join='inner')
    # dfs = dfs.drop(dfs.columns[0])
    dfs.to_csv("colossal_pageContent.csv", encoding="utf_8_sig")
    print('全部完成')


def colossal_downloads_tocsv():
    frames = []
    dfpage = pd.read_csv("colossal_pageUrl.csv")
    # cont = 0
    for i in dfpage.iloc:
        cont = i['Unnamed: 0']
        url = i['page_url']
        df = colossal_content(url)
        # frames.append(df)
        df.to_csv(f"colossal_pageContent/colossal_pageContent_{cont}.csv", encoding="utf_8_sig")
        print(f"已完成第{cont}个")
        print(i)
        print("-" * 10)
        time.sleep(1)
    # dfs = pd.concat(frames, ignore_index=True, join='inner')
    # dfs = dfs.drop(dfs.columns[0])
    # dfs.to_csv("colossal_pageContent.csv", encoding="utf_8_sig")
    print('全部完成')


def colossal_downloads_tocsv222():
    frames = []
    dfpage = pd.read_csv("colossal_pageUrl.csv")
    # print(dfpage.loc[:])
    for i in dfpage.iloc:
        print(i['Unnamed: 0'])


if __name__ == "__main__":
    colossal_downloads_tocsv()
