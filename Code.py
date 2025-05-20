import numpy as np
import pandas as pd
from scipy.signal import butter, lfilter, welch

# --- Bandpass filter (to isolate EEG frequency bands) ---
def butter_bandpass(lowcut, highcut, fs, order=4):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    return butter(order, [low, high], btype='band')

def bandpass_filter(data, lowcut, highcut, fs):
    b, a = butter_bandpass(lowcut, highcut, fs)
    return lfilter(b, a, data)

# --- Feature extraction ---
def extract_features(signal, fs=256):
    # Calculate band power
    freqs, psd = welch(signal, fs, nperseg=fs)

    def bandpower(freq_range):
        idx = np.logical_and(freqs >= freq_range[0], freqs <= freq_range[1])
        return np.trapz(psd[idx], freqs[idx])

    return {
        "delta_power": bandpower((0.5, 4)),
        "theta_power": bandpower((4, 8)),
        "alpha_power": bandpower((8, 13)),
        "beta_power": bandpower((13, 30)),
        "gamma_power": bandpower((30, 45)),
    }

# --- Process EEG Data from CSV ---
def process_eeg(csv_path):
    df = pd.read_csv(csv_path)
    fs = 256  # sampling frequency

    signal = df['value'].values
    filtered = bandpass_filter(signal, 0.5, 45, fs)

    features = extract_features(filtered, fs)
    return features

# Example usage
if __name__ == "__main__":
    features = process_eeg("your_simulated_eeg_data.csv")
    print("Extracted Features:", features)
