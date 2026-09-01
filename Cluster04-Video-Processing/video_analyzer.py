import json
import os
import subprocess


def format_duration(value):
    if not value:
        return "N/A"

    seconds = float(value)
    return f"{seconds:.2f} sec"


def format_fps(value):
    if not value or value == "0/0":
        return "N/A"

    try:
        numerator, denominator = value.split("/")
        fps = float(numerator) / float(denominator)
        return f"{fps:.2f} FPS"
    except:
        return value


def format_bitrate(value):
    if not value:
        return "N/A"

    try:
        kbps = int(value) / 1000
        return f"{kbps:.0f} kbps"
    except:
        return value


def main():

    video_path = "video.mp4"

    # Check video file
    if not os.path.isfile(video_path):
        print("Error: video.mp4 not found!")
        return

    # File size
    file_size = os.path.getsize(video_path)

    # Run FFprobe
    command = [
        "ffprobe",
        "-v", "quiet",
        "-print_format", "json",
        "-show_format",
        "-show_streams",
        video_path
    ]

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True
        )
    except FileNotFoundError:
        print("Error: ffprobe not found!")
        print("Please make sure FFmpeg is added to PATH.")
        return
    except subprocess.CalledProcessError as e:
        print("FFprobe error:")
        print(e.stderr)
        return

    data = json.loads(result.stdout)

    format_info = data.get("format", {})
    streams = data.get("streams", [])

    # Find video and audio streams
    video_stream = next(
        (s for s in streams if s.get("codec_type") == "video"),
        {}
    )

    audio_stream = next(
        (s for s in streams if s.get("codec_type") == "audio"),
        {}
    )

    # -------------------------------
    # REPORT
    # -------------------------------

    print("================================")
    print("     VIDEO METADATA REPORT")
    print("================================")

    print()
    print(f"File Name       : {os.path.basename(video_path)}")
    print(
        f"File Size       : {file_size:,} bytes "
        f"({file_size / (1024 * 1024):.2f} MB)"
    )

    print(
        f"Container       : "
        f"{format_info.get('format_long_name', 'N/A')}"
    )

    print(
        f"Duration        : "
        f"{format_duration(format_info.get('duration'))}"
    )

    # -------------------------------
    # VIDEO
    # -------------------------------

    print()
    print("VIDEO")
    print("--------------------------------")

    width = video_stream.get("width", "N/A")
    height = video_stream.get("height", "N/A")

    print(f"Resolution      : {width} x {height}")

    fps = video_stream.get("avg_frame_rate")

    if not fps or fps == "0/0":
        fps = video_stream.get("r_frame_rate")

    print(f"Frame Rate      : {format_fps(fps)}")

    print(
        f"Bit Rate        : "
        f"{format_bitrate(video_stream.get('bit_rate'))}"
    )

    print(
        f"Codec           : "
        f"{video_stream.get('codec_long_name', 'N/A')}"
    )

    # -------------------------------
    # AUDIO
    # -------------------------------

    print()
    print("AUDIO")
    print("--------------------------------")

    print(
        f"Codec           : "
        f"{audio_stream.get('codec_long_name', 'N/A')}"
    )

    print(
        f"Channels        : "
        f"{audio_stream.get('channels', 'N/A')}"
    )

    sample_rate = audio_stream.get("sample_rate")

    if sample_rate:
        print(f"Sampling Rate   : {sample_rate} Hz")
    else:
        print("Sampling Rate   : N/A")

    print(
        f"Bit Rate        : "
        f"{format_bitrate(audio_stream.get('bit_rate'))}"
    )

    # -------------------------------
    # METADATA
    # -------------------------------

    print()
    print("METADATA")
    print("--------------------------------")

    metadata_found = False

    # Format metadata
    for key, value in format_info.get("tags", {}).items():
        print(f"{key:<16}: {value}")
        metadata_found = True

    # Stream metadata
    for stream in streams:
        for key, value in stream.get("tags", {}).items():
            print(f"{key:<16}: {value}")
            metadata_found = True

    if not metadata_found:
        print("No additional metadata found.")


if __name__ == "__main__":
    main()
