#!/usr/bin/env python
#
# Copyright (c) 2015 Corey Goldberg
# License: MIT


import collections
import textwrap
import csv
import time
import webb
import os
import argparse
from selenium import webdriver
from datetime import datetime
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

parser = argparse.ArgumentParser()
parser.add_argument("--Fname", type=str, required=True,help="File Name")
FNAME = parser.parse_args().Fname

class PageLoadTimer:

    def __init__(self, driver):
        """
            takes:
                'driver': webdriver instance from selenium.
        """
        self.driver = driver

        self.jscript = textwrap.dedent("""
            var performance = window.performance || {};
            var timings = performance.timing || {};
            return timings;
            """)

    def inject_timing_js(self):
        timings = self.driver.execute_script(self.jscript)
        return timings

    def get_event_times(self):
        timings = self.inject_timing_js()
        # the W3C Navigation Timing spec guarantees a monotonic clock:
        #  "The difference between any two chronologically recorded timing
        #   attributes must never be negative. For all navigations, including
        #   subdocument navigations, the user agent must record the system
        #   clock at the beginning of the root document navigation and define
        #   subsequent timing attributes in terms of a monotonic clock
        #   measuring time elapsed from the beginning of the navigation."
        # However, some navigation events produce a value of 0 when unable to
        # retrieve a timestamp.  We filter those out here:
        good_values = [epoch for epoch in timings.values() if epoch != 0]
        # rather than time since epoch, we care about elapsed time since first
        # sample was reported until event time.  Since the dict we received was
        # inherently unordered, we order things here, according to W3C spec
        # fields.
        ordered_events = ('navigationStart', 'fetchStart', 'domainLookupStart',
                          'domainLookupEnd', 'connectStart', 'connectEnd',
                          'secureConnectionStart', 'requestStart',
                          'responseStart', 'responseEnd', 'domLoading',
                          )
        event_times = ((event, timings[event] - min(good_values)) for event
                       in ordered_events if event in timings)
        #print(f"secured start time is {timings['secureConnectionStart']}")
        return collections.OrderedDict(event_times)

def main():
    rows = []
    fields = ['dateTime','connectStart', 'secureConnectionStart', 'requestStart','responseStart','networkTime', 'serverTime']
    all_events = ['dateTime','navigationStart', 'fetchStart', 'domainLookupStart',
                          'domainLookupEnd', 'connectStart', 'connectEnd',
                          'secureConnectionStart', 'requestStart',
                          'responseStart', 'responseEnd', 'domLoading',
                          ]
    #with Xvfb() as xvfb:
   
    # url = "https://en.wikipedia.org/wiki/Carnegie_Mellon_University#/media/File:Carnegie_Mellon_University_seal.svg"
    # url = "http://10.10.1.2:8000"
    url = "https://10.10.1.2:8000"
    counter = 0
    while counter < 2:
        options = webdriver.FirefoxOptions()
        options.add_argument("-headless")
        firefox_binary = FirefoxBinary()
        driver = webdriver.Firefox(options=options, firefox_binary=firefox_binary)
        driver.get(url)
        timer = PageLoadTimer(driver)
        theTime = timer.get_event_times()
        rows.append([datetime.now().strftime('%Y-%m-%d %H:%M:%S'),theTime['navigationStart'], theTime['fetchStart'],\
                        theTime['domainLookupStart'], theTime['domainLookupEnd'], \
                    theTime['connectStart'],theTime['connectEnd'], \
                    theTime['secureConnectionStart'],theTime['requestStart'], \
                    theTime['responseStart'], theTime['responseEnd'], \
                    theTime['domLoading']])
        # rows.append([datetime.now().strftime('%Y-%m-%d %H:%M:%S'),theTime['connectStart'], theTime['secureConnectionStart'],\
        #                 theTime['requestStart'], theTime['responseStart'], \
        #             theTime['secureConnectionStart'] - theTime['connectStart'], \
        #             theTime['responseEnd'] - theTime['requestStart']])
        #             # theTime['responseStart'] - theTime['requestStart']])
        driver.quit()
        counter += 1
        print(f"Round {counter} finished")
        time.sleep(10)

    # name of csv file  
    filename = FNAME
        
    # writing to csv file  
    with open(filename, 'a') as csvfile:  
        # creating a csv writer object  
        csvwriter = csv.writer(csvfile)  
            
        # # writing the fields  
        # csvwriter.writerow(fields)
        csvwriter.writerow(all_events)  
            
        # writing the data rows  
        csvwriter.writerows(rows) 

def traceroute(url):
    result, unans = traceroute(url,maxttl=32)
    print(result)

if __name__ == '__main__':
    # url = "https://en.wikipedia.org/wiki/Carnegie_Mellon_University#/media/File:Carnegie_Mellon_University_seal.svg"
    # webb.traceroute(url)
    main()
    # ipaddr = "154.6.85.146"
    # response = os.system("ping " + ipaddr)
    # print(response)