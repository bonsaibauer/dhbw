import numpy as np
import matplotlib.pyplot as plt

def run(value, value2, fig, fileName, saveValue=None):
    # Parameter
    Ns = 500              # Abtastpunkte
    Ts = 0.002            # Abtastintervall (2 ms)
    fs = 1 / Ts           # Abtastfrequenz (Hz)
    T = Ns * Ts           # Gesamtdauer

    # Werte von Slidern
    freq = 1 + (66 * value / 100)  # Frequenz zwischen 1–67 Hz
    noise_strength = 10 * value2 / 100  # Rauschstärke 0–10

    # Zeitvektor
    t = np.arange(0, T, Ts)

    # Sinussignal erzeugen
    a1 = np.sin(2 * np.pi * freq * t)

    # Rauschen erzeugen (gleichverteiltes, mittelwertfreies Rauschen)
    noise = (np.random.rand(Ns) - 0.5) * 2 * noise_strength

    # Überlagertes Signal
    signal_noisy = a1 + noise

    # --- Analyse 1: normale FFT
    spectrum = np.abs(np.fft.fft(signal_noisy))
    freqs = np.fft.fftfreq(len(signal_noisy), Ts)
    max_freq_index = np.argmax(spectrum[:len(spectrum)//2])
    estimated_freq = freqs[max_freq_index]

    # --- Analyse 2: Nullpadding
    signal_padded = np.hstack((signal_noisy, np.zeros(9 * Ns)))  # 10x mehr Punkte
    spectrum_padded = np.abs(np.fft.fft(signal_padded))
    freqs_padded = np.fft.fftfreq(len(signal_padded), Ts)

    # --- Analyse 3: Signalverlängerung durch Wiederholung
    signal_extended = np.tile(signal_noisy, 10)
    spectrum_extended = np.abs(np.fft.fft(signal_extended))
    freqs_extended = np.fft.fftfreq(len(signal_extended), Ts)

    # --- Plot
    fig.clf()
    fig.suptitle(f"f = {freq:.1f} Hz, geschätzt = {estimated_freq:.1f} Hz, Rauschstärke = ±{noise_strength:.1f}", fontsize=12)

    ax1 = fig.add_subplot(3, 1, 1)
    ax1.plot(t, signal_noisy)
    ax1.set_title("Noisy Sinus")

    ax2 = fig.add_subplot(3, 1, 2)
    ax2.plot(freqs[:len(freqs)//2], spectrum[:len(spectrum)//2])
    ax2.set_title("Spektrum (original)")

    ax3 = fig.add_subplot(3, 1, 3)
    ax3.plot(freqs_padded[:len(freqs_padded)//2], spectrum_padded[:len(freqs_padded)//2], label="Zero-padding")
    ax3.plot(freqs_extended[:len(freqs_extended)//2], spectrum_extended[:len(freqs_extended)//2], linestyle='dashed', label="Signal verlängert")
    ax3.set_title("Spektren mit höherer Auflösung")
    ax3.legend()

    fig.tight_layout()
    fig.canvas.draw()

