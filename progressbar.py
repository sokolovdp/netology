#!/usr/bin/python3
# -*- coding: utf-8

import sys
import time


class Bar:
    def __init__(self, total, message, delay=2.5, last_delay=1.1, barlength=50):
        self.delay = delay  # Delay in secs between progress bar updates
        self.last_delay = last_delay  # Final delay in progress bar updates
        self.barlength = barlength
        self.start_time = time.clock()
        self.total = total
        self.message = message

    def show_progress(self, itr):
        if time.clock() - self.start_time > self.delay:
            percent = int(round((itr / self.total) * 100))
            nb_bar_fill = int(round((self.barlength * percent) / 100))
            bar_fill = '=' * nb_bar_fill
            bar_empty = '-' * (self.barlength - nb_bar_fill)
            sys.stdout.write("\r[{0}] {1}% {2}".format(bar_fill + bar_empty, percent, self.message))
            sys.stdout.flush()
            self.start_time = time.clock()

    def show_progress_100(self, message100):
        time.sleep(self.last_delay)
        bar_fill = '=' * self.barlength
        sys.stdout.write("\r[{0}] {1}% {2}".format(bar_fill, 100, message100))
        sys.stdout.flush()
        print('\n')
