# OjoSaurio 20-20-20

App de escritorio mínima: cada 20 minutos suena un pitido sutil. Veinte segundos después, suena un segundo pitido. Repite mientras esté activa.

## Requisitos

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

## Doble clic (Windows)

- `OjoSaurio.bat`: doble clic, crea `.venv` si falta, instala app, abre temporizador.
- `OjoSaurio.vbs`: doble clic sin ventana de consola (lanza `OjoSaurio.bat` oculto).
- En Windows, pitido usa `winsound.PlaySound` desde memoria (no depende del `wav` en disco).

## Doble clic (macOS)

- `OjoSaurio.command`: doble clic para abrir app normal (`20m` + `20s`).

## Autoarranque al encender ordenador

### macOS

```bash
./scripts/install_autostart_mac.sh
```

Desactivar:

```bash
./scripts/uninstall_autostart_mac.sh
```

### Windows (PowerShell)

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\install_autostart_windows.ps1
```

Desactivar:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\uninstall_autostart_windows.ps1
```

## Controles

- `Start`: inicia ciclo 20 minutos.
- `Pause`: pausa y preserva tiempo restante.
- `Resume`: reanuda exacto desde restante.
- `Exit`: cierra app.

## Regla temporal

- `20m` -> `beep 1`
- `20s` -> `beep 2`
- repetir

Temporización usa `time.monotonic()` para evitar drift por cambios de hora del sistema.

## Salud visual

Esta app es recordatorio conductual; no sustituye evaluación o tratamiento médico.
