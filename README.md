# OjoSaurio 20-20-20 👀🦖

Tu compi jurásico de productividad visual: trabaja 20 minutos, escucha un pitido sutil, mira lejos 20 segundos, vuelve al ataque. Repite mientras la app esté activa.

## Qué hace ⏱️

- Cada `20m` -> `beep 1`
- `20s` después -> `beep 2`
- ciclo infinito mientras esté encendida

Temporización usa `time.monotonic()` para evitar drift por cambios de hora del sistema.

## Requisitos 🧰

- Python 3.11+

## Instalación

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## Uso

```bash
twenty20-beeper
```

O:

```bash
./scripts/run_local.sh
```

## Doble clic (Windows) 🪟

- `OjoSaurio.bat`: doble clic, crea `.venv` si falta, instala app, abre temporizador.
- `OjoSaurio.vbs`: doble clic sin ventana de consola (lanza `OjoSaurio.bat` oculto).
- En Windows, pitido usa `winsound.PlaySound` desde memoria (no depende del `wav` en disco).

## Doble clic (macOS) 🍎

- `OjoSaurio.command`: doble clic para abrir app normal (`20m` + `20s`).

## Autoarranque al encender ordenador 🚀

### macOS

```bash
./scripts/install_autostart_mac.sh
```

Desactivar:

```bash
./scripts/uninstall_autostart_mac.sh
```

### macOS sin terminal (doble clic)

- Instalar autoarranque: doble clic en `InstalarAutoarranqueMac.command`
- Desinstalar autoarranque: doble clic en `DesinstalarAutoarranqueMac.command`
- Si ya lo tenías instalado con versión anterior, desinstala y vuelve a instalar para aplicar mejoras.

### Windows (PowerShell)

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\install_autostart_windows.ps1
```

Desactivar:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\uninstall_autostart_windows.ps1
```

### Windows sin terminal (doble clic)

- Instalar autoarranque: doble clic en `InstalarAutoarranqueWindows.bat`
- Desinstalar autoarranque: doble clic en `DesinstalarAutoarranqueWindows.bat`

## Controles 🎮

- Al abrir app, el ciclo arranca automáticamente.
- `Start`: inicia ciclo si estaba detenido.
- `Pause`: pausa y preserva tiempo restante.
- `Resume`: reanuda exacto desde restante.
- `Exit`: cierra app.

## Salud visual 🩺

Esta app es recordatorio conductual; no sustituye evaluación o tratamiento médico.
