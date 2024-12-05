import mne
import numpy as np
import matplotlib.pyplot as plt

# Load the Eyelink raw data
eyelink_file_path = "C:/Users/Usuario/Desktop/Universidad/Sobre BIO295A/sujetos/ET/DToro.asc"
raw_et = mne.io.read_raw_eyelink(eyelink_file_path, create_annotations=True)

# Get events and event_ids from annotations
et_events, et_event_ids = mne.events_from_annotations(raw_et)

# Find pupil data channel
for ch_name in raw_et.ch_names:
    if 'left' in ch_name:
        pupil = 'pupil_left'
    elif 'right' in ch_name:
        pupil = 'pupil_right'

raw_et.pick([pupil])

# Define parameters for epoching
event_id = et_event_ids['10']  # Use event ID for '10'
tmin, tmax = -1, 25  # Epoch from -1 to 15 seconds around event

# Create epochs
epochs = mne.Epochs(raw_et, events=et_events, event_id=event_id, tmin=tmin, tmax=tmax,
                         preload=True, reject= None, reject_by_annotation=False)

# Get data from epochs
epoch_data = epochs.get_data()


# Calculate nan-mean and nan-standard deviation across epochs
mean_time_series = np.nanmean(epoch_data, axis=0).squeeze()  # Average across epochs
std_time_series = np.nanstd(epoch_data, axis=0).squeeze()    # Std dev across epochs

# Create a time array for plotting
time = epochs.times

# Plot mean and standard deviation
plt.figure(figsize=(10, 6))
plt.plot(time, mean_time_series, label='Mean Time Series', color='blue')
plt.fill_between(time, mean_time_series - std_time_series, mean_time_series + std_time_series,
                 color='blue', alpha=0.3, label='±1 Std Dev')
plt.xlabel('Time (s)')
plt.ylabel('Pupil Size')
plt.title('Epoch Mean and Standard Deviation')
plt.legend()
plt.grid(True)
plt.show()