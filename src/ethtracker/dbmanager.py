from typing import Tuple, List, Any

from fastapi import Depends
from sqlalchemy import insert, select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.models.models import cryptosamples, CryptoSamples


class DBManager:

    def __init__(self, session):
        self.session = session

    # async def get_one_value(self, aa):
    #     print(aa)

    async def put_one_value(self, time: int, value1: float, value2: float, session: AsyncSession = Depends(get_async_session)):
        one_item = {"interval": 0,
                    "samples": 1,
                    "time_": time,
                    "value_btc": value1,
                    "value_eth": value2}
        stmt = insert(cryptosamples).values(one_item)
        await session.execute(stmt)
        await session.commit()

    async def clearing(self, interval: int, num_samples: int):
        """Clear all data in the given interval-samples
        WITHOUT commit!!!"""
        garbage = delete(cryptosamples).where(cryptosamples.c.interval == interval,
                                              cryptosamples.c.samples == num_samples)
        await self.session.execute(garbage)
        # await self.session.commit()

    async def get_values(self, interval: int, num_samples: int) -> tuple[list[Any], list[Any]]:
        """ return all values in the given interval-samples"""
        # todo: clearing should be there
        query = select(cryptosamples).where(cryptosamples.c.interval == interval,
                                            cryptosamples.c.samples == num_samples)
        result = await self.session.execute(query)
        data = result.all()
        btc = [x[4] for x in data]
        eth = [x[5] for x in data]
        return btc, eth

    async def put_values(self, interval: int, num_samples: int, values1, values2):
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
                await self.clearing(interval, num_samples)  # no commit here
                self.session.add_all(samples_to_add)
                await self.session.commit()
            except Exception as e:
                print(f"Something Error {e}")
        else:
            print("Time errors were")
