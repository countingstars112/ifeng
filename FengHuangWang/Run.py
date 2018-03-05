# coding: utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import time
from NewsMessage import NewsMessage

run = NewsMessage()


while 1:
    run.getNewsTotleUrl()
    print "休眠5小时"
    time.sleep(60 * 60 * 5)