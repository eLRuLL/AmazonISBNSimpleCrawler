from scrapy.loader import ItemLoader
from scrapylib.processors import default_input_processor, default_output_processor
from amazonisbn.items import AmazonisbnItem


class DefaultItemLoader(ItemLoader):
    default_input_processor = default_input_processor
    default_output_processor = default_output_processor


class AmazonisbnLoader(DefaultItemLoader):
    default_item_class = AmazonisbnItem
