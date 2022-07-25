import pandas as pd
from bs4 import BeautifulSoup
import pandas as pd

# f = open('main-content.html', encoding='utf-8')
# soup = BeautifulSoup(f.read(), 'html.parser')
# soup = BeautifulSoup('', 'html.parser')

# content_text = '''
# In the same vein as Phaidon’s formidable Great Women Artists and African Artists, a forthcoming book from the publisher similarly widens the art historical canon while recognizing some of the most influential and impactful painters working in the medium today. The massive compilation, titled Great Women Painters, highlights more than 300 artists across 500 years and a vast array of movements and aesthetics. Arranged alphabetically, the book pairs icons like Yayoi Kusama, Frida Kahlo, and Leonora Carrington with contemporary artists, including Ewa Juszkiewicz, Katharina Grosse, and Wangari Mathenge, in a broad and diverse overview of the women who have had profound impacts on the world today. The nearly 350-page Great Women Painters will be released this fall and is currently available for pre-order from Bookshop. Do stories and artists like this matter to you? Become a Colossal Member today and support independent arts publishing for as little as $5 per month. You'll connect with a community of like-minded readers who are passionate about contemporary art, read articles and newsletters ad-free, sustain our interview series, get discounts and early access to our limited-edition print releases, and much more. Join now!
#
# '''
# content_img_list = ['https://www.thisiscolossal.com/wp-content/uploads/2022/07/135-himid.jpg',
#                     'https://www.thisiscolossal.com/wp-content/uploads/2022/07/138-hughes-scaled.jpg',
#                     'https://www.thisiscolossal.com/wp-content/uploads/2022/07/151-jusziewicz-scaled.jpg',
#                     'https://www.thisiscolossal.com/wp-content/uploads/2022/07/153-kahraman.jpg',
#                     'https://www.thisiscolossal.com/wp-content/uploads/2022/07/192-mathenge.jpg',
#                     'https://www.thisiscolossal.com/wp-content/uploads/2022/07/great-woman-painters-en-6328-3d-spread-1-3880.jpg',
#                     'https://www.thisiscolossal.com/wp-content/uploads/2022/07/great-woman-painters-en-6328-3d-spread-4-3880.jpg',
#                     'https://www.thisiscolossal.com/wp-content/uploads/2022/07/great-woman-painters-en-6328-3d-standing-front-3880.jpg']
csvfile = 'colossal_pageContent.csv'
df = pd.read_csv(csvfile)
df = df.drop(columns='Unnamed: 0')

# for index, row in df.iterrows():
#     title = row['title']
#     content_text = row['content_text']
#     content_img_list = row['content_img_list'].split(',')
#     print(content_img_list)
#
#     print('-' * 20)
#     # print(content_img_list)


def html_building(title,content_text, content_img_list):
    f = open('main-content.html', encoding='utf-8')
    soup = BeautifulSoup(f.read(), 'html.parser')
    p_tag = soup.new_tag("p")
    soup.body.append(p_tag)
    soup.body.p.append(content_text)
    for i in content_img_list:
        img_tag = soup.new_tag("img", src=i)
        soup.body.append(img_tag)

    soup.p['style'] = '''font-family: Inter;
                        font-size: 16px;font-weight: 300;
                        line-height: 24px;
                        -webkit-box-sizing: border-box;
                        display: block;
                        margin-block-start: 1em;
                        margin-block-end: 1em;
                        margin-inline-start: 0px;
                        margin-inline-end: 0px;
                        color: #333333;'''
    # print(soup.prettify())
    f.close()
    return soup.prettify()

    # with open(f'{title}.html', mode='w', encoding='utf-8') as newPage:
    #     newPage.write(soup.prettify())

def main():
    # f = open('main-content.html', encoding='utf-8')
    content_html= []
    for index, row in df.iterrows():
        title = row['title']
        content_text = row['content_text']
        content_img_list = str(row['content_img_list']).split(' ')
        # print(content_img_list)

        html = html_building(title, content_text, content_img_list)
        content_html.append(html)
        print(f"已完成{index}")
        print('-' * 20)
    df_html = pd.DataFrame(content_html,columns=['content_html'])
    frames = [df, df_html]
    new_df = pd.concat(frames, axis=1, join='outer',sort=False)
    print(new_df)
    new_df.to_csv("colossal_pageContentHtml.csv", encoding="utf_8_sig")

if __name__ == '__main__':
    main()