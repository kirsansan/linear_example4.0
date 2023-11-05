from sqlalchemy import MetaData, Column, Table, Integer, Float, String, Time, Double, TIMESTAMP, ForeignKey, JSON

metadata = MetaData()

cryptosamples = Table(
    "cryptosamples",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("symbol", String, nullable=True),
    Column("interval", Integer, nullable=True),
    Column("samples", Integer, nullable=True),
    Column("time_", Integer, nullable=True),
    Column("value", Double, nullable=False),
)


# class CryptoSamples(Base):
#     __tablename__ = 'cryptosamples'
#
#     id = Column(Integer, primary_key=True)
#     symbol = Column(String)
#     interval = Column(Integer)
#     samples = Column(Integer)
#     time_ = Column(Integer)
#     value = Column(Double)

