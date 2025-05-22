%% Teil 1 – Filtering an EEG Signal

% Load EEG dataset
load('sampleEEGData.mat');  % Loads EEG struct with fields 'data' and 'srate'
fs = EEG.srate;
fprintf('Sampling rate: %d Hz\n', fs);

% Extract one EEG channel (e.g., channel 1)
eeg_signal = EEG.data(1, :);
t = (0:length(eeg_signal)-1) / fs;

% Plot raw EEG signal
figure;
plot(t, eeg_signal);
xlabel('Time (s)');
ylabel('Amplitude (µV)');
title('Raw EEG Signal');

% Design FIR bandpass filter for alpha band (8–13 Hz)
filt_order = 100;
fir_coeff = fir1(filt_order, [8 13]/(fs/2), 'bandpass');

% Apply FIR filter
eeg_fir = filtfilt(fir_coeff, 1, eeg_signal);

% Design IIR (Butterworth) bandpass filter for alpha band
[iir_b, iir_a] = butter(4, [8 13]/(fs/2), 'bandpass');

% Apply IIR filter
eeg_iir = filtfilt(iir_b, iir_a, eeg_signal);

% Plot comparison of raw, FIR, and IIR filtered signals
figure;
subplot(3,1,1);
plot(t, eeg_signal);
title('Raw EEG Signal');
xlabel('Time (s)'); ylabel('Amplitude (µV)');

subplot(3,1,2);
plot(t, eeg_fir);
title('FIR Filtered EEG (8–13 Hz)');
xlabel('Time (s)'); ylabel('Amplitude (µV)');

subplot(3,1,3);
plot(t, eeg_iir);
title('IIR Filtered EEG (8–13 Hz)');
xlabel('Time (s)'); ylabel('Amplitude (µV)');

% Assume: eeg_signal is a 1D signal vector, fs is the sampling rate

% Define frequency bands
bands = {
    'Delta', [0.5 4];
    'Theta', [4 8];
    'Alpha', [8 13];
    'Beta',  [13 30];
};

% Preallocate results
band_names = bands(:,1);
band_ranges = cell2mat(bands(:,2));
num_bands = size(band_ranges,1);
power_values = zeros(num_bands,1);
% eeg_signal=eeg_fir; % for showing what the filtered signal results in
% Compute power in each band
for i = 1:num_bands
    power_values(i) = bandpower(eeg_signal, fs, band_ranges(i,:));
end

% Compute total power (for relative comparison)
total_power = sum(power_values);
relative_power = power_values / total_power;

% Display result
fprintf('EEG Band Powers:\n');
for i = 1:num_bands
    fprintf('%s: %.4f µV^2 (%.2f%%)\n', ...
        band_names{i}, power_values(i), 100 * relative_power(i));
end

%% Teil 2 – Downsampling and Quantization

% Downsample signal by factor of 4 (here 125 Hz) 
eeg_downsampled = downsample(eeg_signal, 4);
fs_down = fs / 4;
t_down = (0:length(eeg_downsampled)-1) / fs_down;

% Quantize to 8-bit
eeg_min = min(eeg_downsampled);
eeg_max = max(eeg_downsampled);
eeg_norm = (eeg_downsampled - eeg_min) / (eeg_max - eeg_min);
eeg_quant = round(eeg_norm * 255);
eeg_dequant = quantizise(eeg_downsampled,8);



mse = mean((eeg_downsampled - eeg_quant).^2);

fprintf('Mean error is %.2f\n',mse);

% Now all
% downfs = [500,250,125];
% quants = [8 , 4];
% 
% eeg_downsampled=cell(length(downfs),1);
% 
% 
% eeg_quant_down=cell(length(downfs),length(quants));
% t_down=cell(size(eeg_downsampled));
% 
% for i=1:length(downfs)
%     eeg_downsampled{i}=downsamplize(eeg_signal,fs,downfs(i));
%     t_down{i} =downsample(t,downfs(i));
% end
% for i=1:length(eeg_downsampled)
%     for j=1:length(quants)
%         eeg_quant_down{i,j} =quantizise(eeg_downsampled{i},quants(j));
% 
%     end
% end
% 

% Plot downsampled and quantized signal
% figure;
% aux=0;
% for i=1:length(eeg_downsampled)
%     for j=1:length(quants)
%         aux = aux+1;
% subplot(3,2,aux);
% plot(t_down{i}, eeg_quant_down{i,j});
% xlabel('Time (s)');
% ylabel('Amplitude (µV)');
% %legend('Downsampled and Quantized EEG (8-bit)');
% 
%     end
% end

%% Teil 3 – Execution Time and Information Content

% Measure execution time on original signal
tic;
eeg_fir_orig = filtfilt(fir_coeff, 1, eeg_signal);
time_orig = toc;

% Measure execution time on downsampled + quantized signal
tic;
eeg_fir_down = filtfilt(fir_coeff, 1, eeg_dequant);
time_down = toc;

fprintf('Execution time (original): %.5f s\n', time_orig);
fprintf('Execution time (reduced): %.5f s\n', time_down);

% Analyze alpha band power
bp_orig = bandpower(eeg_fir_orig, fs, [8 13]);
bp_down = bandpower(eeg_fir_down, fs_down, [8 13]);

fprintf('Alpha band power (original): %.4f µV^2\n', bp_orig);
fprintf('Alpha band power (reduced): %.4f µV^2\n', bp_down);

% Optional: Compute MSE between original and reconstructed signal
eeg_interp = interp1(t_down, eeg_dequant, t, 'linear', 'extrap');
mse = mean((eeg_signal - eeg_interp).^2);
fprintf('MSE between original and quantized-interpolated: %.4f\n', mse);
%% Functions

function quantized_signal = quantizise(signal, bits)
%QUANTIZISE Quantizes a signal to a given bit depth and returns the dequantized result.
%
%   quantized_signal = quantizise(signal, bits)
%
%   Inputs:
%     signal - input signal vector to be quantized
%     bits   - number of bits for quantization (e.g., 8 for 8-bit)
%
%   Output:
%     quantized_signal - signal after quantization and dequantization

    % Determine min and max of signal
    s_min = min(signal);
    s_max = max(signal);
    
    % Normalize to [0, 1]
    signal_norm = (signal - s_min) / (s_max - s_min);
    
    % Quantize using specified bit resolution
    levels = 2^bits - 1;
    signal_quant = round(signal_norm * levels);
    
    % Dequantize back to original range
    quantized_signal = (signal_quant / levels) * (s_max - s_min) + s_min;
end

function [signal_ds, t_ds] = downsamplize(signal, fs_old, fs_target)
%DOWNSAMPLIZE Downsamples a signal to a target sampling rate and returns the new time vector.
%
%   [signal_ds, t_ds] = downsamplize(signal, fs_old, fs_target)
%
%   Inputs:
%     signal     - input signal to be downsampled
%     fs_old     - original sampling rate (Hz)
%     fs_target  - target sampling rate (Hz)
%
%   Outputs:
%     signal_ds  - downsampled signal
%     t_ds       - corresponding time vector (in seconds)

    % Validate input
    if fs_target > fs_old
        error('Target sampling rate must be lower than original sampling rate.');
    end
    
    % Compute integer downsampling factor
    factor = fs_old / fs_target;
    
    if mod(factor, 1) ~= 0
        error('Downsampling factor must be an integer. Adjust fs_target accordingly.');
    end

    % Downsample signal
    signal_ds = downsample(signal, factor);

    % Create new time vector
    t_ds = (0:length(signal_ds)-1) / fs_target;
end
