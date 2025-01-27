from obspy import read
import pyscamp as mp
import numpy as np

Data   = read('C1.MT12.HH*.2017.204-210.mseed')
SR     = Data[0].stats.sampling_rate 
sublen = int(11*SR)

# abjoin (comparación todo con todo)
profile, index = mp.abjoin(Data[0].data*1e8, -Data[0].data*1e8, sublen, threads=32, pearson=True)

np.save('profile_pearson', profile)
np.save('index_pearson', index)
