#!/bin/bash
echo "Uninstall olmon..."
set -e

sudo rm -f /usr/local/bin/olmon
rm -rf ~/.config/olmon
echo "olmon uninstalled."