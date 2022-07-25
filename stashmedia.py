import time
import requests
import re
import pandas as pd
from time import sleep
from bs4 import BeautifulSoup
from lxml import etree
import os


def stashmedia(url, cont):
    # url = "https://www.stashmedia.tv/"
    # url = "https://www.stashmedia.tv/page/q/"
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
    # div = page.find_all("div", attrs={"class": "homepagecontent"})
    div = tree.xpath("//div[@class='grid-left']/div/div[@class='homepagecontent']")
    title = div[0].xpath("//h2/a/text()")
    pic = div[0].xpath("//a/img/@src")
    link = div[0].xpath("//h2/a/@href")

    zippend = zip(title, pic, link)

    lt = [list(i) for i in zippend]
    col = ["title", "pic", "link"]
    df = pd.DataFrame(lt, columns=col)
    df = df.drop(index=0)
    # print(df)
    print("开始保存")
    df.to_csv(f"page/stashmedia_page_{cont}.csv", encoding="utf_8_sig")
    print(f"已保存页面-{cont}")


def stashmedia_article():
    # url = "https://www.stashmedia.tv/eagle-ottawa-immersion-product-film-by-lunar-north/"
    # headers = {
    #     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"
    # }
    # resp = requests.get(url=url, headers=headers)
    # print("页面加载完毕")
    # resp.encoding = "utf-8"
    # pageSource = resp.text
    f = open('page.html', mode='r', encoding="utf-8")
    pageSource = f.read()
    f.close()

    tree = etree.HTML(pageSource)
    data = tree.xpath("//div[@class='postauthor']/p/text()")
    # result = etree.tostring(div[0])
    # print(result.decode('utf-8'))
    data[0] = data[0].replace('\t', '')
    data = data[0].replace('\n', '')[17:]
    main_text = tree.xpath("//div[@class='grid-left']//p")
    # print(main_text[0])
    # for i in main_text[1:]:
    #     print(etree.tostring(i))
    with open('c.txt', mode='wb+') as f:
        for i in main_text[1:]:
            txt = etree.tostring(i)
            print(txt)
            f.write(txt)














def main():
    print("开始爬取页面")
    for i in range(25):
        cont = i + 1
        url = f"https://www.stashmedia.tv/page/{cont}/"
        print(f"开始页面-{cont}")
        print(f"{url}")
        stashmedia(url, cont)
        time.sleep(1)
    print("完成所有任务")


def file_list(path):
    file_lists = []
    for i in os.listdir(path):
        if os.path.isfile(path + "/" + i):
            file_lists.append(path + "\\" + i)
    return file_lists


def main2():
    path = "D:\DuximpresaProject\PycharmProject\duxspider\page"
    csvlist = file_list(path)
    # print(csvlist)
    # dfs = pd.read_csv(csvlist[0])
    frames = []
    for i in csvlist:
        df = pd.read_csv(i)
        frames.append(df)
    dfs = pd.concat(frames, join='inner', ignore_index=False)
    dfs = dfs.drop(columns="Unnamed: 0")
    dfs.to_csv("stashmedia_page_0.csv")

def main3():
    stashmedia_article()

if __name__ == '__main__':
    main3()
