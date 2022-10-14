from scrapy.pipelines.images import ImagesPipeline
from scrapy.pipelines.files import FilesPipeline
from scrapy import Request
import re

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


# class BiaoqingbaoPipeline:
#     def process_item(self, item, spider):
#         img = item["img"]
#         # print(img[0])
#         for img_title, img_src in img:
#             print(img_title, img_src)
#
#
#         return item

def clean_file_name(filename: str):
    invalid_chars = r'[\\\/:*?"<>|]'
    replace_char = '_'
    return re.sub(invalid_chars, replace_char, filename)

class BiaoqingbaoPipeline(FilesPipeline):
    def get_media_requests(self, item, info):
        img = item["img"]
        title = item["title"]
        # print(title)
        for img_title, img_src in img:
            # print(img_title)
            yield Request(img_src, meta={"img_title": img_title, "img_src": img_src, "title": title})


    def file_path(self, request, response=None, info=None, *, item=None):
        # print("接收到一条数据", request)
        img_title = request.meta["img_title"]
        img_title = clean_file_name(img_title)
        img_src = request.meta["img_src"]
        suffix = img_src.split(".")[-1]
        code4 = img_src.split(".")[-2][-5:-1]
        title = request.meta["title"]
        title = clean_file_name(title)
        file_path =  f"hot/{title}/{img_title}_{code4}.{suffix}"
        print(file_path)
        return file_path


    def item_completed(self, results, item, info):
        return item
