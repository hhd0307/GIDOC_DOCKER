import sys
import wave
import contextlib
import numpy as np
import os.path
import scipy.io.wavfile as wavfile

def signaltonoise(a, axis=0, ddof=0):
    a = np.asanyarray(a)
    m = a.mean(axis)
    sd = a.std(axis=axis, ddof=ddof)
    return np.where(sd == 0, 0, m/sd)

def snr(file):
	data = wavfile.read(file)[1]
	singleChannel = data
	try:
		singleChannel = np.sum(data, axis=1)
	except:
		# was mono after all
		pass

	norm = singleChannel / (max(np.amax(singleChannel), -1 * np.amin(singleChannel)))
	return signaltonoise(norm)

def rate(file):
	with contextlib.closing(wave.open(file, 'r')) as f:
	    frames = f.getnframes()
	    rate = f.getframerate()
	    duration = frames / float(rate)
	    return rate, int(duration*1000)

if (os.path.isfile(sys.argv[1])) and (os.path.isfile(sys.argv[2])) and (os.path.isfile(sys.argv[3])):
	snr1 = snr(sys.argv[1])
	# print(snr1)
	rate1, dr1 =rate(sys.argv[1])
	
	snr2 = snr(sys.argv[2])
	# print(snr2)
	rate2, dr2 =rate(sys.argv[2])

	snr3 = snr(sys.argv[3])
	# print("  %s" %(float(snr3)))
	rate3, dr3 =rate(sys.argv[3])

	print("{\"status\":true,\"message\":{ \"file1\":{\"snr\": %s,\"rate\": %s,\"dr\": %s}, \"file2\":{\"snr\": %s,\"rate\": %s,\"dr\": %s}, \"file3\":{\"snr\": %s,\"rate\": %s,\"dr\": %s} } }" %(float(snr1), rate1, dr1, float(snr2), rate2, dr2, float(snr3), rate3, dr3))
else:
	print("{\"status\": false, \"message\": null}")

sys.stdout.flush()

# audio\file1424-1542116667062.wav

# audio\file2608-1542116667082.wav

# audio\file3615-1542116667100.wav

# python .\onlyCode\SNR.py .\audio\file3615-1542116667100.wav .\audio\file2608-1542116667082.wav .\audio\file1424-1542116667062.wav