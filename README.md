# Music Recording and Recognition

This project implements a music recording and recognition system using the Win API for audio recording and an unofficial API from Shazam for music recognition. The program allows users to record music playing through their speakers and then perform music recognition on the recorded audio.

## Requirements
- Python 3.x
- FFmpeg (must be installed and added to system PATH)

## Installation

1. Clone the repository or download the source code.

2. Install the required dependencies using the following command:
   ```
   pip install -r requirements.txt
   ```

3. Make sure FFmpeg is installed and added to the system PATH. FFmpeg is used for audio processing. You can download FFmpeg from the official website: [https://ffmpeg.org/](https://ffmpeg.org/)

## Usage

Run the `main.py` script to start the program.

```
python main.py
```

### Recording and Recognition

The program provides an interactive command-line interface. You can use the following options:

- Press Enter: Start recording and perform music recognition on the recorded audio.
- 'q': Quit the program.
- 's': Go to settings to change the duration of recording.
- 'r': Perform music recognition on a specific audio file.

When you press Enter or choose the default option, the program will record audio for the specified duration (default is 5 seconds) and attempt to recognize the recorded music using Shazam's unofficial API.

### Settings

If you choose the 's' option, you can enter a new duration for recording. Enter the desired duration in seconds and press Enter.

### Music Recognition from File

If you choose the 'r' option, you can perform music recognition on a specific audio file. Enter the path to the audio file (in .mp3 format) and press Enter. The program will attempt to recognize the music in the specified file using Shazam's unofficial API.

## Disclaimer

Please note that the use of an unofficial API for Shazam may be against their terms of service. Use this project at your own risk.

## License

This project is licensed under the [MIT License](LICENSE).
