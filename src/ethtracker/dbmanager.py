from sqlalchemy import insert

from src.models.models import cryptosamples, CryptoSamples


class DBManager:

    def __init__(self, session):
        self.session = session

    def put_one_value(self):
        stmt = insert(cryptosamples).values(dict)
        await self.session.execute(stmt)
        await self.session.commit()

    def put_values(self, symbol, interval, samples, values):
        list_with_data_for_write = []
        for one_value in values:
            list_with_data_for_write.append(
                CryptoSamples(symbol=symbol, interval=interval, samples=samples, values=one_value))
        self.session.add_all(list_with_data_for_write)
        self.session.commit()
        # self.session.close()

    def get_values(self, aa):
        print(aa)