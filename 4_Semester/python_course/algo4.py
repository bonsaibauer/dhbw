import multiprocessing as multiproc
import numpy as np
import soundfile as sf
import pyaudio
import matplotlib.pyplot as plt

def run(value, value2, fig, fileName, saveValue=None):
    data, fs = sf.read(fileName)
    if data.ndim > 1:
        data = data[:, 0]

    ts = 1 / fs
    nt = data.size
    T = nt * ts
    t = np.arange(0, T, ts)
    f = np.arange(-fs / 2, fs / 2, 1 / T)

    # --- SPEKTRUM-BASIERTER MISCHER ---
    spektrum = np.fft.fft(data)
    pos = spektrum[:nt//2 + 1]  # nur positive Frequenzen

    # Verschiebung berechnen (value ∈ 0–100 → 0 bis nt//2)
    shift = int((value / 100.0) * (nt // 2))

    # 0en voranstellen und abschneiden, damit die Länge konstant bleibt
    pos_shifted = np.concatenate((np.zeros(shift, dtype=complex), pos))[:nt//2 + 1]

    # Negative Frequenzen ergänzen (Hermitesymmetrie)
    neg = np.conj(np.flip(pos_shifted[1:-1]))  # DC und Nyquist nicht doppelt
    spektrum_neu = np.concatenate((pos_shifted, neg))

    # Rücktransformation
    data_neu = np.fft.ifft(spektrum_neu).real  # Reell, da symmetrisch

    # --- PLOTDARSTELLUNG ---
    fig.clf()
    fig.suptitle(fileName + f'     fs={fs} Hz     shift={shift}', fontsize=16)

    ax = fig.add_subplot(2, 1, 1)
    ax.plot(t, data_neu)
    ax.set_title("Gemischtes Signal (Zeit)")

    ax = fig.add_subplot(2, 1, 2)
    ax.plot(f, np.fft.fftshift(np.abs(np.fft.fft(data_neu))) / nt)
    ax.set_title("Gemischtes Signal (Spektrum)")

    fig.canvas.draw()

    multiproc.Process(target=playAudio, args=(data_neu, fs)).start()

def playAudio(dat, samplerate):
    stream = pyaudio.PyAudio().open(format=pyaudio.paFloat32, channels=1, rate=samplerate, output=True)
    stream.write(dat.astype(np.float32).tobytes())
    stream.close()

if __name__ == '__main__':
    run(50, 0, plt.figure(), "flying-mosquito-105770.mp3")
    plt.show()
