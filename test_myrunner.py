#!/usr/bin/python3

# I wasnt sure what kind of testing do you expect...
# so I implemented both unit testing and the integrative blackbox testing.
# I do believe that better unit tests is a better aproach,
# but I wanted to play a bit with multi-threading.
# for any further explanation do not hessetite to contact me.

import unittest
import threading
import time
from runforever import RunForever
from myrunner import MyRunner
import test_helper
import queue


class TestRunForeverMethods(unittest.TestCase):
    def setUp(self):
        # setting up new instance before each class
        self.defaultAbstractObj = RunForever()
        self.MAXT = RunForever.MAX_COUNTER_VALUE
        self.MINT = RunForever.INITIAL_COUNTER_VALUE
        self.mr = MyRunner()

        # unit tests
    def test_init_reset(self):
        obj = self.defaultAbstractObj
        self.assertEqual(obj.getT(), 1, "initial value of fib should be 1")
        obj.resetT()
        self.assertEqual(obj.getT(), 1, "initial value of fib should be 1")

    def test_inc_no_reset(self):
        a, b = 1, 1
        obj = self.defaultAbstractObj
        for i in range(self.MINT, self.MAXT - 1):
            self.assertEqual(obj.getT(), a, "increasement failed. " + str(i) +
                             "-th element in fib seq IMHO should be " + str(a))
            a, b = b, a + b
            obj.incT()

    def test_inc_reset(self):
        obj = self.defaultAbstractObj
        for i in range(self.MINT, self.MAXT + 1):
            obj.incT()
        self.assertEqual(obj.getT(), 1, "reset failed." +
                         "after MAXT fib seq should be 1")

        # NOTE: IMHO to gain full coverage, we can/should add at least 3
        # more classes implemeting run forever:
        # that run just that returns False, class that returns True and a
        # Fucntion that once return
        # return False, True, False True and so on
        # (also we can throw exceptions and so).
        # than, parse thier logs (in same metter I do in the integration test).
        # [these would check all relavant Equivalence classes IMHO in
        # the logic and will make it more predicted and less tightly-coupled
        # with myrunner class ]

        # some integration black box testing...
        # the idea here is to start my runner, and start the log parser.
        # if log parser gets all the relavant cases from log or
        # timeout is reached - it will join and stop MyRunner.
        # the downside of it - is that it is tightly coupled to
        # the myrunner implentation.

    def test_myRunner(self):
        # set and start the runner
        runner_thread = threading.Thread(target=MyRunner().cant_stop_me_now,
                                         daemon=True)
        runner_thread.start()
        # set and start the logger parser.
        q = queue.Queue()
        parse = test_helper.LogParser()
        parser_thread = threading.Thread(target=parse,
                                         args=(q,), daemon=True)
        parser_thread.start()
        # setting long timeout in order to let it check.
        parser_thread.join(60)
        print("ENDED PARSER THREAD")
        results = (q.get())
        print(results)
        self.assertNotIn(False, results.values(),
                         "there is functionality that doesnt work or tested")
        runner_thread.join(1)
        print ("ENDED CLASS THREAD")

if __name__ == '__main__':
    # TODO: its reasonable to add suites here.
    # one for unit test and one for integration.)
    try:
        unittest.main(verbosity=3)
    except KeyboardInterrupt:
        print("Bye Bye test, got ctrl+c")
