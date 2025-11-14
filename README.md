# MoreLogin Editor Automation

A Python-based GUI application for browser automation using MoreLogin and MPPC API integration. This application provides a simple interface to manage multiple browser instances and automate browser-related tasks.

## Features

- **Multi-Browser Management**: Control up to 6 browser instances simultaneously
- **MoreLogin Integration**: Seamless integration with MoreLogin browser profiles
- **MPPC API Integration**: Connect to MPPC API for traffic list management
- **Screenshot Capability**: Capture screenshots of browser windows
- **Grid View**: Quick access to all browser windows in a grid layout
- **Windows Automation**: Native Windows API integration for window management
- **Configurable**: Easy configuration through INI files

## Requirements

- Python 3.11 or higher
- Windows OS (uses Windows-specific APIs)
- Required Python packages:
  - `tkinter` (usually included with Python)
  - `PIL` (Pillow)
  - `pywintypes` (pywin32)
  - `configparser` (standard library)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/RikuSato0/morelogin-editor-automation.git
cd morelogin-editor-automation
```

2. Install required dependencies:
```bash
pip install pillow pywin32
```

3. Configure the application by creating or editing `settings.ini` (see Configuration section)

## Configuration

The application uses `settings.ini` for configuration. You can also specify a custom configuration file as the first argument:

```bash
python start-ui.py path/to/settings.ini
```

A custom settings file can be specified as the second argument:

```bash
python start-ui.py settings.ini settings-custom.ini
```

### Configuration Sections

The `settings.ini` file should contain the following sections:

- `[Process]`: Browser process configuration
- `[MppcApi]`: MPPC API connection settings
- `[Log]`: Logging configuration
- `[Browser]`: Browser-specific settings (MoreLogin)

Example configuration structure:
```ini
[Process]
browser_title = Your Browser Title
screenshot_path = screenshots/

[MppcApi]
base_url = https://api.example.com
login = your_login
traflist = your_traflist_id

[Log]
logfile = ui.log

[Browser]
# MoreLogin browser configuration
```

## Usage

### Running the Application

**Option 1: Using Python directly**
```bash
python start-ui.py
```

**Option 2: Using the batch file**
```bash
start.bat
```

**Option 3: Using the compiled executable**
```bash
dist/start-ui.exe
```

### GUI Controls

The application provides a simple GUI with the following controls:

- **Buttons 1-6**: Switch to and activate browser windows 1-6
- **Grid Button**: Display all browser windows in a grid layout
- **Screenshot Button**: Capture screenshots of browser windows
- **Restart Button**: Restart all browser instances

### Testing

Test scripts are available to verify the setup:

**Test MPPC Connection:**
```bash
python test_mppc_connection.py
```

Or use the batch file:
```bash
test_mppc.bat
```

**List Traffic Lists:**
```bash
python list_traflists.py
```

Or use the batch file:
```bash
list_traflists.bat
```

## Building

The application can be built into a standalone executable using PyInstaller.

### Build Options

**Standard build (with console):**
```bash
build-console.bat
```

**Windowed build (no console):**
```bash
build.bat
```

**Manual build:**
```bash
pyinstaller.exe --onefile --noconsole start-ui.py
```

The executable will be created in the `dist/` directory.

## Project Structure

```
.
├── classes/                  # Core application classes
│   ├── caction.py           # Business logic and actions
│   ├── cbasic.py            # Base class with common functionality
│   ├── cbrowsermorelogin.py # MoreLogin browser integration
│   ├── cmppcapi.py          # MPPC API client
│   ├── cui.py               # User interface (tkinter)
│   ├── cwindows.py          # Windows API wrapper
│   └── ubasics.py           # Utility functions
├── static/                  # Static assets (images)
│   ├── camera.png
│   ├── grid.png
│   └── refresh.png
├── build/                   # PyInstaller build directory (ignored)
├── dist/                    # Compiled executables (ignored)
├── start-ui.py              # Main application entry point
├── start-ui.spec            # PyInstaller specification file
├── settings.ini             # Configuration file (ignored, create your own)
├── build.bat                # Build script
├── build-console.bat        # Build script with console
├── start.bat                # Run script
├── test_mppc_connection.py  # MPPC API connection test
├── test_morelogin_permissions.py  # MoreLogin permissions test
├── list_traflists.py        # List traffic lists utility
└── README.md                # This file
```

## Version History

- **v1.08** - Updated MoreLogin browsers
- **v1.07** - Added MPPC track visit and click API calls, updated MoreLogin browsers
- **v1.06** - Added single screenshots, updated MoreLogin browsers
- **v1.05** - Added multi pages to proxy read in MultiLogin API (new config: `Browser.proxy_pages = 2`)

## Development

### Code Structure

The application follows an object-oriented design:

- **CBasic**: Base class providing configuration management and logging
- **CUI**: Main UI class extending CBasic, handles tkinter interface
- **CAction**: Business logic layer, coordinates browser and API operations
- **CBrowserMoreLogin**: MoreLogin browser automation wrapper
- **CMppcApi**: MPPC API client implementation
- **CWindows**: Windows API wrapper for window management

### Logging

The application logs to files specified in the configuration. Logs include:
- Application startup/shutdown
- Browser operations
- API calls
- Errors and exceptions

## Troubleshooting

### Common Issues

1. **"Another instance already running"**: Close any existing instances of the application
2. **MPPC API connection fails**: Verify your `settings.ini` configuration and network connectivity
3. **Browser windows not found**: Ensure MoreLogin browsers are properly installed and configured
4. **Screenshot errors**: Check that the screenshot path exists and is writable

### Debug Mode

For debugging, you can modify `start-ui.py` to enable console output or run with console:

```bash
python start-ui.py
```

Or build with console enabled:
```bash
build-console.bat
```

## License

[Specify your license here]

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues and questions, please open an issue on the [GitHub repository](https://github.com/RikuSato0/morelogin-editor-automation).

