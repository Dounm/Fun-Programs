#!/usr/bin/env python

import sys
import os
import urllib
import urllib2
import re
import threading

class ImageSpider:
    def __init__(self, \
            header = {'User-Agent' : 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'}, \
            image_pattern = r"http[s]?://[\S]*\.gif", \
            title_pattern = r"\<h4\>(.*?)\<\/h4\>",
            timeout = 5):
        self.header = header
        self.image_pattern = re.compile(image_pattern)
        self.title_pattern = re.compile(title_pattern)
        self.timeout = timeout

    def get_page(self, url):
        request = urllib2.Request(url, headers = self.header)
        response = urllib2.urlopen(request)
        page_content = response.read().decode('gbk')
        return page_content

    def get_image_url_list(self, page_content):
        image_url_list = re.findall(self.image_pattern, page_content)
        print 'Extract the image urls done'
        return image_url_list

    def save_image(self, image_url, filename):
        request = urllib2.Request(image_url, headers = self.header)
        #must set the timeout parameter, or it will block
        response = urllib2.urlopen(request, timeout=self.timeout)
        data = response.read()
        print 'Saving [%s]' % filename
        with open(filename, 'wb') as f:
            f.write(data)

    def get_folder_name(self, url, page_content):
        folder = re.findall(self.title_pattern, page_content)[0]
        folder = folder.replace('&nbsp;', ' ')
        if not os.path.exists(folder):
            os.makedirs(folder)
        return folder
    
    def multithread_download(self, folder, spos, epos, image_url_list):
        while spos <= epos:
            filename = folder + '/' + str(spos) + '.gif'
            self.save_image(image_url_list[spos], filename)
            spos += 1

    def main(self, url, thread_num=4):
        page_content = self.get_page(url)
        image_url_list = self.get_image_url_list(page_content)
        folder = self.get_folder_name(url, page_content)

        image_num = len(image_url_list)
        print 'There are %d' % image_num , 'gifs in this url'
        thread_pool = []
        end_pos = -1
        for i in range(thread_num - 1):
            start_pos = end_pos + 1
            end_pos = start_pos + image_num / thread_num - 1
            thread_pool.append(threading.Thread(target = self.multithread_download, \
                    args = (folder, start_pos, end_pos, image_url_list)))
            thread_pool[i].start()
        thread_pool.append(threading.Thread(target = self.multithread_download, \
                args = (folder, end_pos+1, image_num-1, image_url_list)))
        thread_pool[i+1].start()
        
        for thread in thread_pool:
            thread.join()

if __name__ == '__main__':
    url = sys.argv[1]
    thread_num = int(sys.argv[2])
    time_out = int(sys.argv[3])
    spider = ImageSpider(timeout = time_out)
    spider.main(url, thread_num=thread_num)
