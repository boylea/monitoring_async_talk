import threading
import time

import tornado
import tornado.httpclient
from tornado.web import Application, RequestHandler

URL = 'http://httpbin.org/delay/1'

def process(responses):
        # pretend to do processing
        time.sleep(0.5)
        pass

class ASyncRequestHandler(RequestHandler):

    async def get(self):
        start = time.time()

        client = tornado.httpclient.AsyncHTTPClient()

        req = tornado.httpclient.HTTPRequest(URL)
        future = client.fetch(req)

        check0 = time.time()
        responses = await future
        check1 = time.time()

        self.finish('DONE!\n')
        check2 = time.time()

        process(responses)

        end = time.time()
        # save the datas
        fetch_time = req._fetch_time
        response = check2 - start
        total_duration = end - start
        total_time = (check0 - start) + (end - check1)
        wait = fetch_time - check0
        print('{0:.2f}\t\t{1:.2f}\t\t{2:.2f}\t\t{3:.2f}'
                .format(response, total_duration, total_time, wait))

class SyncRequestHandler(RequestHandler):

    def get(self):
        client = tornado.httpclient.HTTPClient()
        response = requests.get(URL)
        self.finish('DONE!\n')

class ParallelRequestHandler(RequestHandler):

    def get(self):

        threads = []
        for i in range(10):
            t = threading.Thread(target=requests.get, args=(URL,))
            t.start()
            threads.append(t)

        for t in threads:
            t.join()

        self.finish('DONE!\n')

application = Application([
    ('/', ASyncRequestHandler),
    ('/sync', SyncRequestHandler),
    ('/parallel', ParallelRequestHandler),
])

if __name__ == '__main__':
    print('Response\tDuration\tExclusive\tWait')
    application.listen(8888)
    # print("Tornado server listening on port 8888")
    tornado.ioloop.IOLoop.current().start()