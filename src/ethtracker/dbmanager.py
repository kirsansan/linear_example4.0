from typing import Tuple, List, Any

from fastapi import Depends
from sqlalchemy import insert, select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from src.database import get_async_session, engine_a, engine_s
from src.models.models import cryptosamples, CryptoSamples


class DBManager:

    def __init__(self):
        self.session = None

    # async def get_one_value(self, aa):
    #       print(aa)

    def open_local_session(self):
        session_maker = sessionmaker(autocommit=False, autoflush=False, bind=engine_s)
        session = session_maker()
        # print("s_process sess", session_maker)
        # print("db", session)
        self.session = session
        return session

    def close_local_session(self):
        self.session.close()

    async def put_one_value(self, time: int, value1: float, value2: float):
        try:
            session = self.open_local_session()
            one_item = {"interval": 0,
                        "samples": 1,
                        "time_": time,
                        "value_btc": value1,
                        "value_eth": value2}
            stmt = insert(cryptosamples).values(one_item)
            session.execute(stmt)
            session.commit()
            session.close()
        except Exception as e:
            print(f"Error writing current value. {e}")

    async def clear_all_for_interval(self, interval: int, num_samples: int):
        """Clear all data in the given interval-samples
        WITHOUT commit!!!"""
        garbage = delete(cryptosamples).where(cryptosamples.c.interval == interval,
                                              cryptosamples.c.samples == num_samples)
        await self.session.execute(garbage)
        # await self.session.commit()

    async def get_values(self, interval: int, num_samples: int) -> tuple[list[Any], list[Any]] | tuple[None, None]:
        """ return all values in the given interval-samples"""
        query = select(cryptosamples).where(cryptosamples.c.interval == interval,
                                            cryptosamples.c.samples == num_samples)
        try:
            session = self.open_local_session()
            result = await self.session.execute(query)
            data = result.all()
            self.close_local_session()
            btc = [x[4] for x in data]
            eth = [x[5] for x in data]
            return btc, eth
        except Exception as e:
            print(f"Error reading values. {e}")
            return None, None

    async def put_values_dataframe(self, interval: int, num_samples: int, values1, values2):
        """ Put into BASE values in the given interval-samples with checking length of values
        also clearing all old values in the given interval-samples
        Unfortunately values1, values2 are DataFrame yet"""

        error_with_time = False
        constant_values = {"interval": interval,
                           "samples": num_samples}
        # but we need to restyle out pandas and checking time
        i1 = values1.index.tolist()
        v1 = values1.values.tolist()
        i2 = values2.index.tolist()
        v2 = values2.values.tolist()
        if len(i1) == len(i2):
            for n in range(len(i1)):
                t1 = int(i1[n][:-3])
                t2 = int(i2[n][:-3])
                if abs(t1 - t2) > 5:
                    error_with_time = True
                    break
                i1[n] = t1
        else:
            print("Different length of data samples")
        if not error_with_time:

            samples_to_add = [CryptoSamples(time_=i1[n],
                                            value_btc=v1[n][3],
                                            value_eth=v2[n][3],
                                            **constant_values) for n in range(len(i1))]
            try:
                await self.clear_all_for_interval(interval, num_samples)  # no commit here
                self.session.add_all(samples_to_add)
                await self.session.commit()
            except Exception as e:
                print(f"Something Error {e}")
        else:
            print("Time errors were")
