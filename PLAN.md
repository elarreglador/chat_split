# msg_split

## Plan de Arquitectura

### Estructura del proyecto

```
msg_split/
├── README.md
├── pyproject.toml
├── .gitignore
├── src/
│   ├── __init__.py
│   ├── __main__.py        # Punto de entrada CLI (argparse)
│   ├── models.py          # Dataclasses: Message, Conversation
│   ├── ingestor.py        # Capa 1: leer estado previo + filtrar mensajes nuevos
│   ├── segmenter.py       # Capa 2: cálculo de umbral dinámico + agrupación
│   ├── persist.py         # Capa 3: lectura/escritura JSONL
│   └── adapters/
│       ├── __init__.py
│       ├── base.py        # ABC: TelegramAdapter
│       └── telegram_json.py  # Adaptador para result.json
├── tests/
│   ├── __init__.py
│   ├── test_models.py
│   ├── test_segmenter.py
│   └── test_ingestor.py
└── sample_data/
    └── sample_result.json
```

### Flujo de datos

```
[result.json]  ──►  adapters.telegram_json  ──►  list[Message]
                                                     │
                                              ingestor.py (filtra por end_time)
                                                     │
                                              segmenter.py (calcula umbral dinámico)
                                                     │
                                              persist.py (append a conversaciones.jsonl)
```

### 1. Modelos (`models.py`)

Dos dataclasses:

- **`Message`**: `id`, `date` (datetime), `from` (str), `text` (str)
- **`Conversation`**: `conversation_id` (UUID), `participants` (list[str]), `start_time`, `end_time`, `message_count`, `raw_content` (texto completo), `summary` (None)

### 2. Adaptador (`adapters/telegram_json.py`)

Parsea `result.json` (estructura estándar de Telegram Desktop: `{name, type, messages: [{id, date, from, text}]}`) y devuelve `list[Message]`. Los adaptadores adicionales solo necesitan implementar `parse(path) -> list[Message]`.

### 3. Ingesta idempotente (`ingestor.py`)

1. Lee `conversaciones.jsonl` (si existe) con `persist.read_jsonl()`.
2. Extrae el `end_time` más reciente.
3. Filtra `messages` nuevos donde `msg.date > last_end_time`.
4. Si no hay estado previo, procesa todos.

### 4. Segmentación dinámica (`segmenter.py`) — núcleo

1. Calcula los Δt (segundos) entre mensajes consecutivos.
2. **Umbral**: `median(Δt) + (factor × std(Δt))`. El factor es configurable (por defecto 1.0).
3. Si Δt > umbral → corte de conversación.
4. Agrupa los mensajes en objetos `Conversation`.
5. Si hay muy pocos mensajes (< umbral mínimo), usa un valor fijo de respaldo (ej: 30 min).

### 5. Persistencia (`persist.py`)

- `read_jsonl(path) -> list[Conversation]` — lee estado previo
- `append_jsonl(path, conversations)` — añade nuevas conversaciones al final (append-only)

### 6. CLI (`__main__.py`)

```
python -m msg_split --input result.json [--output conversaciones.jsonl] [--factor 1.0] [--min-messages 3]
```

Usa `argparse`. Argumentos:
- `--input` (obligatorio): ruta al log de Telegram
- `--output` (por defecto: `conversaciones.jsonl`)
- `--factor` (por defecto: `1.0`): multiplicador de desviación estándar para el umbral
- `--min-messages` (por defecto: `3`): mínimo de mensajes para considerar una "conversación"

### Tests

Unit tests con `pytest`:
- `test_models.py`: creación de Message/Conversation
- `test_segmenter.py`: cálculo de umbral con datos controlados, casos borde (1 mensaje, gaps muy grandes, etc.)
- `test_ingestor.py`: filtrado por end_time, integración simple

---