# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
from lxml.html import fromstring
import urllib
from scrapy.http import Request
from scrapy.selector import Selector
from realtor.items import RealtorItem

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import time

class RealtorspiderSpider(scrapy.Spider):
    name = "realtorspider"
    allowed_domains = ["realtor.com"]
    start_urls = (        
        'http://www.realtor.com/',
    )

    base_url = 'http://www.realtor.com'
    def parse(self, response):
        print response.url
        try:
            options = webdriver.ChromeOptions()
            options.add_argument("--start-maximized")
            options.add_argument("--disable-javascript")
            options.add_argument("--disable-java")
            options.add_argument("--disable-plugins")
            options.add_argument("--disable-popup-blocking")
            options.add_argument("--disable-images")
            driver = webdriver.Chrome('c://chromedriver.exe',chrome_options = options)
            links = ['http://www.realtor.com/realestateagents/Cincinnati_OH/realtorType-Agent#/city-Cincinnati/pagesize-50/pg-{}/realtorType-Agent/state-OH'.format(page_no) for page_no in range(30,72)[::-1]]
            for link in links:
                driver.get('http://www.realtor.com/realestateagents/')
                driver.get('http://www.realtor.com/apartments/Cincinnati_OH/type-apartment')

                driver.get(link)
                time.sleep(35)
                html = driver.page_source
                hxs = fromstring(html)
                
                results_item = hxs.xpath('//div[@class="resultsItem agent"]')
                print "total agents"
                print len(results_item)
                for agent in results_item:
                    item = RealtorItem()
                    designation = agent.xpath('.//span[@class="DandC"]/text()')
                    if designation:
                        item['Designation'] = designation
                    brokerage = agent.xpath('.//ul[@class="summary"]/label/text()')
                    if brokerage:
                        item['Brokerage'] = brokerage
                    phone = agent.xpath('normalize-space(.//ul[@class="summary"]/li[@class="phone"]/text())')
                    if phone:
                        item['Phone'] = phone

                    profile_link = agent.xpath('.//ul[@class="summary"]/li[@class="viewProfile"]/a/@href')
                    print designation,brokerage,profile_link
                    # print phone

                    if profile_link:
                        item['URL'] = self.base_url+profile_link[0]
                        driver.get(self.base_url+profile_link[0])
                        time.sleep(1)
                        html = driver.page_source
                        hxs = fromstring(html)
                        agent_modal_body = hxs.xpath('//div[@id="modalcontactInfo"]//div[@class="modal-body"]')
                        if agent_modal_body:
                            agent_modal_body = agent_modal_body[0]
                            print "here in modal body"

                            profile_phone = agent_modal_body.xpath('.//span[@itemprop="telephone"]/text()')
                            if profile_phone:
                                item['profilePhone'] = profile_phone

                            agent_name = agent_modal_body.xpath('.//p[@class="modal-agent-name"]/text()')
                            if agent_name:
                                item['Name'] = agent_name[0].strip(',')

                            agent_location = agent_modal_body.xpath('.//p[@class="modal-agent-location"]/text()')
                            if agent_location:
                                item['Location'] =  agent_location[0].strip('\n ')

                            address = agent_modal_body.xpath('.//span[@itemprop="streetAddress"]/text()')
                            if address:
                                item['Address'] = address

                            website = agent_modal_body.xpath('.//a[@itemprop="url"]/@href')
                            if website:
                                item['Website'] = website

                            facebook = agent_modal_body.xpath('.//a[contains(text(),"Facebook")]/@href')
                            if facebook:
                                item['Facebook'] = facebook

                            linked_in = agent_modal_body.xpath('.//a[contains(text(),"Linkedin")]/@href')
                            if linked_in:
                                item['LinkedIn'] = linked_in

                            # print profile_phone, agent_name, agent_location, address, website, facebook, linked_in
                            print item

                            yield item


        except Exception as e:
                print e
