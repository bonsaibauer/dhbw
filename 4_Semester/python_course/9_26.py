import numpy as np
import matplotlib.pyplot as plt

# Parameter
Ts = 0.002  # Abtastintervall = 2 ms
Nt = 500    # Anzahl der Abtastpunkte
t = np.arange(0, Nt) * Ts  # Zeitachse von 0 bis 1 Sekunde

# Frequenzen für die Analyse
frequenzen = [1, 5, 5.3, 100, 200, 300]

# Erstellen des Plotfensters
fig, axes = plt.subplots(len(frequenzen), 1, figsize=(10, 12))
fig.suptitle("Kosinusschwingungen bei verschiedenen Frequenzen", fontsize=16)

# Schleife zur Darstellung der Signale
for i, f in enumerate(frequenzen):
    y = np.cos(2 * np.pi * f * t)
    axes[i].plot(t, y)
    axes[i].set_title(f"f = {f} Hz")
    axes[i].grid(True)

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.show()
