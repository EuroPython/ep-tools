import sqlite3
import pandas as pd

TICKET_SALE_START_DATE = '2016-01-01'

conn = sqlite3.connect('data/site/p3.db')

c = conn.cursor()

query = c.execute("""
SELECT ORDER_ID, COUNTRY_ID
FROM assopy_orderitem, assopy_order
WHERE assopy_orderitem.order_id == assopy_order.id AND 
assopy_order.created >= date(TICKET_SALE_START_DATE)"""")

countries = query.fetchall()

df = pd.DataFrame(countries, columns=['order_id', 'country'])

counts = df.groupby('country').count().sort_values(by='order_id', ascending=False)

print(counts)
