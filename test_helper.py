#!/usr/bin/python3

from myrunner import MyRunner
from runforever import RunForever
import time
import queue

EPSILON_SEC = 0.1


def calc_fib(n):
    # this code repetition from runforever is
    # actually neccesery (in order to verify test the T)
        a, b = 1, 1
        for i in range(n):
            a, b = b, a+b
        return a


def check_interval(time1, time2, epsilon_SEC=EPSILON_SEC):
    return (abs(time1-time2) <= epsilon_SEC)


# calcs the correct delta for values.
def calc_delta(prev_value, curr_value, false_sequence):
    if prev_value:
        return 0
    else:
        return calc_fib(false_sequence)


# gets what is needed form the log line
def parse_line(line):
    line_list = line.strip().split('|')
    value = bool(line_list[1])
    timestamp = float(line_list[0])
    return value, timestamp


# helper for is_sublist
def n_slices(n, list_):
    for i in range(len(list_) + 1 - n):
        yield list_[i:i+n]


# checks if sublist is in list.
def is_sublist(list, sub_list):
    for slice_ in n_slices(len(sub_list), list):
        if slice_ == sub_list:
            return True
    return False


# parse not the first line logic.
class LogParser:

    def __init__(self, log_file=MyRunner.LOGGING_FILENAME):
        self.log_file = log_file
        self.correct_sleep = 'currect sleep (T)'
        self.got_log = 'got log file'
        # these are the cases needed in order to make a
        # decistion iff class is working or not.
        # we can extend them in any moment...

        self.False_true_false = tuple([False, False, False, True, False])
        maxVal = RunForever.MAX_COUNTER_VALUE
        self.MaxT_falses = tuple([False] * (maxVal + 1))

        # these are the results on the tested functionality.
        self.results = {self.got_log: False, self.MaxT_falses: None,
                        self.False_true_false: None, self.correct_sleep: None}
        # represents the sequnce in this run...
        self.sequence = []
        # number of falses in current round.
        self.false_sequence = 0
        # number of line in the log(mainly for debugging)
        self.line_cnt = 1
        # previous value
        self.prev_value = None

    def check_correctness_line(self):
        # check if interval between this and previous line makes sense
        expected_delta = calc_delta(self.prev_value, self.value,
                                    self.false_sequence)
        if not check_interval(self.timestamp, self.prev_time + expected_delta):
            self.results[self.correct_sleep] = False
            error_str = "Error! ran {}->{}. expected_delta is {}" \
                        " but got {}. sequence is {}".format(
                            self.prev_value, self.value, expected_delta,
                            self.timestamp - self.prev_time, self.sequence)
            raise Exception(error_str)
        else:
            self.results[self.correct_sleep] = True
        # if its a false sequence, update
        if self.value is False and self.prev_value is False:
            self.false_sequence += 1
            if self.false_sequence >= RunForever.MAX_COUNTER_VALUE:
                self.false_sequence = 0
        else:
            self.false_sequence = 0
        # set prev = this
        self.prev_value = self.value
        self.prev_time = self.timestamp

    # runs on log_file and verifies for
    # correctness until finds all the sequnces.
    def __call__(self, q):
        try:
            with open(self.log_file, 'r') as fp:
                print ("printing log lines from the spawned class -")
                # while theres a pattern then we didnt find yet
                while None in self.results.values():
                    line = fp.readline()
                    while (line and None in self.results.values()):
                        # parse line to value and timestamp
                        self.value, self.timestamp = parse_line(line)
                        # add it to the current sequence list
                        self.sequence.append(self.value)
                        print("Line {}: PREV_VAL={} VAL={} TIME={} ".format(
                            self.line_cnt, self.prev_value,
                            self.value, self.timestamp))
                        if self.line_cnt == 1:
                            # case where it is the first line - prev is none.
                            self.results[self.got_log] = True
                            self.prev_time = self.timestamp
                            self.prev_value = self.value
                        else:
                            # general case
                            self.check_correctness_line()
                            # check if sequence found
                            for needed_seq in self.results.keys():
                                needed = list(needed_seq)
                                if is_sublist(self.sequence, needed):
                                    self.results[needed_seq] = True

                        # go to next line in log
                        line = fp.readline()
                        self.line_cnt += 1
                        time.sleep(0.1)
        except KeyboardInterrupt:
            print("Bye Bye test, got ctrl+c")
        # except Exception as e:
        #     print("error while parsing log.", e)
        finally:
            if False in self.results.values() or None in self.results.values():
                print("test Failed see results", self.results)
            else:
                print("all good", self.results)
            if q:
                q.put(self.results)

if __name__ == "__main__":
    a = LogParser('my_runner.log.sample')
    a(None)
