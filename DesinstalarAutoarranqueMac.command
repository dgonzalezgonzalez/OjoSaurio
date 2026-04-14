#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"
./scripts/uninstall_autostart_mac.sh

echo
echo "Si ves 'Autostart disabled on macOS.', quedo desinstalado."
read -r -p "Pulsa Enter para cerrar..."
