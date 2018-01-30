#!/usr/bin/python3

from runforever import RunForever
import random
import sys
import logging


class MyRunner(RunForever):
    LOGGING_TRUE_STR = 'True'
    LOGGING_FALSE_STR = ''
    LOGGING_FILENAME = 'my_runner.log'
    LOGGING_FORMAT = '%(created)f|%(message)s|%(levelname)s|%(asctime)s'

    def __init__(self):
        logging.basicConfig(filename=MyRunner.LOGGING_FILENAME,
                            level=logging.INFO, filemode='w',
                            format=MyRunner.LOGGING_FORMAT)
        super(MyRunner, self).__init__()

    def run(self):
        r = random.random()
        if r > 0.85:
            logging.info(MyRunner.LOGGING_TRUE_STR)
            return True
        logging.info(MyRunner.LOGGING_FALSE_STR)
        return False

    # altered for logging purpose.
    def cant_stop_me_now(self):
        try:
            super(MyRunner, self).cant_stop_me_now()
        except KeyboardInterrupt:
            logging.info("Bye Bye, got ctrl+c")
        except Exception as e:
            logging.error("Exception occured while running: "+str(e))


if __name__ == "__main__":
    a = MyRunner()
    a.cant_stop_me_now()
