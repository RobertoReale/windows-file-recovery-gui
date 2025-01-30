# Windows File Recovery GUI

A user-friendly graphical interface for Microsoft's Windows File Recovery tool, making file recovery more accessible to all users.

![License](https://img.shields.io/badge/license-MIT-blue.svg)

## Features

- Intuitive step-by-step interface
- Visual drive selection
- Multiple recovery modes:
  - Regular Mode (for recently deleted files)
  - Extensive Mode (for older files or formatted drives)
  - Segment Mode (for NTFS file recovery)
- File type filtering
- Folder path browser
- Built-in help guide
- Command preview before execution

## Prerequisites

- Windows 10 version 2004 and above
- [Windows File Recovery](https://www.microsoft.com/en-us/p/windows-file-recovery/9n26s50ln705) tool installed
- Python 3.6 or higher
- Administrator privileges

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/windows-file-recovery-gui.git
cd windows-file-recovery-gui
```

2. Install required dependencies:
```bash
pip install pywin32
```

## Usage

1. Run the application as administrator:
   - Right-click on `windows_file_recovery_gui.py`
   - Select "Run as administrator"

2. Follow the step-by-step interface:
   - Select source and destination drives
   - Choose recovery mode
   - Specify file types or paths (optional)
   - Generate and execute the recovery command

## Creating an Executable

To create a standalone executable:

1. Install PyInstaller:
```bash
pip install pyinstaller
```

2. Create the executable:
```bash
pyinstaller --onefile --uac-admin windows_file_recovery_gui.py
```

The executable will be created in the `dist` folder.

## Important Notes

- Source and destination drives must be different
- For best results, minimize computer usage after file deletion
- Recovery success depends on various factors including time since deletion and disk usage
- Some file systems only support specific recovery modes (see help tab for details)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Based on Microsoft's [Windows File Recovery](https://support.microsoft.com/en-us/windows/recover-lost-files-on-windows-61f5b28a-f5b8-3cc2-0f8e-a63cb4e1d4c4) tool
- Thanks to all contributors and users of this project

## Disclaimer

This is an unofficial GUI for Windows File Recovery. It is not affiliated with or endorsed by Microsoft. Use at your own risk.
