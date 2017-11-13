# -*- coding: utf-8 -*-
import scrapy


class DdSpider(scrapy.Spider):
    name = "dd"
    allowed_domains = ["www.dangdang.com"]  #允许的域名
    start_urls = ['http://www.dangdang.com/'] #起始地址

    #默认处理方法
    def parse(self, response):
        sel=scrapy.Selector(response) #解析html
        #讲选择器转化为列表 extract
        list_d=sel.xpath("//div[@class='e']/a/@href").extract()

        #发送一个请求给下载器，并指定回调函数
        for url in list_d:
            # yield 等同于return,会把所有返回数据封装成一个可迭代对象，并且代码还会往下执行
            yield scrapy.Request(url,callback=self.parse_list)

    #2 抓取分类列表中详细商品链接，并且完成下一页机制
    def parse_list(self,response):
        print(response.url)
        sel = scrapy.Selector(response)
        #做分析 xpath的规则 最耗时间，需要分析该网站的代码规律
        list_d = sel.xpath("//*[@id='component_0__0__8609]/li/a/@href").extract()

        for url in list_d:
            # 不做域名验证
            yield scrapy.Request(url,callback=self.parse_info,dont_filter=True)

        next_page=sel.xpath('//li[@class="next"]/a/@href').extract()
        if next_page:
            next_url="http://category.dangdang.com"+next_page[0]
            return scrapy.Request(next_url,callback=self.parse_list) #调自身，下一页

    #3 商品信息抓取
    def parse_info(self,response):
        sel=scrapy.Selector(response)
        #获取商品信息
        #1 商品名  2 商品id  3商品价格  4 商品分类