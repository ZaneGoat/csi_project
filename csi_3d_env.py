import argparse
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from CSIKit.reader import get_reader
from CSIKit.util.csitools import get_CSI

def render_3d_environment(pcap_file):
    print(f"Loading CSI data from {pcap_file} to map the 3D environment...")
    try:
        reader = get_reader(pcap_file)
        csi_data = reader.read_file(pcap_file)
        csi_matrix, no_frames, no_subcarriers = get_CSI(csi_data)
    except Exception as e:
        print(f"Error reading PCAP: {e}")
        print("Please ensure you have captured a valid CSI .pcap file using FeitCSI.")
        return

    print(f"Environment mapped using {no_frames} frames over {no_subcarriers} subcarriers.")

    # Extract amplitude data (we use the first antenna pair for simplicity)
    # The shape might vary, but generally we want (frames, subcarriers)
    amplitudes = np.abs(csi_matrix[:, 0, 0, :])
    
    # Create the X, Y meshgrid for the 3D plot
    # X = Subcarrier index (frequencies)
    # Y = Frame index (time)
    X = np.arange(no_subcarriers)
    Y = np.arange(no_frames)
    X, Y = np.meshgrid(X, Y)
    Z = amplitudes

    # Setup the 3D plot
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    # Plot the surface. This creates the "landscape" of the radio waves.
    # When a person walks through the room, they disturb the subcarriers,
    # causing visible ripples, valleys, or peaks in this surface mesh.
    surf = ax.plot_surface(X, Y, Z, cmap=cm.viridis, linewidth=0, antialiased=True)
    
    ax.set_title("3D Radio Environment Map (CSI Amplitude)")
    ax.set_xlabel("Frequency Subcarrier (Space)")
    ax.set_ylabel("Packet Frame (Time)")
    ax.set_zlabel("Signal Amplitude")
    
    fig.colorbar(surf, shrink=0.5, aspect=5)
    
    print("Opening 3D viewer. You can rotate and zoom the map.")
    plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Render a 3D environment map from CSI data.")
    parser.add_argument("pcap_file", help="Path to the FeitCSI .pcap file.")
    args = parser.parse_args()
    
    render_3d_environment(args.pcap_file)
