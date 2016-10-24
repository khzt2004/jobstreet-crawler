import scrapy
from scrapy.spider import Spider, CrawlSpider, Rule
from scrapy.selector import HtmlXPathSelector
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
from craigslist_sample.items import CraigslistSampleItem

class MySpider(CrawlSpider):
    name = "craig"
    allowed_domains = ["jobstreet.com.sg"]
    start_urls = ["http://www.jobstreet.com.sg/en/job-search/job-vacancy.php?ojs=10&key=solidworks"]
    download_delay = 1

    rules = (
        Rule(LinkExtractor(restrict_xpaths="//a[@id='page_next']"), follow=True),
        Rule(LinkExtractor(allow=r"/en/job-search/job-vacancy.php\d+$"), callback='parse_item'),
    )

    def parse_item(self, response):
        self.log('\n Crawling  %s\n' % response.url)
        hxs = HtmlXPathSelector(response)
        titles = hxs.xpath('//div[contains(@id, "job_ad")]')
        items = []
        for titles in titles:
            item = CraigslistSampleItem()
            item["title"] = titles.xpath('./div[@class="position-title header-text"]/a/h2/text()').extract()
            item["link"] = titles.xpath('./div[@class="position-title header-text"]/a/@href').extract()
            item["company"] = titles.xpath('./h3/a/span/text() | ./h3/span/text()').extract()
            items.append(item)
        return items
        parse_start_url = parse_item