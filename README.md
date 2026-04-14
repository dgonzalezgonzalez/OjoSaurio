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
