import numpy as np
import os.path
import scipy.io.wavfile as wavfile
import wavio

def signaltonoise(a, axis=0, ddof=0):
    a = np.asanyarray(a)
    m = a.mean(axis)
    sd = a.std(axis=axis, ddof=ddof)
    return np.where(sd == 0, 0, m/sd)

def snr(file):
	if (os.path.isfile(file)):
		data = wavfile.read(file)[1]
		singleChannel = data
		try:
			singleChannel = np.sum(data, axis=1)
		except:
			# was mono after all
			pass

		norm = singleChannel / (max(np.amax(singleChannel), -1 * np.amin(singleChannel)))
		return signaltonoise(norm)
	else:
		return 'dm'

file = '../Server/uploads/file1302-1540031701069.wav'

temp = snr(file);
print(temp)