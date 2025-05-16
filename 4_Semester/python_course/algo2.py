import multiprocessing as multiproc
import numpy as np
import soundfile as sf
import pyaudio
import matplotlib.pyplot as plt

# Algo 2

def run(value, value2, fig, fileName, saveValue=None):
    # Audiodatei laden
    data, fs = sf.read(fileName)
    if data.ndim > 1:
        data = data[:, 0]

    ts = 1 / fs
    nt = data.size
    T = nt * ts
    t = np.arange(0, T, ts)
    f = np.linspace(-fs / 2, fs / 2, nt)

    # Mischfrequenz berechnen (0 bis 0.6*fs, gesteuert durch value2 ∈ [0, 100])
    f_mix = (value2 / 100.0) * 0.6 * fs
    mixer = np.cos(2 * np.pi * f_mix * t)
    mixed = data * mixer

    # Filterparameter
    M = 40
    N = 81
    i = np.arange(-40, 41)  # 81 Werte von -40 bis 40
    P = max(1, min(28, int(value)))  # P in [1, 28], gesteuert durch 'value'

    # Filterfunktion g[i]
    g = np.exp(-i**2 / (8 * M**2)) * np.sin(2 * np.pi * P * i / N)

    # Filter anwenden durch Faltung
    filtered = np.convolve(mixed, g, mode='same')
    filtered = filtered / np.max(np.abs(filtered))  # Normalisierung

    # Visualisierung
    fig.clf()
    fig.suptitle(f"Mischfrequenz: {f_mix:.2f} Hz, Filter P={P}", fontsize=14)

    ax1 = fig.add_subplot(2, 2, 1)
    ax1.plot(t, data)
    ax1.set_title("Originalsignal (Zeit)")

    ax2 = fig.add_subplot(2, 2, 2)
    ax2.plot(f, np.fft.fftshift(np.abs(np.fft.fft(data)))/nt)
    ax2.set_title("Originalsignal (Spektrum)")

    ax3 = fig.add_subplot(2, 2, 3)
    ax3.plot(t, filtered)
    ax3.set_title("Gefiltertes Mischergebnis (Zeit)")

    ax4 = fig.add_subplot(2, 2, 4)
    ax4.plot(f, np.fft.fftshift(np.abs(np.fft.fft(filtered)))/nt)
    ax4.set_title("Gefiltertes Mischergebnis (Spektrum)")

    fig.tight_layout()
    fig.canvas.draw()

    # Audioausgabe
    multiproc.Process(target=playAudio, args=(filtered, fs)).start()

def playAudio(dat, samplerate):
    stream = pyaudio.PyAudio().open(format=pyaudio.paFloat32, channels=1, rate=samplerate, output=True)
    stream.write(dat.astype(np.float32).tobytes())
    stream.close()

if __name__ == '__main__':
    run(value=10, value2=40, fig=plt.figure(), fileName="flying-mosquito-105770.mp3")
    plt.show()
