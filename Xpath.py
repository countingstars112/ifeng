# coding: utf-8
import re


def pathOneNode(tree, path):
    try:
        content = tree.xpath(path)
        return re.sub('\s', '', content[0])
    except Exception as e:
        # print 'Xpath解析错误:', e
        return None


def pathAllNode(tree, path):
    try:
        content = tree.xpath(path)
        return re.sub('\s', '', content[0].xpath('string(.)'))
    except Exception as e:
        # print 'Xpath解析错误:++'+path, e
        return None


def pathGetImg(tree, path):
    try:
        content = tree.xpath(path)
        if content:
            return content
        else:
            return None
    except Exception as e:
        # print 'Xpath解析错误:++'+path, e
        return None