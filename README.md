# dlytb

A simple Python script to download video or audio from YouTube.

## Description

This project provides a command-line tool to download videos from YouTube in high quality or to extract audio tracks and save them as `mp3` or `m4a` files. It uses `pytubefix` for interacting with YouTube and `ffmpeg` for video and audio processing.

## License

This project is licensed under the GNU General Public License v3.0. See the `LICENSE` file for more details.

## Setup

This project uses [pixi](https://pixi.sh/) to manage dependencies and `git` for version control. Follow the instructions below for your operating system to set up the project.

### Windows

1.  **Install Git:**
    - Download and install Git from [git-scm.com/downloads](https://git-scm.com/downloads).
    - Alternatively, you can use a package manager like Chocolatey (`choco install git`) or Winget (`winget install -e --id Git.Git`).

2.  **Install pixi:**
    - Open PowerShell and run the following command:
      ```powershell
      irm https://pixi.sh/install.ps1 | iex
      ```

3.  **Clone and Install:**
    - Open a new terminal (like PowerShell or Git Bash), and run the following commands:
      ```bash
      git clone https://github.com/RaphaelRibes/dlytb.git
      cd dlytb
      pixi install
      ```

### macOS

1.  **Install Git:**
    - The easiest way to install Git is to install the Xcode Command Line Tools. Open a terminal and run:
      ```bash
      xcode-select --install
      ```
    - Alternatively, if you use [Homebrew](https://brew.sh/), you can run:
      ```bash
      brew install git
      ```

2.  **Install pixi:**
    - Open a terminal and run the following command:
      ```bash
      curl -fsSL https://pixi.sh/install.sh | bash
      ```

3.  **Clone and Install:**
    - Open a new terminal and run the following commands:
      ```bash
      git clone https://github.com/RaphaelRibes/dlytb.git
      cd dlytb
      pixi install
      ```

### Linux

1.  **Install Git:**
    - Use your distribution's package manager. For example:
      - **Debian/Ubuntu:**
        ```bash
        sudo apt-get update && sudo apt-get install git
        ```
      - **Fedora:**
        ```bash
        sudo dnf install git
        ```
      - **Arch Linux:**
        ```bash
        sudo pacman -S git
        ```

2.  **Install pixi:**
    - Open a terminal and run the following command:
      ```bash
      curl -fsSL https://pixi.sh/install.sh | bash
      ```

3.  **Clone and Install:**
    - Open a new terminal and run the following commands:
      ```bash
      git clone https://github.com/RaphaelRibes/dlytb.git
      cd dlytb
      pixi install
      ```

## Usage

The commands to use this script are the same across Windows, macOS, and Linux. You can run the tasks defined in `pixi.toml` from your terminal.

By default, the downloaded files will be saved in the directory where you run the command.

### Running the Graphical User Interface (UI)

For an easier experience, you can launch the graphical user interface. 
This allows you to paste a URL, choose your download options, and select a save location without using command-line arguments.

```bash
pixi run python gui.py
```

### Command-Line Usage

#### Download Video

To download a video in the highest available quality, use the `dlvideo` task. You need to pass the YouTube URL as an argument.

```bash
pixi run dlvideo <youtube_url>
```

**Example:**

```bash
pixi run dlvideo "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
```

#### Download Audio

To download only the audio track, use the `dlaudio` task. The default format is `mp3`.

```bash
pixi run dlaudio <youtube_url> [options]
```

**Example (MP3):**

```bash
pixi run dlaudio "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
```

**Example (M4A):**

To save the audio as an `m4a` file, pass the `--format m4a` option.

```bash
pixi run dlaudio "https://www.youtube.com/watch?v=dQw4w9WgXcQ" --format m4a
```
