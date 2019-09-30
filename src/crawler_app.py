from configparser import ConfigParser
import logging.config
from db import Db
from web import web_request
import multiprocessing
import logging
from logging.handlers import QueueHandler, QueueListener
import time
import random

class LogDescriptor(object):
    is_started = False

def download_page(stock_symbol):
    def start_log():
        log_filename = '{0}_worker.log'.format(multiprocessing.current_process().name)

        # Set up a specific logger with our desired output level
        logger = logging.getLogger('Process Worker')
        logger.setLevel(logging.DEBUG)

        # Add the log message handler to the logger
        handler = logging.handlers.RotatingFileHandler(
            log_filename, maxBytes=999999999, backupCount=5)

        logger.addHandler(handler)
        LogDescriptor.logger = logger
        LogDescriptor.is_started = True

    try:
        if not LogDescriptor.is_started:
            start_log()

        LogDescriptor.logger.info('Processing: {0}'.format(stock_symbol.symbol))
        html = web_request(LogDescriptor.logger,
                           'https://finance.yahoo.com/quote/{0}?p={0}&.tsrc=fin-srch'.format(stock_symbol.symbol))
        with open('C:\\crawler_output\\' + stock_symbol.symbol + '.html', 'w') as f:
            f.write(html)
            f.close()
    except Exception as e:
        LogDescriptor.logger.info('error:')
        LogDescriptor.logger.info(stock_symbol.symbol)
        LogDescriptor.logger.exception(e)


def run():
    logger = None
    try:
        parser = ConfigParser()
        logging.config.fileConfig('crawler_app.cfg')
        logger = logging.getLogger('basic')
        parser.read('crawler_app.cfg')
        logger.info("Starting crawling process...")

        connection_string = parser.get('Db', 'connection_string')

        db_obj = Db(connection_string, logger)
        db_obj.open()

        stock_symbols = db_obj.get_symbols()
        p = multiprocessing.Pool(2)
        p.map(download_page, stock_symbols)

        db_obj.close()
        logger.info("Ending")
    except Exception as e:
        logger.exception("Error while generating ...")


if __name__ == '__main__':
    run()
