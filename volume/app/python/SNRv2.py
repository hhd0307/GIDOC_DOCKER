import sys
import numpy as np
import os.path as path
import soundfile as sf
import math
from scipy.signal import lfilter
from scipy.signal import butter
def VUS(x=None, SR=None, inbkpts = None, instate = None):
    outbkpts = 0;
    outstate = 0;
    T = 0;

    x_N = len(x)
    F = 3
    f = np.zeros((x_N, F))
    g = np.zeros((x_N, F))

    ma  = computeMA(x, SR);
    zcr = computeZCR(x, SR);
    lf  = computeLF(x, SR);
    f[:,0] = np.reshape(ma, (1, len(ma)));
    f[:,1] = np.reshape(zcr, (1, len(zcr)));
    f[:,2] = np.reshape(lf, (1, len(lf)));
    if type(instate) != type(None):
        if len(instate) != len(inbkpts) - 1:
            print('length(instate) ~= length(inbkpts)-1');
            return
        V_n = np.array([]); V_n = np.reshape(V_n, (len(V_n),1));
        U_n = np.array([]); U_n = np.reshape(U_n, (len(U_n),1));
        S_n = np.array([]); S_n = np.reshape(S_n, (len(S_n),1))

        for i in range(len(instate)):
            n = np.arange(inbkpts[i],inbkpts[i + 1]);
            n = np.reshape(n, (len(n),1))
            __switch__ = instate[i]
            if   __switch__ == 1:
                V_n = np.concatenate((V_n, n), axis=0)
            elif __switch__ == 2:
                U_n = np.concatenate((U_n, n), axis=0)
            elif __switch__ == 3:
                S_n = np.concatenate((S_n, n), axis=0)

        V_n = V_n.astype(int);
        U_n = U_n.astype(int);
        S_n = S_n.astype(int);

        T = np.zeros((4,1))

        union = np.union1d(U_n, V_n) + 1;
        union = np.reshape(union, (len(union), 1))
        f1 = f[S_n, 0];
        f2 = f[union - 1, 0];
        f2 = np.reshape(f2, (len(f2), 1));
        T[0,:] = threshold(f1, f2);

        for i in range(0,F):
        	f1 = f[U_n, i];
        	f2 = f[V_n, i];
        	T[i + 1] = threshold(f1 , f2);
    else:
    	T = inbkpts;

    for i in range(F):
    	g[:, i] = normalise(f[:, i], T[i+1])
    	if i == 1:
    		g[:, i] = -g[:, i];
    # Speech/Silence
    SS = computeSTA(f[:, 0] > T[0,0], SR) > .5
    # Voiced/Unvoiced
    sumG= np.sum(g, axis = 1)
    VU = computeSTA(sumG > 0, SR) > .5

    # print(SS[:10])
    notVU = np.logical_not(VU);
    notSS = np.logical_not(SS);

    S = np.zeros((x_N, 1))
    S[VU] = 1
    S[notVU] = 2
    S[notSS] = 3

    diffArr = np.diff(np.reshape(S, len(S)))
    # print(diffArr[:10])
    diffInd = np.where(diffArr != 0)
    diffInd =np.array(diffInd)
    # print(diffInd.shape[1])
    # print(diffInd[:10])

    zero = np.array([0]);
    x_N_1 = np.array([x_N - 1]);
    diffInd = np.reshape(diffInd, diffInd.shape[1])

    # print(diffInd.shape)
    # print(zero.shape)
    # print(x_N_1.shape)
    outbkpts = np.concatenate((zero, diffInd, x_N_1), axis=0)
    outstate = S[outbkpts[0:-1] + 1]
    outbkpts = np.reshape(outbkpts, (len(outbkpts),1))
    return outbkpts, outstate, T
def computeMA(x=None, SR=None): #Done
    N = math.floor(20e-3 * SR);
    zerosArray = np.zeros((int(N/2), 1));
    x_pad = np.concatenate((x, zerosArray), axis=0)
    onesArray = np.ones(N);
    absArray = np.abs(x_pad);
    absArray = np.reshape(absArray, len(absArray));
    MA = lfilter(onesArray, 1, absArray);
    MA = MA[int(N/2):];
    return MA
def computeSTA(x=None, SR=None):
    N = math.floor(20e-3 * SR)

    onesArray = np.ones(N);
    zerosArray = np.zeros(int(N/2));
    appendAr = np.concatenate((x, zerosArray));
    
    STA = lfilter(1/N*onesArray, 1, appendAr)
    
    STA = STA[int(N/2):]
    return STA;
def computeLF(x=None, SR=None): #Done
    cutoff = 1000
    Wn = cutoff * 2 / SR
    [B, A] = butter(5, Wn);

    x =np.reshape(x, (len(x)))
    xlp = lfilter(B, A, x)

    x =np.reshape(x, (len(x),1))
    xlp =np.reshape(xlp, (len(xlp),1))

    LF = computeSTE(xlp, SR) / computeSTE(x, SR)
    return LF
