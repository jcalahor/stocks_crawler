from configparser import ConfigParser
import logging.config
from db import Db

import logging
import os
from parser_util import Parser
import datetime

class StockSnapshot(object):
    def __init__(self):
        self.date = None
        self.symbol = None
        self.price = None
        self.recommendation = None
        self.fair_value_status = None
        self.short_term = None
        self.mid_term = None
        self.long_term = None


def process_file(logger, db, symbol, f):
    def parse_file():
        def get_term_strategy(color_code):
            if color_code == '1ac567': # green
                return 1
            if color_code == 'ff4d52': #red
                return 2
            return 3  # black

        try:

            p = Parser(html)

            if (not p.move_to('Quote Lookup')):
                return None
            price = p.extract_between('data-reactid="52">', '</span>')
            if not price:
                return None
            if (not p.move_to('Analyst Recommendation')):
                return None
            if (not p.move_to('Fz(14px)')):
                return None
            recommendation = p.extract_between('>', '<')
            if not recommendation:
                return None
            if (not p.move_to('>Fair Value</div>')):
                return None
            if (not p.move_to('Fz(12px)')):
                return None
            if (not p.move_to('Fz(12px)')):
                return None
            fair_value_status = p.extract_between('>', '<')
            if (not p.move_to('stroke:')):
                return None
            short_term_color_code = p.extract_between('#', ';')
            if (not p.move_to('stroke:')):
                return None
            mid_term_color_code = p.extract_between('#', ';')
            if (not p.move_to('stroke:')):
                return None
            long_term_color_code =  p.extract_between('#', ';')

            ssp = StockSnapshot()
            ssp.symbol = symbol
            ssp.date = datetime.datetime.now()
            ssp.price = float(price)
            ssp.recommendation = recommendation
            ssp.fair_value_status = fair_value_status
            ssp.short_term = get_term_strategy(short_term_color_code)
            ssp.mid_term = get_term_strategy(mid_term_color_code)
            ssp.long_term = get_term_strategy(long_term_color_code)
            return ssp
        except Exception as e:
            logger.info("cannot process file {0}: {1}".format(f, symbol))
            logger.error(e)
            return None

    with open(f, "r") as myfile:
        logger.info('processing file: {0}'.format(f))
        html = myfile.read()
        ssp = parse_file()
        if ssp:
            db.start_cursor()
            db.store_stock_snapshot(ssp)
            db.terminate_cursor()



def run():
    logger = None
    try:
        parser = ConfigParser()
        logging.config.fileConfig('snapshot_uploader.cfg')
        logger = logging.getLogger('basic')
        parser.read('snapshot_uploader.cfg')
        logger.info("Starting uploading  process...")

        connection_string = parser.get('Db', 'connection_string')

        db_obj = Db(connection_string, logger)
        db_obj.open()

        path = 'C:\\crawler_output'
        files = []
        for r, d, f in os.walk(path):
            for file in f:
                files.append((file.replace('.html', ''), os.path.join(r, file)))

        for symbol, file in files:
            process_file(logger, db_obj, symbol, file)

        db_obj.close()
        logger.info("Ending")
    except Exception as e:
        logger.exception("Error while generating ...")


if __name__ == '__main__':
    run()
