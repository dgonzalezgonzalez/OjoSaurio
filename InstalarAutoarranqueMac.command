#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"
./scripts/install_autostart_mac.sh

echo
echo "Si ves 'Autostart enabled on macOS.', quedo instalado."
read -r -p "Pulsa Enter para cerrar..."
