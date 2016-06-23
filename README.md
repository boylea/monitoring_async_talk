Monitoring Asynchronous Applications
====================================

Demo application is in puppy_service.py

Charting app in monitor.py

presentation slides are async.rst

To run the demo:
----------------

Install Tornado and bokeh:

    $ pip install bokeh
    $ pip install tornado

Start the charting server:

    $ bokeh serve --show montior.py

Start the app:

    $ python puppy_service.py

Now send the app some traffic. e.g. via curl:

    $ curl localhost:8888

or via apache bench:

    $ ab -c 10 -n 800 "http://localhost:8888/"