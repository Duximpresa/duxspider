from scrapy.pipelines.images import ImagesPipeline
from scrapy.pipelines.files import FilesPipeline

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

class BiaoqingbaoPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        pass

    def file_path(self, request, response=None, info=None, *, item=None):
        pass

    def item_completed(self, results, item, info):
        pass
