```
%% Teil 1 - Filtering an EEG Signal

% Load EEG dataset
load('sampleEEGData.mat'); % Loads EEG structure with fields 'data' and 'srate'
fs = EEG.srate;            % Sampling rate in Hz
fprintf('Sampling rate: %d Hz\n', fs);

% Extract one EEG channel (e.g., channel 1)
eeg_signal = EEG.data(1,:);           % 1D signal vector of selected channel
t = (0:length(eeg_signal)-1) / fs;    % Time vector in seconds

% Design FIR bandpass filter for alpha band (8-13 Hz)
filt_order = 100;
fir_coeff = fir1(filt_order, [8 13]/(fs/2), 'bandpass');
eeg_fir = filtfilt(fir_coeff, 1, eeg_signal);

% Design IIR (Butterworth) bandpass filter for alpha band
[iir_b, iir_a] = butter(3, [8 13]/(fs/2), 'bandpass');
eeg_iir = filtfilt(iir_b, iir_a, eeg_signal);

% Define EEG frequency bands and descriptive labels
band_ranges = [
    0.5 4;    % Delta
    4 8;      % Theta
    8 13;     % Alpha
    13 30     % Beta
];
band_labels = {
    'Delta (Tiefschlaf)';
    'Theta (leichter Schlaf)';
    'Alpha (wach, entspannt)';
    'Beta (wach, aktiv)';
};
num_bands = size(band_ranges, 1);

% Function to compute relative band power
compute_relative_power = @(signal) ...
    arrayfun(@(i) bandpower(signal, fs, band_ranges(i,:)), 1:num_bands);

% Compute power only for RAW signal (valid!)
raw_power = compute_relative_power(eeg_signal);
raw_relative = raw_power / sum(raw_power);

% Compute for filtered signals (illustrative only!)
fir_power = compute_relative_power(eeg_fir);
fir_relative = fir_power / sum(fir_power);

iir_power = compute_relative_power(eeg_iir);
iir_relative = iir_power / sum(iir_power);

% Plot 1: Raw Signal with VALID Band Power Analysis
figure;

subplot(2,1,1);
plot(t, eeg_signal);
title('Raw EEG Signal');
xlabel('Time (s)');
ylabel('Amplitude (μV)');

subplot(2,1,2);
bar(100 * raw_relative);
set(gca, 'XTickLabel', band_labels);
ylabel('Power (%)');
title('Relative Power in EEG Bands (Raw Signal - Valid)');
ylim([0 100]);
grid on;

% Plot 2: FIR Filtered Signal (Alpha Band Only)
figure;

subplot(2,1,1);
plot(t, eeg_fir);
title('FIR Filtered EEG (Alpha Band: 8–13 Hz)');
xlabel('Time (s)');
ylabel('Amplitude (μV)');

subplot(2,1,2);
bar(100 * fir_relative);
set(gca, 'XTickLabel', band_labels);
ylabel('Power (%)');
title({'Relative Power in EEG Bands (FIR Filtered)', ...
       '⚠ Filtering distorts full-band power; use raw signal for band analysis'});
ylim([0 100]);
grid on;

% Plot 3: IIR Filtered Signal (Alpha Band Only)
figure;

subplot(2,1,1);
plot(t, eeg_iir);
title('IIR Filtered EEG (Alpha Band: 8–13 Hz)');
xlabel('Time (s)');
ylabel('Amplitude (μV)');

subplot(2,1,2);
bar(100 * iir_relative);
set(gca, 'XTickLabel', band_labels);
ylabel('Power (%)');
title({'Relative Power in EEG Bands (IIR Filtered)', ...
       '⚠ Filtering distorts full-band power; use raw signal for band analysis'});
ylim([0 100]);
grid on;

%% Teil 2 - Downsampling and Quantization

% Downsample signal by factor of 4

```
