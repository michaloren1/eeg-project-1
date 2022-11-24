import os
import mne
from mne.preprocessing import ICA


def plot_raw(file):
    raw = mne.io.read_raw(file, preload=True)
    # deleting extra channels for development
    raw.pick(["Pz", "Cz", "Fz", "C3", "C4"])
    # chosen electrodes to work on
    raw.plot(duration=4)


def step1(file):  # file- str of file location
    # bandpass- some of the data is not made by the brain, remove it
    raw = mne.io.read_raw(file, preload=True)  # read_raw comes from mne.io
    raw.pick(['Pz', 'Cz', 'Fz', 'C3', 'C4'])
    bandpass_filter(raw)
    rereference(raw)
    print("------------------------")
    print("pick bad channels")
    raw.plot(duration=4)
    return raw
    # the function alters raw and returns the new version


def bandpass_filter(raw):
    raw.filter(l_freq=1, h_freq=40)  # lowest frequency to remove =1, highest = 40 Hz.
    raw.resample(sfreq=250)  # changing the amount of samples per sec to 250 in a calculated way, s for sample.
    freqs = (60, 120, 180, 240)  # freqs to remove
    raw.notch_filter(freqs=freqs, picks="eeg", method='spectrum_fit', filter_length='4s')
    # removing the powerline frequencies that might interrupt- 60 Hz


def rereference(raw):
    raw.set_eeg_reference(ref_channels=['Cz'])


def step2(raw, file):
    inspect_bads(raw)
    ica_analysis(raw)
    epochs = epoching(raw, True) # new eeg file, divided into pieces of the data
    print("---------------------------------")
    print("Pick bad epochs")
    epochs.plot()
    return epochs


def inspect_bads(raw):
    print("---------------------------------") # best practice for console organization
    if len(raw.info['bads']) > 0: # if there's no "bad channel" don't
        raw.pick(picks='eeg', exclude="bads") # choose eeg info except of bad channels
        print("Removed bad channels picked in step one")
    else:
        print("No bad channels picked")


def ica_analysis(raw): # analysing independent components
    # deep learning based function- guesses the outcome, improves itself
    ica = ICA(method="fastica", max_iter="auto")
    ica.fit(raw)  # the computer can change the calculations to fit the pattern better
    return ica.apply(raw)


def epoching(raw, reject): # slicing the data to smaller pieces
    events = mne.make_fixed_length_events(raw, start=5, duration=2.5)
    # takes the data and epoches based on time (every few secs is new event)
    if reject:  # last preprocess, will remove some wave lengths
        reject_criteria = dict(eeg=150e-6)  # 250 µV
        return mne.Epochs(raw, events, reject=reject_criteria, tmin=-0.2, tmax=0.5, preload=True)
    else:
        return mne.Epochs(raw, events, tmin=-0.2, tmax=0.5, preload=True)


def save_processed_epochs(epochs, file):
    processed_file_name = f"Processed - {file.rsplit('/', 1)[-1].split('.')[0]}-epo.fif"
    # not regular string, added argument. this is the new file name
    epochs.save(fname=processed_file_name, overwrite=True)
    # saving the new file with the new name
    os.rename(processed_file_name, f"../data/preprocessed/{processed_file_name}")
