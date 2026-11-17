
import os
import csv
import soundfile as sf
from mutagen import File

def analyze_audio(file_path):
    if not os.path.isfile(file_path):
        print("Error: File not found!")
        return

    try:
        audio = File(file_path)

        if audio is None or audio.info is None:
            print("Unsupported audio file!")
            return

        # Audio properties
        duration = audio.info.length
        sample_rate = getattr(audio.info, "sample_rate", "Not available")
        channels = getattr(audio.info, "channels", "Not available")
        bitrate = getattr(audio.info, "bitrate", None)

        # MP3 metadata
        metadata = {
            "File Name": os.path.basename(file_path),
            "File Format": os.path.splitext(file_path)[1].upper(),
            "Duration (seconds)": round(duration, 2),
            "Sample Rate (Hz)": sample_rate,
            "Channels": channels,
            "Bitrate (kbps)": (
                round(bitrate / 1000, 2)
                if bitrate else "Not available"
            ),
            "File Size (MB)": round(
                os.path.getsize(file_path) / (1024 * 1024), 2
            )
        }

        # Display report
        print("\n===== AUDIO ANALYSIS REPORT =====")

        for key, value in metadata.items():
            print(f"{key}: {value}")

        # Export CSV
        output_file = os.path.splitext(file_path)[0] + "_report.csv"

        with open(output_file, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Property", "Value"])

            for key, value in metadata.items():
                writer.writerow([key, value])

        print(f"\nReport saved to: {output_file}")

    except Exception as error:
        print("Could not analyze audio:", error)


if __name__ == "__main__":
    file_path = input("Enter the audio file path: ").strip().strip('"')
    analyze_audio(file_path)
