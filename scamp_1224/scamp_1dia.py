from obspy import read
import pyscamp as mp
import numpy as np

Data   = read('C1.MT12.HHZ.2017.358.mseed')
SR     = Data[0].stats.sampling_rate 
sublen = int(11*SR) # Intervalos de 11 segundos

# Self join (comparación todo con todo)
profile, index = mp.selfjoin(Data[0].data*1e8, sublen, threads=32, pearson=True)        # Matrix profile, index de MP
cc_suma        = mp.selfjoin_sum(Data[0].data*1e8, sublen, threads=32, threshold=0.7)   # Cuántas veces una subsecuencia tiene correlación alta con otras subsecuencias

np.save('profile_pearson', profile)
np.save('index_pearson', index)
np.save('cc_suma', cc_suma)