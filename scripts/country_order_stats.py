#!/usr/bin/env python

import sqlite3
import pandas as pd

pd.set_option("display.max_columns", None)

TICKET_SALE_START_DATE = "2016-01-01"
DB_FILE = "../../epcon/data/site/p3.db"
TICKET_CODES = (
    "TDDC",
    "TDDP",
    "TDDS",
    "TDSC",
    "TDSP",
    "TDSS",
    "TESC",
    "TESP",
    "TESS",
    "TRSC",
    "TRSP",
    "TRSS",
    "TWDC",
    "TWDP",
    "TWDS",
)

conn = sqlite3.connect(DB_FILE)

c = conn.cursor()

query = c.execute(
    """
SELECT ORDER_ID, COUNTRY_ID
FROM assopy_orderitem, assopy_order
WHERE
assopy_orderitem.order_id == assopy_order.id AND
assopy_orderitem.code IN {codes} AND
assopy_order._complete == 1 AND
assopy_order.created >= date('{date}')""".format(
        codes=str(TICKET_CODES), date=TICKET_SALE_START_DATE
    )
)

countries = query.fetchall()

df = pd.DataFrame(countries, columns=["order_id", "country"])

country_is_none = pd.isnull(df["country"])
df.loc[:, "country"][country_is_none] = "Others"

sums = df.groupby("country").count().sort_values(by="order_id", ascending=False)
sums = sums.reset_index()

for i, row in sums.iterrows():
    print("{},{}".format(row["country"], row["order_id"]))

print("Total: {}.".format(sums["order_id"].sum()))
