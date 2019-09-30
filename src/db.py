import pyodbc
from stock_symbol import StockSymbol

class Db(object):
    def __init__(self, connection_string, logger):
        self.connection_string = connection_string
        self.logger = logger
        self.cursor = None

    def open(self):
        self.connection = pyodbc.connect(self.connection_string)

    def close(self):
        self.connection.close()

    def start_cursor(self):
        self.cursor = self.connection.cursor()

    def get_symbols(self):
        entities = []

        def read(row):
            entity = StockSymbol(row[0])
            entities.append(entity)

        try:
            cursor = self.connection.cursor()
            cursor.execute('select * from [dbo].[Symbols]', [])
            rows = cursor.fetchall()
            list(map(read, rows))
            cursor.close()
            return entities
        except Exception as e:
            self.logger.error("error while getting entities...")
            self.logger.error(e)
            raise

    def store_stock_snapshot(self, ssp):
        try:
            sql = """
                execute dbo.StoreSnapshot 
    				@Date = ?,
    				@Symbol = ?,
    				@Price = ?,
    				@Recommendation = ?,
    				@FairValueStatus  = ?,
    				@ShortTerm = ?,
    				@MidTerm = ?,
    				@LongTerm = ?
            """
            params = (ssp.date,
                      ssp.symbol,
                      ssp.price,
                      ssp.recommendation,
                      ssp.fair_value_status,
                      ssp.short_term,
                      ssp.mid_term,
                      ssp.long_term)
            self.cursor.execute(sql, params)
        except Exception as e:
            self.logger.error("error while storing... {0}".format(ssp.symbol))
            self.logger.error(e)

    def terminate_cursor(self):
        self.cursor.commit()
        self.cursor.close()

    def store_single(self, entity):
        self.start_cursor()
        self.store_entity(entity)
        self.terminate_cursor()

    def delete_single(self, entity):
        self.start_cursor()
        self.delete_entity(entity)
        self.terminate_cursor()