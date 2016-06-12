:title: Monitoring Async Apps
:author: Amy Boyle
:description: Why and how to measure asynchronous applications
:css: async.css

.. :data-transition-duration: 500

---------------------------------------------------------------

:id: title

:data-scale: 1

Measuring Asynchronous Applications
====================================

Amy Boyle `@amylouboyle`__
***************************

.. note::
    words words words

__ https://twitter.com/amylouboyle

----------------------------------------------------------------

:data-x: r500
:data-y: r1200
:data-z: r-500

**Concurrent** = multiple tasks executing during the same period of time

**Asynchronous** = interleaved execution of task pieces

**Parallel** = execution of multiple tasks in the same time instant

----------------------------------------------------------------

.. image:: img/concurrent_diagram.png

----------------------------------------------------------------

Asynchronous code *yields* execution to other pieces of code

.. code:: python

    class ASyncRequestHandler(RequestHandler):
        async def get(self):
            client = tornado.httpclient.AsyncHTTPClient()
            responses = await [client.fetch(URL) for i in range(10)]
            self.finish('DONE!\n')

    class SyncRequestHandler(RequestHandler):
        def get(self):
            client = tornado.httpclient.HTTPClient()
            responses = [client.fetch(URL) for i in range(10)]
            self.finish('DONE!\n')

----------------------------------------------------------------

Our example app

.. code:: python

    URL = 'http://httpbin.org/delay/1'

    def process(responses):
        # pretend to do processing
        time.sleep(0.5)

    class ASyncRequestHandler(RequestHandler):

        async def get(self):
            client = tornado.httpclient.AsyncHTTPClient()
            responses = await client.fetch(URL)
            self.finish('DONE!\n')
            process(responses)

    application = Application([('/', ASyncFetchRequestHandler))]

    if __name__ == '__main__':
        application.listen(8888)
        tornado.ioloop.IOLoop.current().start()

----------------------------------------------------------------

What to Measure

* Response time
* Duration
* Total self time
* Wait time

