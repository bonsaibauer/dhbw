import numpy as np
import matplotlib.pyplot as plt

# Parameter
Ts = 0.002  # Abtastintervall = 2 ms
Nt = 500    # Anzahl der Abtastpunkte
Fs = 1 / Ts  # Abtastfrequenz = 500 Hz
t = np.arange(0, Nt) * Ts  # Zeitachse von 0 bis 1 Sekunde

# Frequenzen für die Analyse
frequenzen = [1, 5, 5.3, 100, 200, 300]

# Plot-Gitter: Zeilen = Anzahl der Frequenzen, 2 Spalten (links: Signal, rechts: Spektrum)
fig, axes = plt.subplots(len(frequenzen), 2, figsize=(14, 12))
fig.suptitle("Kosinusschwingungen und deren Fourier-Spektren", fontsize=16)

for i, f in enumerate(frequenzen):
    # Signal im Zeitbereich (Cosinus)
    a = np.cos(2 * np.pi * f * t)

    # Fourier-Transformation
    b = np.fft.fft(a)
    c = np.abs(b)
    d = np.fft.fftshift(c)  # Spektrum zentriert

    freq_axis = np.fft.fftshift(np.fft.fftfreq(Nt, Ts))  # Frequenzachse in Hz

    # Linke Spalte: Zeitbereich
    axes[i, 0].plot(t, a)
    axes[i, 0].set_title(f"Signal: f = {f} Hz")
    axes[i, 0].set_xlabel("Zeit [s]")
    axes[i, 0].grid(True)

    # Rechte Spalte: Frequenzbereich (Amplitude)
    axes[i, 1].plot(freq_axis, d)
    axes[i, 1].set_title("Fourier-Spektrum")
    axes[i, 1].set_xlim(-Fs/2, Fs/2)
    axes[i, 1].set_xlabel("Frequenz [Hz]")
    axes[i, 1].grid(True)

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.show()
