import time
import requests
import re
import pandas as pd
from bs4 import BeautifulSoup
from lxml import etree
import os
from threading import Thread
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor


def pageSourceResp(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"
    }
    count = 0
    while count <= 100:
        count += 1
        resp = requests.get(url=url, headers=headers)
        # print(resp.status_code)
        if resp.status_code == int(200):
            break
    resp.encoding = "utf-8"
    return resp.status_code, resp.text


def baioqingbao_downloads(url):
    status_code, pageSource = pageSourceResp(url)
    print(status_code)
    tree = etree.HTML(pageSource)
    link = tree.xpath("//*/img[@class='biaoqingpp']/@src")[0]
    title = tree.xpath("//*/img[@class='biaoqingpp']/@title")[0].split(" - ")[0]

    print(title)
    print(link)
    img_download_save(link, title)


def img_download_save(url, title):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"
    }
    #
    resp = requests.get(url=url, headers=headers)
    imgName = url.split('/')[-1]
    imgContent = resp.content
    file_type = imgName.split('.')[-1]
    fImg = open(f'biaoqingbao/{title}.{file_type}', mode='wb')
    fImg.write(imgContent)
    fImg.close()


def biaoqingbao_tag_downloads(count):
    domain = "https://fabiaoqing.com"
    url = f"https://fabiaoqing.com/tag/index/page/{count}.html"
    status_code, pageSource = pageSourceResp(url)
    # print(status_code)
    if status_code == int(200):
        # print(status_code)
        tree = etree.HTML(pageSource)
        cards = tree.xpath("//*/div[@class='card']/div[@class='content']/a/text()")
        cards_link = tree.xpath("//*/div[@class='card']/div[@class='content']/a/@href")
        cards_link = [f"{domain}{i.split('.')[0]}/page/1.html" for i in cards_link]
        tags_name = tree.xpath("//*/div[@class='ui segment']/a/div/text()")
        tags_link = tree.xpath("//*/div[@class='ui segment']/a/@href")
        tags_link = [f"{domain}{i.split('.')[0]}/page/1.html" for i in tags_link]

        columns = ["tags_name", "tags_link"]
        zippend = zip(tags_name, tags_link)
        df_list = [i for i in zippend]
        df = pd.DataFrame(df_list, columns=columns)
    else:
        df = pd.DataFrame([], columns=columns)
        print(status_code)

    return df


def biaoqingbao_tag_downloads_save(count):
    path = "biaoqingbao/biaoqingbao_tag/"
    df = biaoqingbao_tag_downloads(count)
    page = str(count).rjust(4, '0')
    df_name = f"{path}baioqingbao_tage_page_{page}.csv"
    print(df_name)
    df.to_csv(df_name)


def biaoqingbao_tag_downloads_save_thread():
    with ThreadPoolExecutor(8) as t:
        for i in range(1, 384):
            t.submit(biaoqingbao_tag_downloads_save, i)


def file_list(patch):
    file_lists = []
    for i in os.listdir(patch):
        if os.path.isfile(patch + "/" + i):
            file_lists.append(i)
    return file_lists


def csvfile_merge(path):
    csvFileList = file_list(path)
    frames = []
    for i in csvFileList:
        paths = path + i
        print(paths)
        df = pd.read_csv(paths)
        frames.append(df)
    # columns = ["index", "tags_name", "tags_link"]
    dfs = pd.concat(frames, ignore_index=True, join='inner')
    dfs = dfs.drop(columns='Unnamed: 0')
    dfs.to_csv("biaoqingbao/biaoqingbao_tage_all.csv", encoding="utf_8_sig")


def main():
    # url = "https://fabiaoqing.com/biaoqing/detail/id/57244.html"
    # baioqingbao_downloads(url)
    # biaoqingbao_tag_downloads_save_thread()
    path = "biaoqingbao/biaoqingbao_tag/"
    csvfile_merge(path)


if __name__ == '__main__':
    main()
