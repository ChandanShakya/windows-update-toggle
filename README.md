# Windows Update Toggle

A simple GUI application for Windows that enables or disables Windows Update services with just a click.

![Windows Update Toggle Screenshot](screenshot.png)

## Features

- Toggle Windows Updates on or off with a single click
- Remove the "Update and restart" option from the Windows menu
- Simple and user-friendly interface
- Requires administrator privileges to function properly

## Installation

You can download the latest executable from the [Releases](https://github.com/ChandanShakya/windows-update-toggle/releases) page.

Alternatively, you can run the script directly:

1. Ensure you have Python installed on your system
2. Clone this repository or download the source code
3. Run the script with administrator privileges:
   ```
   python windows_update_toggle.py
   ```

## Usage

1. Launch the application (requires administrator privileges)
2. Click "Disable Windows Updates" to turn updates off
3. Click "Enable Windows Updates" to turn updates back on
4. Check/uncheck the "Remove 'Update and restart' option" as needed

## Building from Source

To build the executable from source:

1. Clone this repository
   ```
   git clone https://github.com/ChandanShakya/windows-update-toggle.git
   cd windows-update-toggle
   ```

2. Install PyInstaller
   ```
   pip install pyinstaller
   ```

3. Build the executable
   ```
   pyinstaller --onefile --windowed --icon=windows_update_toggle.ico windows_update_toggle.py
   ```

## Releasing New Versions

This project uses GitHub Actions to automatically build and release new versions.

To create a new release:

1. Tag a new version in git
   ```
   git tag v1.0.0
   git push origin v1.0.0
   ```

2. The GitHub workflow will automatically build the executable and publish it as a release.

## Requirements

- Windows 10/11
- Administrator privileges
- If running from source: Python 3.6 or higher with tkinter

## License

[MIT License](LICENSE)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Disclaimer

This tool modifies system settings related to Windows Update. Use at your own risk. Always ensure you have backups of important data.