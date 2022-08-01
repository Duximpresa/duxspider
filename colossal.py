import time
import requests
import re
import pandas as pd
from bs4 import BeautifulSoup
from lxml import etree
import os
from threading import Thread
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor


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
    for i in dfpage[266:].iloc:
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


def colossal_downloads_tocsv_one(dfiloc):
    cont = dfiloc['Unnamed: 0']
    url = dfiloc['page_url']
    df = colossal_content(url)
    # df = pd.DataFrame([cont,url])
    df.to_csv(f"colossal_pageContent/colossal_pageContent_{cont}.csv", encoding="utf_8_sig")
    print(f"已完成第{cont}个")
    print(i)
    print("-" * 10)
    # time.sleep(1)


def colossal_downloads_thread():
    dfpage = pd.read_csv("colossal_pageUrl.csv")
    with ThreadPoolExecutor(32) as t:
        for dfiloc in dfpage.iloc:
            t.submit(colossal_downloads_tocsv_one, dfiloc)
            # time.sleep(1)


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

    dfs = pd.concat(frames, ignore_index=True, join='inner')
    dfs.to_csv("colossal_pageContent.csv", encoding="utf_8_sig")

def img_downloads(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"
    }
    #
    resp = requests.get(url=url, headers=headers)
    imgName = url.split('/')[-1]
    imgContent = resp.content
    return imgContent, imgName

def delete_text(oriText):
    del_Text = '''Do stories and artists like this matter to you? Become a Colossal Member today and support 
    independent arts publishing for as little as $5 per month. You'll connect with a community of like-minded readers 
    who are passionate about contemporary art, read articles and newsletters ad-free, sustain our interview series, 
    get discounts and early access to our limited-edition print releases, and much more. Join now! '''
    text: object = oriText.strip(del_Text)
    return text

def page_downloads(index, row, main_path):
    page_path = main_path + f'colossal_page_{index}'
    title = row['title']
    date = row['date']
    author = row['author']
    category = row['category']
    tags = row['tags']
    content_text = row['content_text']
    content_text = delete_text(content_text)
    content_img_list = str(row['content_img_list']).split(' ')

    if not os.path.exists(page_path):
        os.mkdir(page_path)

    fText = open(f'{page_path}/colossal_page_text_{index}.txt', mode='w', encoding='utf-8')
    fText.write(title)
    fText.write('\n'+'\n')
    fText.write(date)
    fText.write('\n'+'\n')
    fText.write(author)
    fText.write('\n' + '\n')
    fText.write(category)
    fText.write('\n' + '\n')


    fText.write(content_text)
    fText.close()
    print(f'已保存文本-{index}')

    for i in content_img_list:
        img = img_downloads(i)
        imgContent = img[0]
        imgName = img[1]
        fImg = open(f'{page_path}/colossal_page_img_{index}_{imgName}', mode='wb')
        fImg.write(imgContent)
        fImg.close()
        print(f'已保存页面-{index}-图片_{imgName}')
    
    ok_list = open('colossal/ok_list.txt', mode='a', encoding='utf-8')
    ok_list.write(f'{index},')


    print("已完成：", page_path)
    print("-" * 50)



def page_downloads_thread():
    main_path = 'colossal2/'
    csvfile = 'colossal_pageContent.csv'
    df = pd.read_csv(csvfile)
    df = df.drop(columns='Unnamed: 0')
    ok_list = open('colossal/ok_list.txt', mode='w', encoding='utf-8')
    ok_list.close()
    with ThreadPoolExecutor(128) as t:
        for index, row in df[:1].iterrows():
            t.submit(page_downloads, index, row, main_path)
    # ok_list = open('colossal/ok_list.txt', mode='r', encoding='utf-8')
    # ok_list_sort = ok_list.split(',').sort()
    # ok_list_file = open('colossal/ok_list.txt', mode='w', encoding='utf-8')
    # ok_list_file.write(','.join(ok_list_sort))

if __name__ == "__main__":
    # path = 'colossal_pageContent/'
    # csvfile_merge(path)
    # colossal_downloads_thread()
    #
    # csvfile = 'colossal_pageContent.csv'
    # main_path = 'colossal/'
    # df = pd.read_csv(csvfile)
    # df = df.drop(columns='Unnamed: 0')
    # for index, row in df[:2].iterrows():
    #     page_downloads(index, row, main_path)
    page_downloads_thread()