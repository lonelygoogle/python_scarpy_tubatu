import scrapy
import re
import json
from tubaotu_scrapy_project.items import TubaotuScrapyProjectItem

class TubatuSpider(scrapy.Spider):
    name = 'tubatu'
    allowed_domains = ['xiaoguotu.to8to.com']
    start_urls = ['https://xiaoguotu.to8to.com/tuce/p_1.html']

    #  默认的解析方法
    def parse(self, response):
        print(response.request.headers)
        # 正则表达式获取项目id
        content_id_search = re.compile(r"(\d+)\.html")
        pic_item_list = response.xpath("//div[@class='item' and position()>1 ]")
        for item in pic_item_list:
            info = {}
            info['content_name'] = item.xpath(".//div/a/text()").extract_first()
            content_url = 'http:' + item.xpath(".//div/a/@href").extract_first()
            info['content_id'] = content_id_search.search(content_url).group(1)
            info['content_ajax_url'] = 'https://xiaoguotu.to8to.com/case/list?a2=0&a12=&a11='+str(info['content_id'])+'&a1=0&a17=1'
            print(content_url)
            yield scrapy.Request(url=info['content_ajax_url'], callback=self.handle_pic_parse, meta=info)

        # 页码逻辑
        if response.xpath('//a[@id="nextpageid"]'):
            now_page = int(response.xpath('//div[@class="pages"]/strong/text()')).extract_first()
            next_page_url = 'https://xiaoguotu.to8to.com/tuce/p_%d.html' % (now_page+1)
            yield scrapy.Request(url=next_page_url, callback=self.parse)

    def handle_pic_parse(self, response):
        pic_dict_data = json.loads(response.text)['dataImg']
        for pic_item in pic_dict_data:
            for item in pic_item['album']:
                tubatu_info = TubaotuScrapyProjectItem()
                tubatu_info['nick_name'] = item['l']['n']
                tubatu_info['pic_url'] = 'http://pic1.to8to.com/smallcase' + item['l']['s']
                tubatu_info['pic_name'] = item['l']['t']
                tubatu_info['content_name'] = response.request.meta['content_name']
                tubatu_info['content_id'] = response.request.meta['content_id']
                tubatu_info['content_url'] = response.request.meta['content_ajax_url']
                yield tubatu_info