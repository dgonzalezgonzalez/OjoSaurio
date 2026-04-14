# OjoSaurio 20-20-20 👀🦖

Tu compi jurásico de productividad visual: trabaja 20 minutos, escucha un pitido sutil, mira lejos 20 segundos, vuelve al ataque. Repite mientras la app esté activa.

![Logo OjoSaurio](assets/logo/ojosaurio-logo.png)

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
- El temporizador arranca automáticamente al abrir la app (también en Windows).

## Autoarranque (manual recomendado) 🚀

No incluimos instaladores de autoarranque. Si quieres autoabrir al iniciar sesión, configúralo manualmente en tu sistema operativo (es más fiable).

## Controles 🎮

- Al abrir app, el ciclo arranca automáticamente.
- `Start`: inicia ciclo si estaba detenido.
- `Pause`: pausa y preserva tiempo restante.
- `Resume`: reanuda exacto desde restante.
- `Exit`: cierra app.

## Logo e icono 🧩

Assets del logo:
- `assets/logo/ojosaurio-logo.svg`
- `assets/logo/ojosaurio-logo.png`
- `assets/logo/ojosaurio-logo.ico`

La ventana de la app ya usa este logo automáticamente cuando está disponible.

### Cambiar icono en Windows (muy básico)

1. Crea acceso directo de `OjoSaurio.bat` (clic derecho -> Crear acceso directo).
2. Clic derecho en acceso directo -> `Propiedades`.
3. `Cambiar icono...` -> elige `assets/logo/ojosaurio-logo.ico`.
4. Usa ese acceso directo en Escritorio/Barra de tareas.

### Cambiar icono en macOS (muy básico)

1. Abre `assets/logo/ojosaurio-logo.png` con Preview.
2. `Cmd + A`, luego `Cmd + C`.
3. `Get Info` de `OjoSaurio.command`.
4. Clic en iconito superior izquierdo y `Cmd + V`.
5. Si quieres, arrastra `OjoSaurio.command` al Dock.

## Salud visual 🩺

Esta app es recordatorio conductual; no sustituye evaluación o tratamiento médico.
