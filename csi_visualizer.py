import argparse
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from CSIKit.reader import get_reader
from CSIKit.util.csitools import get_CSI
import numpy as np
import time

def visualize_csi(pcap_file):
    print(f"Reading CSI data from {pcap_file} using CSIKit...")
    try:
        reader = get_reader(pcap_file)
        csi_data = reader.read_file(pcap_file)
        csi_matrix, no_frames, no_subcarriers = get_CSI(csi_data)
    except Exception as e:
        print(f"Error reading PCAP: {e}")
        print("Ensure you have captured packets using a CSI-enabled driver (like PicoScenes or Nexmon).")
        return

    print(f"Extracted {no_frames} frames with {no_subcarriers} subcarriers.")

    # We will plot the amplitude of the first subcarrier over time
    amplitudes = np.abs(csi_matrix[:, 0, 0, :]) # Shape might vary depending on hardware (frames, rx, tx, subcarriers)
    
    # Flatten it out to just get a mean amplitude per frame for simple visualization
    if len(amplitudes.shape) > 1:
        mean_amp = np.mean(amplitudes, axis=1)
    else:
        mean_amp = amplitudes

    plt.figure(figsize=(10, 5))
    plt.plot(mean_amp)
    plt.title("CSI Amplitude Over Time (Motion Proxy)")
    plt.xlabel("Packet Frame Index")
    plt.ylabel("Average CSI Amplitude")
    plt.grid(True)
    
    print("Close the plot window to exit.")
    plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Visualize CSI Data from a PCAP file.")
    parser.add_argument("pcap_file", help="Path to the .pcap file containing CSI data.")
    args = parser.parse_args()
    
    visualize_csi(args.pcap_file)
