import time

import numpy as np

import tornado
from tornado.web import Application, RequestHandler
from bokeh.plotting import figure, curdoc
from bokeh.io import vplot, hplot
from bokeh.palettes import Spectral4

dtypes = ['response', 'duration', 'cpu', 'external']
# spectral works better with projector
colors = Spectral4
data_samples = []

x = np.linspace(100, 0, 100)

performace_plot = figure(title="95% percentile", x_axis_label='seconds ago', y_axis_label='time (s)')#, width=500, height=300)
plot_data = {}
plot_lines = {}
for i, dtype in enumerate(dtypes):
    plot_data[dtype] = np.zeros_like(x)
    plot_lines[dtype] = performace_plot.line(x, plot_data[dtype], legend=dtype,
            line_width=4, color=colors[i])


throughput_plot = figure(title="Throughput", x_axis_label='x', y_axis_label='# of requests')#, width=500, height=300)
throughput_data = np.zeros_like(x)
throughput_line = throughput_plot.line(x, throughput_data)

def harvest():
    global plot_data, data_samples, throughput_data
    crop = data_samples[:]
    data_samples = []
    for dtype in dtypes:
        times = [d[dtype] for d in crop]
        try:
            if len(times) > 0:
                # data_point = sum(times)/len(times)
                times.sort()
                index95 = max(int(len(times)*0.95), len(times) -1)
                # print("TIMES", times, index95)
                data_point = times[index95]
            else:
                data_point = 0

        except ZeroDivisionError:
            data_point = 0
        pdata = plot_data[dtype]
        pline = plot_lines[dtype]
        pdata = np.roll(pdata, -1)
        pdata[-1] = data_point
        pline.data_source.data["y"] = pdata
        plot_data[dtype] = pdata

    throughput_data = np.roll(throughput_data, -1)
    throughput_data[-1] = len(crop)
    throughput_line.data_source.data["y"] = throughput_data


class DataReceiever(RequestHandler):
    def post(self):
        global data_samples

        post_data = self.get_arguments('data')[0]
        times = tornado.escape.json_decode(post_data)
        data_samples.append(times)

    def get(self):
        self.finish('This is an endpoint for collection of performance data')


curdoc().add_periodic_callback(harvest, 1000)
p = hplot(performace_plot, throughput_plot)
curdoc().add_root(p)

endpoints = [(r'/datas', DataReceiever)]
from tornado.web import Application
data_app = Application(endpoints)
data_app.listen(8080)
