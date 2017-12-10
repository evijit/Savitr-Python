import pandas as pd
import time


start = time.time()

df = pd.read_csv('data/tweets.csv')

# print df.iloc[0]

end = time.time()

print 'Time taken', end - start, 's'