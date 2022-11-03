import os
import mne

def plot_raw(file):
    raw = mne.io.read_raw(file, preload= True)
    # deleting extra channels for development
    raw.pick(["Pz", "Cz", "Fz", "C3", "C4"])
    # chosen electrodes to work on
    raw.plot(duration=4)
