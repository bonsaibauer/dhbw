import numpy as np
import matplotlib.pyplot as plt

def run(value, value2, fig, a=None, b=None):
    fig.clf()               # Löscht das aktuelle Figure-Objekt (damit beim erneuten Aufruf keine alten Plots übrig bleiben)
    fig.tight_layout()      # Optimiert das Layout, damit sich die Subplots nicht überlappen

    # === Parameter definieren ===
    T_s = 0.002             # Abtastzeit (Sampling-Intervall) = 2 ms = 0.002 Sekunden
    f_s = 1 / T_s           # Abtastfrequenz fs = 500 Hz
    N_T = 500               # Anzahl der Abtastpunkte
    t = np.arange(N_T) * T_s  # Zeitachse: 0, T_s, 2*T_s, ..., (N_T-1)*T_s

    # === Umrechnung der Eingabewerte in Frequenzen im Bereich 0 bis 0.625 * fs ===
    # Die Werte 'value' und 'value2' sollen z. B. von 0–100 skaliert werden
    freq1 = value / 100 * 0.625 * f_s     # Frequenz 1 für erste Kosinusschwingung
    freq2 = value2 / 100 * 0.625 * f_s    # Frequenz 2 für zweite Kosinusschwingung

    # === Erzeuge Kosinusschwingungen mit den jeweiligen Frequenzen ===
    x1 = np.cos(2 * np.pi * freq1 * t)    # Erste Schwingung
    x2 = np.cos(2 * np.pi * freq2 * t)    # Zweite Schwingung

    # === Mischen durch elementweise Multiplikation ===
    mixed = x1 * x2                       # Multiplikation beider Signale

    # === Funktion zur Berechnung des Betrags der FFT mit verschobener Achse ===
    def compute_fft(x):
        fft_vals = np.fft.fftshift(np.fft.fft(x))         # FFT berechnen und Nullfrequenz in die Mitte verschieben
        freqs = np.fft.fftshift(np.fft.fftfreq(N_T, T_s))  # Frequenzachse erzeugen, ebenfalls verschoben
        magnitude = np.abs(fft_vals)                      # Betragsspektrum
        return freqs, magnitude

    # === Berechnung der Spektren ===
    f1, mag1 = compute_fft(x1)
    f2, mag2 = compute_fft(x2)
    f_mixed, mag_mixed = compute_fft(mixed)

    # === Plot der Zeitverläufe ===
    ax1 = fig.add_subplot(3, 2, 1)
    ax1.plot(t, x1)
    ax1.set_title(f"x1: f = {freq1:.1f} Hz")  # Anzeige der verwendeten Frequenz
    ax1.set_ylabel("Amplitude")

    ax2 = fig.add_subplot(3, 2, 3)
    ax2.plot(t, x2)
    ax2.set_title(f"x2: f = {freq2:.1f} Hz")
    ax2.set_ylabel("Amplitude")

    ax3 = fig.add_subplot(3, 2, 5)
    ax3.plot(t, mixed)
    ax3.set_title("Mischung x1 * x2")
    ax3.set_xlabel("Zeit [s]")
    ax3.set_ylabel("Amplitude")

    # === Plot der Frequenzspektren (Betragsdarstellung von -fs/2 bis fs/2) ===
    ax4 = fig.add_subplot(3, 2, 2)
    ax4.plot(f1, mag1)
    ax4.set_xlim([-f_s/2, f_s/2])  # Frequenzachse zentriert um 0
    ax4.set_title("Spektrum von x1")
    ax4.set_ylabel("|X(f)|")

    ax5 = fig.add_subplot(3, 2, 4)
    ax5.plot(f2, mag2)
    ax5.set_xlim([-f_s/2, f_s/2])
    ax5.set_title("Spektrum von x2")
    ax5.set_ylabel("|X(f)|")

    ax6 = fig.add_subplot(3, 2, 6)
    ax6.plot(f_mixed, mag_mixed)
    ax6.set_xlim([-f_s/2, f_s/2])
    ax6.set_title("Spektrum der Mischung")
    ax6.set_xlabel("Frequenz [Hz]")
    ax6.set_ylabel("|X(f)|")

    # Gesamtüberschrift des Plots mit den eingegebenen Werten
    fig.suptitle("Test: value = {}, value2 = {}".format(value, value2))

    fig.canvas.draw()  # Aktualisiere das Figure-Fenster

# === Testlauf im Hauptprogramm ===
if __name__ == '__main__':
    run(40, 30, plt.figure(figsize=(12, 8)))  # Beispiel: value = 40, value2 = 30
    plt.show()  # Zeige die gesamte Abbildung


    