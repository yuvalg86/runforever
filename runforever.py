#!/usr/bin/python3
import time
from abc import abstractmethod


def fib_backoff_function(n):
    # this is the backoff function implementation.
    # this is the least(!) efficient way to do it - yet it
    # increases readibility & modulization.
    # moduliztion in the term that if someday we would move it to
    # exponenetial backoff - this would mean altering only this part.
    # the more effiecient solution would be to have a,b as class members
    # without calculating the previous numbers each time
    a, b = 1, 1
    for i in range(n):
        a, b = b, a+b
    return a


class RunForever:
    INITIAL_COUNTER_VALUE = 0
    MAX_COUNTER_VALUE = 6

    def __init__(self):
        self.backoff_cnt = RunForever.INITIAL_COUNTER_VALUE
        self.calc_T = fib_backoff_function
        self.sleep = time.sleep

    def resetT(self):
        self.backoff_cnt = RunForever.INITIAL_COUNTER_VALUE

    def getT(self):
        return self.calc_T(self.backoff_cnt)

    def incT(self):
        self.backoff_cnt += 1
        if self.backoff_cnt >= RunForever.MAX_COUNTER_VALUE:
            self.resetT()

    # could be __call__ and than
    # for B inharits RunForever we could just implement B.run function.
    # and in main: B() would run it.
    def cant_stop_me_now(self):
        while True:
            if self.run():
                self.resetT()
            else:
                self.sleep(self.getT())
                self.incT()

    @abstractmethod
    def run(self): pass
