import threading
import time
import urllib

# from concurrent.futures import Future
from tornado.concurrent import Future

import tornado
import tornado.httpclient
from tornado.web import Application, RequestHandler

def feed_puppy(callback=None):
    def do_thing(future):
        time.sleep(0.2)
        future.set_result(True)
    future = Future()
    t = threading.Thread(target=do_thing, args=(future,))
    t.start()

    if callback:
        future.add_done_callback(lambda f: tornado.ioloop.IOLoop.current().add_callback(callback, f))

    return future

def cuddle_pup():
    # pretend to do processing
    time.sleep(0.1)
    pass

class ASyncRequestHandler(RequestHandler):

    def puppy_done_eating(self, future):
        self.meal_done_time = time.time()

    async def get(self):
        start = time.time()

        future = feed_puppy()
        future.add_done_callback(self.puppy_done_eating)

        check0 = time.time()

        await future

        check1 = time.time()

        self.finish('DONE!\n')
        check2 = time.time()

        cuddle_pup()

        end = time.time()

        # save the datas
        response = check2 - self.request._start_time
        total_duration = end - start
        total_time = (check0 - start) + (end - check1)
        service_time = self.meal_done_time - check0
        # print('{0:.2f}\t\t{1:.2f}\t\t{2:.2f}'.format(response, total_duration, total_time))

        client = tornado.httpclient.AsyncHTTPClient()
        times = {"response": response, "duration": total_duration, "self":total_time, "external": service_time}
        times = tornado.escape.json_encode(times)
        post_data = { 'data': times } #A dictionary of your post data
        body = urllib.parse.urlencode(post_data) #Make it into a post request
        client.fetch("http://0.0.0.0:8080/datas", method='POST', headers=None, body=body)

application = Application([
    ('/', ASyncRequestHandler),
])

if __name__ == '__main__':
    # print('Response\tDuration\tExclusive')
    application.listen(8888)
    print("Tornado server listening on port 8888")
    tornado.ioloop.IOLoop.current().start()