def computeZCR(x=None, SR=None): #Done
    N = math.floor(20e-3 * SR)
    zerosArray = np.zeros((int(N/2), 1));
    x_pad = np.concatenate((x, zerosArray), axis = 0)
    multi = x_pad[:-1] * x_pad[1:] < 0;
    onlyFalse = np.reshape(np.array([False]),(1,1))
    z = np.concatenate((onlyFalse, multi), axis = 0);
    onesArray = np.ones(N);
    z = 1*z;
    z = np.reshape(z, (1,len(z)))
    ZCR = lfilter(onesArray, 1, z);
    ZCR = np.reshape(ZCR, ZCR.shape[1]);
    ZCR = ZCR[int(N/2):]
    ZCR = np.reshape(ZCR, len(ZCR));
    return ZCR
def threshold(f=None, g=None,fig=None): #Done
	if type(fig) == type(None):
		fig = False;
	T_min = np.max(np.array([np.min(f), np.min(g)]));
	T_max = np.min(np.array([np.max(f), np.max(g)]));
	f = np.sort(f[f > T_min]);
	g = np.sort(g[g < T_max]);
	T = (T_min + T_max) / 2;
	m = len(np.where(f < T));
	p = len(np.where(g > T));
	n = -1;
	q = -1;
	N_f = len(f);
	N_g = len(g);
	while not (m == n and p == q):
		if 1/N_f*np.sum(f[f>T]-T) > 1/N_g*np.sum(T-g[g < T]):
			T_min = T
		else:
			T_max = T
		T = (T_min + T_max)/2;
		n = m;
		q = p;
		m = np.sum(f < T);
		p = np.sum(g > T)
	return T;
def normalise(x=None, T=None): #Done
    n_pos = np.where(x >= T)
    n_neg = np.where(x < T)
    maxX = np.max(x)
    minX = np.min(x)
    f = np.zeros(len(x));
    f[n_pos] = (x[n_pos] - T) / (maxX - T)
    f[n_neg] = (x[n_neg] - T) / (T - minX)
    return f
def computeSTE(x=None, SR=None): #Done
    N = math.floor(20e-3 * SR);
    zerosArray = np.zeros((int(N/2), 1));
    x_pad = np.concatenate((x, zerosArray), axis=0)
    onesArray = np.ones(N);
    powerArray = np.power(x_pad, 2);
    powerArray = np.reshape(powerArray, len(powerArray))
    STE = lfilter(onesArray, 1, powerArray);
    return STE[int(N/2):]

def snr(s,r):
	if len(s) == len(r):
		Ps = (s.T @ s)/len(s);
		Pn = (r.T @ r)/len(s);
		snr = 10 * math.log10((Ps-Pn)/Pn);
	else:
		snr = 0;
	return snr


if __name__ == '__main__':
    T = np.zeros((4,1));

    if path.exists('./python/result.out'):
    	file = open('./python/result.out', 'r')
    	T = np.zeros((4,1));
    	for i in range(4):
    		line = file.readline();
    		while (line[len(line)-1] == '\n') or (line[len(line)-1] == '\r'):
    			line = line[0:len(line)-1]
    		T[i] = float(line)
    else:
    	inbkpts = np.array([0, 47622, 53747, 59649, 65784, 74414, 75422, 76133, 84779, 85925, 90810, 99030, 110146]);
    	instate = np.array([3, 2, 1, 2, 1, 3, 2, 1, 3, 2, 1, 3]);
    	x, SR = sf.read('./python/training.wav')
    	x = np.reshape(x , (x.shape[0],1))
    	outbkpts, outstate, T = VUS(x,SR,inbkpts,instate);
    	np.savetxt('./python/result.out', T)

    if (path.isfile(sys.argv[1])):
        rs = "";
        for i in range(1,2):
            file = sys.argv[i];
            # print(file)   
            y, SR = sf.read(file);
            try:
                y = np.reshape(y[:,0] , (y.shape[0],1));
            except IndexError:
                y = np.reshape(y , (y.shape[0],1));

            SNR = 0;
            try:
                outbkpts, outstate, T = VUS(y,SR,T);
                S = np.zeros(len(y));
                for j in range(len(outbkpts) - 1):
                    n = np.arange(outbkpts[j],outbkpts[j+1]-1);
                    S[n] = outstate[j];
                slient  = y[S==3];
                if (len(slient) != 0):
                    ntimes = math.ceil(len(y) / len(slient));
                    r = np.tile(np.reshape(slient, len(slient)), ntimes);
                    r = r[:len(y)];
                    r = np.reshape(r, (len(r),1));
                    SNR = snr(y,r);
            except:
                SNR = 0;
            rs = rs + ("\"file%s\":{\"snr\": %.2f,\"rate\": %s,\"dr\": %.2f}," %(i,float(SNR), SR, (len(y)/SR)));
        print("{\"status\":true,\"message\":"+"{"+rs[0:len(rs)-1]+"}"+"}");
    else:
        print("{\"status\": false, \"message\": null}")

sys.stdout.flush()
