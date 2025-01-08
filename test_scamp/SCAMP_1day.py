from obspy import read
import pyscamp as mp
import numpy as np

Data   = read('./1P.TDPA..HHZ_20190601.mseed')
SR     = Data[0].stats.sampling_rate 
sublen = int(15*SR)

# Self join.
profile, index = mp.selfjoin(Data[0].data*1e8, sublen, threads=32, pearson=True)
cc_suma        = mp.selfjoin_sum(Data[0].data*1e8, sublen, threads=32, threshold=0.7)

np.save('profile_pearson', profile)
np.save('index_pearson', index)
np.save('cc_suma', cc_suma)
