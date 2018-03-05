# coding:utf-8
import time
from lxml import etree
from Xpath import *
from NewsComment import NewsComment
from Pipe import MongoDB
import requests
import NewsUrl
import json


class NewsMessage(object):
    def __init__(self):
        self.comment = NewsComment()
        self.mongo = MongoDB()
        self.f = open('test.txt', "r+")
        self.i = 0
        self.url_list =[]

    def getNewsTotleUrl(self):
        for news_url in NewsUrl.Run():
            self.getNewsMessage(news_url)

        if self.f.read():
            with open('test.txt', 'r+') as f:
                a = json.load(f)
            url_list_before = a['url']
            for url_before in url_list_before:
                url_json = json.loads(url_before)['wen_zhang_wang_zhi']
                pin_lun_shu = self.getPinglun(url_json)
                if pin_lun_shu != json.loads(url_before)['ping_lun_shu_liang']:
                    self.getNewsMessage(url_json)
                else:
                    url_list_before.remove(url_before)
        self.file_close(url_list_before)


    def getNewsMessage(self, news_url):
        self.i += 1
        print self.i
        print news_url
        html = ''
        flag = 1
        while 1:
            try:
                html = requests.get(news_url, timeout=30).content
                break
            except Exception as e:
                flag += 1
                print e
            if flag > 10:
                return
        tree = etree.HTML(html)

        """这一段代码是用来获取阅读数和评论数的"""
        comment_number = self.getCommentNumber(news_url)
        if comment_number:
            yue_du_shu = comment_number[0]
            ping_lun_shu_liang = comment_number[1]
        else:
            yue_du_shu = 0
            ping_lun_shu_liang = 0

        message_dict = dict()
        message_url = dict()

        # 文章网址
        wen_zhang_wang_zhi = news_url
        message_dict['wen_zhang_wang_zhi'] = wen_zhang_wang_zhi
        message_url['wen_zhang_wang_zhi'] = wen_zhang_wang_zhi

        # 文章标题
        wen_zhang_biao_ti = pathOneNode(tree, '//title/text()')
        if  wen_zhang_biao_ti != None:
            wen_zhang_biao_ti = wen_zhang_biao_ti.replace('_', '').replace(u"娱乐频道", "").replace(u"凤凰网","").replace(u'凤凰体育','').replace(u'凤凰财经','')
        message_dict['wen_zhang_biao_ti'] =wen_zhang_biao_ti

        # 发布时间
        fa_bu_shi_jian = pathOneNode(tree, '//span[@itemprop="datePublished"]/text()')
        if fa_bu_shi_jian == None:
            fa_bu_shi_jian = pathOneNode(tree, '//*[@id="titL"]/p/span/text()')
        message_dict['fa_bu_shi_jian'] = fa_bu_shi_jian

        # 评论数量
        ping_lun_shu_liang = ping_lun_shu_liang
        message_dict['ping_lun_shu_liang'] = ping_lun_shu_liang
        message_url['ping_lun_shu_liang'] = ping_lun_shu_liang

        # 文章来源
        wen_zhang_lai_yuan = pathOneNode(tree, '//span[@itemprop="publisher"]/span/a/text()')
        if wen_zhang_lai_yuan == None:
            wen_zhang_lai_yuan = pathOneNode(tree, '//*[@id="artical_sth"]/p/span[3]/span/text()')
        if wen_zhang_lai_yuan == None:
            wen_zhang_lai_yuan = u'凤凰网'
        message_dict['wen_zhang_lai_yuan'] = wen_zhang_lai_yuan

        # 文章正文
        wen_zhang_zheng_wen = pathAllNode(tree, '//div[@id="main_content"]')
        if wen_zhang_zheng_wen == None:
            try:
                re_ = "G_listdata=..\n{1,}.*({title:\'[\S\s]+?])"
                re__ = "{title:\'([\S\s]+?)\',"
                text_first = re.findall(re_, html)
                text_conten = re.findall(re__, text_first[0])
                wen_zhang_zheng_wen = "".join(text_conten)
            except Exception as e:
                try:
                    wen_zhang_zheng_wen = pathAllNode(tree, '//*[@id="slidedesc2"]')
                except Exception as e:
                    wen_zhang_zheng_wen = None
        message_dict['wen_zhang_zheng_wen'] = wen_zhang_zheng_wen

        # 抓取时间
        do_time = time.time()
        message_dict['do_time'] = do_time

        # 抓取网站
        zhan_dian = u'凤凰网'
        message_dict['zhan_dian'] = zhan_dian

        # 图片链接
        tu_pian_lian_jie = pathGetImg(tree, '//*[@id="main_content"]//img[@alt]/@src')
        if tu_pian_lian_jie:
            message_dict['tu_pian_lian_jie'] = " ".join(tu_pian_lian_jie)
        else:
            message_dict['tu_pian_lian_jie'] = None


        # 文章栏目
        wen_zhang_lan_mu = pathAllNode(tree, '//div[@class="theCurrent cDGray js_crumb"]')
        if wen_zhang_lan_mu == None:
            wen_zhang_lan_mu = pathAllNode(tree, '//div[@class="speNav js_crumb"]')
        if wen_zhang_lan_mu == None:
            wen_zhang_lan_mu = pathAllNode(tree, '//div[@class="cmtNav js_crumb"]')
        try:
            message_dict['wen_zhang_lan_mu'] = wen_zhang_lan_mu.replace('>', '->')
        except Exception as e:
            message_dict['wen_zhang_lan_mu'] = wen_zhang_lan_mu

        # 文章作者
        wen_zhang_zuo_zhe = None
        message_dict['wen_zhang_zuo_zhe'] = wen_zhang_zuo_zhe

        # 关键词
        guan_jian_ci = None
        message_dict['guan_jian_ci'] = guan_jian_ci

        # 相关标签
        xiang_guan_biao_qian = None
        message_dict['xiang_guan_biao_qian'] = xiang_guan_biao_qian

        # 阅读数量
        yue_du_shu = yue_du_shu
        message_dict['yue_du_shu'] = yue_du_shu

        # 主键
        message_dict['_id'] = news_url

        # #时间
        # d1 = datetime.datetime.now().date()
        # message_url['time'] = d1


        # print json.dumps(message_dict, ensure_ascii=False, indent=4)
        if wen_zhang_zheng_wen != None and wen_zhang_biao_ti != None:
            self.mongo.put_content(message_dict)
            self.url_list.append(json.dumps(message_url, sort_keys=True, indent=4))
            print message_dict
            if ping_lun_shu_liang > 0:
                all_page = ping_lun_shu_liang / 20
                for page in xrange(1, all_page + 1):
                    self.comment.run(news_url, page)


    def getPinglun(self, news_url):
        """这一段代码是用来获取和评论数的"""
        comment_number = self.getCommentNumber(news_url)
        if comment_number:
            ping_lun_shu_liang = comment_number[1]
        else:
            ping_lun_shu_liang = 0
        return ping_lun_shu_liang



    def file_close(self, url_list_before):
        url_dirc=dict()
        end_url= self.url_list+url_list_before
        url_dirc['url'] = end_url
        self.f.truncate(0)
        self.f.seek(0, 0)
        self.f.write(json.dumps(url_dirc))
        self.f.close()


    def getCommentNumber(self, news_url):
        json_object = dict()
        comment_url = 'http://comment.ifeng.com/get.php?doc_url=%s&format=js&job=1' % news_url
        flag = 1
        while 1:
            try:
                json_object = json.loads(requests.get(comment_url, timeout=30).content.replace('var commentJsonVarStr___=', '')[:-1])
                break
            except Exception as e:
                flag += 1
                print e
            if flag > 5:
                return
        # 阅读数
        yue_du_shu = json_object['join_count']
        # 评论数
        ping_lun_shu_liang = json_object['count']
        return yue_du_shu, ping_lun_shu_liang


if __name__ == '__main__':
    newMessage = NewsMessage()
    newMessage.getNewsMessage('http://ent.ifeng.com/a/20170801/42961199_0.shtml')


