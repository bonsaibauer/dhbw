import multiprocessing as multiproc
import numpy as np
import soundfile as sf
import pyaudio
import matplotlib.pyplot as plt

# Algo 1

def run(value, value2, fig, fileName, saveValue=None):
    # Audiodatei lesen
    data, fs = sf.read(fileName)
    if data.ndim > 1:
        data = data[:, 0]  # Nur linken Kanal verwenden, falls Stereo

    ts = 1 / fs
    nt = data.size
    T = nt * ts
    t = np.arange(0, T, ts)
    f = np.linspace(-fs / 2, fs / 2, nt)

    # Mischfrequenz berechnen: value2 ∈ [0, 100] → f_mix ∈ [0, 0.6 * fs]
    f_mix = (value2 / 100.0) * 0.6 * fs
    mixer = np.cos(2 * np.pi * f_mix * t)

    # Modulation: Multiplikation mit Cosinus
    mixed = data * mixer

    # Darstellung
    fig.clf()
    fig.suptitle(f"Mischfrequenz: {f_mix:.2f} Hz", fontsize=16)

    # Eingangssignal – Zeit und Spektrum
    ax1 = fig.add_subplot(2, 2, 1)
    ax1.plot(t, data)
    ax1.set_title("Eingangssignal (Zeit)")

    ax2 = fig.add_subplot(2, 2, 2)
    ax2.plot(f, np.fft.fftshift(np.abs(np.fft.fft(data)))/nt)
    ax2.set_title("Eingangssignal (Spektrum)")

    # Mischergebnis – Zeit und Spektrum
    ax3 = fig.add_subplot(2, 2, 3)
    ax3.plot(t, mixed)
    ax3.set_title("Mischergebnis (Zeit)")

    ax4 = fig.add_subplot(2, 2, 4)
    ax4.plot(f, np.fft.fftshift(np.abs(np.fft.fft(mixed)))/nt)
    ax4.set_title("Mischergebnis (Spektrum)")

    fig.tight_layout()
    fig.canvas.draw()

    # Audio abspielen
    multiproc.Process(target=playAudio, args=(mixed, fs)).start()

def playAudio(dat, samplerate):
    stream = pyaudio.PyAudio().open(format=pyaudio.paFloat32, channels=1, rate=samplerate, output=True)
    stream.write(dat.astype(np.float32).tobytes())
    stream.close()

if __name__ == '__main__':
    run(10, 40, plt.figure(), "flying-mosquito-105770.mp3")
    plt.show()
