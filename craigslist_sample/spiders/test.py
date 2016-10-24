from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from craigslist_sample.items import CraigslistSampleItem

class MySpider(BaseSpider):
    name = "craig"
    allowed_domains = ["jobstreet.com.sg"]
    start_urls = ["http://www.jobstreet.com.sg/en/job-search/job-vacancy.php?ojs=10&key=solidworks"]

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        titles = hxs.xpath('//div[contains(@id, "job_ad")]')
        items = []
        for titles in titles:
            item = CraigslistSampleItem()
            item["title"] = titles.xpath('./div[@class="position-title header-text"]/a/h2/text()').extract()
            item["link"] = titles.xpath('./div[@class="position-title header-text"]/a/@href').extract()
            items.append(item)
        return items