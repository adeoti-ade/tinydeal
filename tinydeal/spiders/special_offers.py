# -*- coding: utf-8 -*-
import scrapy


class SpecialOffersSpider(scrapy.Spider):
    name = 'special_offers'
    allowed_domains = ['www.tinydeal.com']
    # start_urls = ['https://www.tinydeal.com/specials.html']

    def start_requests(self):

        yield scrapy.Request(url= "https://www.tinydeal.com/specials.html", headers= {
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36"
            })

    def parse(self, response):
        result = response.xpath("//ul[@class='productlisting-ul']/div/li")

        for product in result:
            
            yield {
                'title': product.xpath(".//a[@class='p_box_title']/text()").get(),
                'url': response.urljoin(product.xpath(".//a[@class='p_box_title']/@href").get()),
                'discounted_price': product.xpath(".//div[@class='p_box_price']/span[1]/text()").get(),
                'price': product.xpath(".//div[@class='p_box_price']/span[2]/text()").get(),
                'User-Agent': response.request.headers['User-Agent']
            }
        
        next_page = response.xpath("//a[@class='nextPage']/@href").get()

        if next_page:
            yield scrapy.Request(url=next_page, callback=self.parse, headers= {
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36"
            })
