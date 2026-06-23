#!/bin/bash
set -e

REPO="https://github.com/glemiu6/olmon"

detect_platform() {
  OS=$(uname -s)
  ARCH=$(uname -m)

  case $OS in
    Linux)
      case $ARCH in
        x86_64)   BINARY="olmon-linux-x86_64" ;;
        aarch64)  BINARY="olmon-linux-arm64" ;;
        *)        echo "Unsupported architecture: $ARCH"; exit 1 ;;
      esac
      INSTALL_DIR="/usr/local/bin/"
      ;;
    Darwin)
      case $ARCH in
        arm64)
          BINARY="olmon-macos-arm64"
          INSTALL_DIR="/opt/homebrew/bin"
          ;;
        x86_64)
          echo "Intel Mac binary not available."
          echo "Install via pip: pip install olmon"
          exit 1
          ;;
        *)  echo "Unsupported architecture: $ARCH"; exit 1 ;;
      esac
      ;;
    *)
      echo "Unsupported OS: $OS. Use pip install olmon"
      exit 1
      ;;
    esac

}


get_latest_version() {
  LATEST=$(curl -fsSL "https://api.github.com/repos/glemiu6/olmon/releases/latest" | grep '"tag_name"' | sed 's/.*"tag_name": *"\([^"]*\)".*/\1/')
  # PyPI fallback
  if [ -z "$LATEST" ]; then
    LATEST=$(curl -fsSL "https://pypi.org/pypi/olmon/json" | grep -o '"version":"[^"]*"' | head -1 | sed 's/"version":"//;s/"//')
    LATEST="v$LATEST"
  fi

  if [ -z "$LATEST" ]; then
    echo "Error: could not determine latest version."
    exit 1
  fi
}


download_binary() {
  URL="$REPO/releases/download/$LATEST/$BINARY"
  echo "Downloading from $URL..."
  curl -L --progress-bar "$URL" -o olmon
  if [ $? -ne 0 ] || [ ! -s olmon ]; then
    rm -f komit
    exit 1
  fi
  chmod +x olmon
  if [ ! -d "$INSTALL_DIR" ]; then
    echo "Creating $INSTALL_DIR..."
    sudo mkdir -p "$INSTALL_DIR"
  fi
  sudo mv olmon "$INSTALL_DIR/"
  echo "Installed to $INSTALL_DIR/olmon"
}


print_success() {
  echo ""
  echo "olmon $LATEST installed successfully"
  echo ""
  echo "Run 'olmon status'        to check Ollama status"
  echo "Run 'olmon models'        to list installed models"
  echo "Run 'olmon ps'            to see running models"
  echo "Run 'olmon watch'         to open live dashboard"
  echo "Run 'olmon --help'   to view your config"
  echo ""
}

detect_platform
get_latest_version
echo "Installing olmon $LATEST"
download_binary
print_success