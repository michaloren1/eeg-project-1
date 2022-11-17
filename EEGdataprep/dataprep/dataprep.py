import os
import mne


def plot_raw(file):
    raw = mne.io.read_raw(file, preload=True)
    # deleting extra channels for development
    raw.pick(["Pz", "Cz", "Fz", "C3", "C4"])
    # chosen electrodes to work on
    raw.plot(duration=4)


def step1(file): # file- str of file location
    # bandpass- some of the data is not made by the brain, remove it
    raw = mne.io.read_raw(file, preload= True) # read_raw comes from mne.io
    raw.pick(['Pz', 'Cz', 'Fz', 'C3', 'C4'])
    bandpass_filter(raw)
    rereference(raw)
    print("------------------------")
    print("pick bad channels")
    raw.plot(duration=4)
    return raw
    # the function alters raw and returns the new version


def bandpass_filter(raw):
    raw.filter(l_freq = 1, h_freq = 40) # lowest frequency to remove =1, highest = 40 Hz.
    raw.resample(sfreq = 250) # changing the amount of samples per sec to 250 in a calculated way, s for sample.
    freqs = (60, 120, 180, 240) # freqs to remove
    raw.notch_filter(freqs=freqs, picks= "eeg", method= 'spectrum_fit', filter_length='4s')
    # removing the powerline frequencies that might interrupt- 60 Hz


def rereference(raw):
    raw.set_eeg_reference(ref_channels=['Cz'])


