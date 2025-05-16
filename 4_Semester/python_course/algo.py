import multiprocessing as multiproc
import numpy as np
import soundfile as sf
import pyaudio
import matplotlib.pyplot as plt

def run(value,value2,fig,fileName,saveValue=None):
    data, fs = sf.read(fileName)
    if(data.ndim>1): data=data[:,0]
    
    ts=1/fs
    nt=data.size
    T=nt*ts
    t = np.arange(0, T,ts)
    f= np.arange(-fs/2, fs/2,1/T)

    fig.clf()
    fig.suptitle(fileName+'     fs='+str(fs)+" Hz", fontsize=16)
    ax = fig.add_subplot(2, 1, 1)
    ax.plot(t, data)
    ax = fig.add_subplot(2, 1, 2)
    ax.plot(f,np.fft.fftshift(np.abs(np.fft.fft(data)))/nt)
    fig.canvas.draw()

    multiproc.Process(target=playAudio,args=(data,fs)).start()

def playAudio(dat,samplerate):
    stream = pyaudio.PyAudio().open(format = pyaudio.paFloat32,channels = 1,rate = samplerate,output = True)
    stream.write(dat.astype(np.float32).tobytes())
    stream.close()

if __name__ == '__main__':
    run(10,0,plt.figure(),"flying-mosquito-105770.mp3")
    plt.show()