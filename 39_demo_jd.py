# coding:utf-8

import requests
from bs4 import BeautifulSoup
import lxml
import threading
import Queue
import time
import urllib
import codecs
import json
import random
import pickle
import numpy


# from SQL import save_mysql  # 导入sql存储数据
# import MySQLdb as db


class spiders:
    def __init__(self, page):
        # self.url = 'https://search.jd.com/Search?keyword=%E8%A3%A4%E5%AD%90&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&offset=5&wq=%E8%A3%A4%E5%AD%90&page=' + str(
        #     page)
        # self.url = 'http://ypk.39.net/search/保健品-p'+str(i)+'/'
        self.headers = {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'}
        # self.search_urls = 'https://search.jd.com/s_new.php?keyword=%E6%99%AE%E4%B8%BD%E6%99%AE%E8%8E%B1%20%E4%BA%AC%E4%B8%9C%E8%87%AA%E8%90%A5&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&bs=1&suggest=3.def.0.V05&wq=%E6%99%AE%E4%B8%BD%E6%99%AE%E8%8E%B1&ev=exbrand_%E6%99%AE%E4%B8%BD%E6%99%AE%E8%8E%B1%EF%BC%88Puritan%27s%20Pride%EF%BC%89%5E&stock=1&page=2&s=31&scrolling=y&log_id=1515380984.36917&tpl=1_M&show_items=2622752,2366129,2289451,2365252,2355514,2608225,2356469,2451575,2366119,2123768,3572036,2289457,2288508,1938923,3705503,3516276,1926187,4484113,4279152,3791179,2288506,3562384,2656316,4279190,3572010,2622474,2481303,2365264,2365174,2365188'
        self.pids = set()  # 页面中所有的id,用来拼接剩下的30张图片的url,使用集合可以有效的去重
        self.img_urls = set()  # 得到的所有图片的url
        self.detail_urls = set()  # 得到的所有产品的url
        self.all_urls = []  # 得到的所有产品的url
        self.search_page = page + 1  # 翻页的作用
        # self.sql = save_mysql()  # 数据库保存


    # ip池
    def proxypool(self,num):
        n = 1
        fp = open('host.txt', 'r')
        proxys = list()
        ips = fp.readlines()
        while n < num:
            for p in ips:
                ip = p.strip('\n').split('\t')
                proxy = 'http:\\' + ip[0] + ':' + ip[1]
                proxies = {'proxy': proxy}
                proxys.append(proxies)
                n += 1
        return proxys

    # 得到39 a_href
    def get_a_href(self):
        proxyPool = self.proxypool(50)
        for i in range(1, 872):
            print (u'第',i,u'页')
            url = 'http://ypk.39.net/search/%E4%BF%9D%E5%81%A5%E5%93%81-c3-p' + str(i) + '/'
            res = requests.get(url, headers=self.headers, proxies=random.choice(proxyPool))
            html = res.text
            soup = BeautifulSoup(html, 'lxml')
            ul = soup.find('ul', class_='search_ul search_ul_yb')
            lis = ul.find_all('li')
            # print ('lis:', lis)
            for li in lis:
                # data_pid = li.get("data-pid")
                href = li.find('a').get('href')
                if (href):
                    self.detail_urls.add(href)
                    self.all_urls.append(href)
                    # print "-------------------------------------------------------------"
        # print ('all_urls:', self.all_urls)
        print ('detail_urls_len:', len(self.detail_urls))
        # numpy.savetxt('arr.txt',self.detail_urls)
        numpy.save('arr1_ob.npy', self.detail_urls)
        numpy.save('arr_all_ob.npy', self.all_urls)
        # output = open('data.pkl', 'wb')
        # pickle.dump(self.detail_urls, output)
        # output.close()
        # with open('data.json', "w+", encoding='utf-8') as outfile:
        #     json.dump(self.detail_urls, outfile, ensure_ascii=False)
        #     outfile.write('\n')

    # 得到每一页的网页源码
    def get_html(self,i ):
        print (i, 111111)
        url = 'http://ypk.39.net/search/保健品-p' + str(i) + '/'
        res = requests.get(url, headers=self.headers)
        html = res.text
        return html

    # 得到每一个页面的id
    def get_pids(self):
        for i in range(1, 3):
            html = self.get_html(i)
            soup = BeautifulSoup(html, 'lxml')
            ul = soup.find('ul', class_='search_ul search_ul_yb')
            lis = ul.find_all('li')
            print ('lis:', lis)
            for li in lis:
                # data_pid = li.get("data-pid")
                href = li.find('a').get('href')
                if (href):
                    self.detail_urls.add(href)
                    # print "-------------------------------------------------------------"
        print ('detail_urls:', self.detail_urls)
        print ('detail_urls_len:', len(self.detail_urls))

    # 得到每一个页面的图片和一些数据，由于这是aiax加载的，因此前面一段的img属性是src，后面的属性是data-lazy-img
    def get_src_imgs_data(self):
        html = self.get_html()
        soup = BeautifulSoup(html, 'lxml')
        divs = soup.find_all("div", class_='p-img')  # 图片
        # divs_prices = soup.find_all("div", class_='p-price')   #价格
        for div in divs:
            href = div.find('a').get('href')
            # img_1 = div.find("img").get('data-lazy-img')  # 得到没有加载出来的url
            img_2 = div.find("img").get("src")  # 得到已经加载出来的url
            # if img_1:
            #     print ('img_1:',img_1)
            # self.sql.save_img(img_1)
            # self.img_urls.add(img_1)
            if img_2:
                print ('img_2:', img_2)
                # self.sql.save_img(img_2)
                self.img_urls.add(img_2)
            self.detail_urls.add(href)
        print "--------------------------------------------------"
        print ('detail_urls:', self.detail_urls)

        # 这个是得到后面30张的图片和数据，由于是ajax加载的，打开一页会显示前30张的一部分，但是后面30张都保存在这个网页中，因此要请求这个网页得到原来的网站

    def get_extend_imgs_data(self):
        # self.search_urls=self.search_urls+','.join(self.pids)
        # self.search_urls = self.search_urls.format(str(self.search_page), ','.join(self.pids))
        print self.search_urls
        html = requests.get(self.search_urls, headers=self.headers).text
        soup = BeautifulSoup(html, 'lxml')
        div_search = soup.find_all("div", class_='p-img')
        lis = soup.find_all("li", class_='gl-item')
        for li in lis:
            # data_pid = li.get("data-pid")
            href = li.find('a').get('href')
            if (data_pid):
                self.pids.add(data_pid)
                # print self.pids
            if (href):
                self.detail_urls.add(href)

        print ('detail_urls:', self.detail_urls)
        print ('detail_urls_len:', len(self.detail_urls))
        # for div in div_search:
        #     img_3 = div.find("img").get('data-lazy-img')
        #     img_4 = div.find("img").get("src")
        #
        #     if img_3:
        #         print img_3
        #         # self.sql.save_img(img_3)
        #         self.img_urls.add(img_3)
        #     if img_4:
        #         print img_4
        #         # self.sql.save_img(img_4)
        #         self.img_urls.add(img_4)

    def main(self):
        # self.get_pids()
        self.get_a_href()
        # self.get_src_imgs_data()
        # self.get_extend_imgs_data()
        # print len(self.img_urls)
        print "------------------------------------------------------------------------------------"


if __name__ == '__main__':
    threads = []
    for i in range(1, 2):
        page = i * 2 - 1  # 这里每一页对应的都是奇数，但是ajax的请求都是偶数的，所有在获取扩展的网页时都要用page+1转换成偶数
        t = threading.Thread(target=spiders(page).main, args=[])
        threads.append(t)
    for t in threads:
        t.start()
        t.join()
    print "end"

# if __name__ == '__main__':
#     data_pids=[]
#     img_urls=[]
#     url='https://search.jd.com/Search?keyword=%E8%A3%A4%E5%AD%90&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&offset=5&wq=%E8%A3%A4%E5%AD%90&page=1'
#     search_url='https://search.jd.com/s_new.php?keyword=%E8%A3%A4%E5%AD%90&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&offset=3&wq=%E8%A3%A4%E5%AD%90&page=2&s=26&scrolling=y&pos=30&show_items='
#     headers={'User-Agent':'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'}
#     res=requests.get(url,headers=headers)
#     html=res.text
#     soup=BeautifulSoup(html,'lxml')
#     lis=soup.find_all("li",class_='gl-item')
#     divs=soup.find_all("div",class_='p-img')
#     for div in divs:
#         img_1=div.find("img").get('data-lazy-img')
#         img_2=div.find("img").get("src")
#         if img_1:
#             print img_1
#             img_urls.append(img_1)
#         if img_2:
#             print img_2
#             img_urls.append(img_2)
#
#     for li in lis:
#         data_pid=li.get("data-pid")
#         if(data_pid):
#             data_pids.append(data_pid)
#
#     pids= ",".join(data_pids)
#
#
#
#     res_search=requests.get(search_url+pids,headers=headers)
#     search_html=res_search.text
#     print res_search.url
#     soup_s=BeautifulSoup(search_html,'lxml')
#     div_search=soup_s.find_all("div",class_='p-img')
#     for div in div_search:
#         img_3 = div.find("img").get('data-lazy-img')
#         img_4 = div.find("img").get("src")
#
#         if img_3:
#             print img_3
#             img_urls.append(img_3)
#         if img_4:
#             print img_4
#             img_urls.append(img_4)
#
#
#     print len(img_urls)
