#!/bin/bash
#scripts/build_binaries.sh
set -e

OS=$(uname -s)
ARCH=$(uname -m)
echo "Building binaries for $OS/$ARCH..."
pip install pyinstaller

case $OS in
    Linux)
      case $ARCH in
        x86_64)   NAME="olmon-linux-x86_64" ;;
        aarch64)  NAME="olmon-linux-arm64" ;;
        *)        echo "Unsupported architecture: $ARCH"; exit 1 ;;
      esac
      ;;
    Darwin)
      case $ARCH in
        arm64)    NAME="olmon-macos-arm64" ;;
        *)        echo "Unsupported architecture: $ARCH"; exit 1 ;;
      esac
      ;;
    *)
      echo "Unsupported OS: $OS"
      exit 1
      ;;
  esac
pyinstaller --onefile olmon/main.py --name "$NAME"

echo "binaries in dist/$NAME"
ls -la dist/