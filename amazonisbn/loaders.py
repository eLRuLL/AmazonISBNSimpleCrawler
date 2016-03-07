from scrapy.loader import ItemLoader
from scrapylib.processors import default_input_processor, default_output_processor
from amazonisbn.items import AmazonisbnItem
from scrapy.loader.processors import MapCompose, Identity, Compose, Join, TakeFirst


class DefaultItemLoader(ItemLoader):
    default_input_processor = default_input_processor
    default_output_processor = default_output_processor


class AmazonisbnLoader(DefaultItemLoader):
    default_item_class = AmazonisbnItem
    found_in = Identity()
    isbn_in = Identity()
