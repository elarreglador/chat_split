# chat_split

Herramienta para dividir registros de chat en conversaciones individuales.

## Descripción

La aplicación `chat_split` es una herramienta que permite segmentar registros de chat en conversaciones individuales. Esta utilidad es especialmente útil para procesar exportaciones de chats de Telegram y otros formatos compatibles, dividiendo los mensajes en bloques lógicos que representan conversaciones separadas.

El proceso identifica automáticamente los límites entre conversaciones utilizando un factor de umbral que determina la separación entre mensajes de diferentes conversaciones. Esto permite crear un archivo de salida estructurado en formato JSONL (JSON Lines) donde cada línea representa una conversación completa.

## Formatos de Entrada Soportados

La herramienta `chat_split` soporta múltiples formatos de entrada a través de diferentes adaptadores:

### 1. Formato JSON de Telegram (Por defecto)
Exportaciones estándar de Telegram Desktop en formato `result.json`.

```bash
python -m chat_split --input telegram_export.json --adapter telegram
```

### 2. Formato Chat Export 
Nuevo formato con datos de conversación en estructura de directorio `ChatExport_YYYY-MM-DD`.

```bash
python -m chat_split --input ChatExport_2026-06-26/conversation.json --adapter chat_export
```

## Ejemplos de Uso

### Uso Básico
```bash
python -m chat_split --input <archivo_entrada> --adapter <formato>
```

### Con Archivo de Salida Personalizado
```bash
python -m chat_split --input ChatExport_2026-06-26/conversation.json --adapter chat_export --output mis_conversaciones.jsonl
```

### Ajustando el Factor de Umbral
```bash
python -m chat_split --input ChatExport_2026-06-26/conversation.json --adapter chat_export --factor 1.5
```

### Estableciendo Mensajes Mínimos por Conversación
```bash
python -m chat_split --input ChatExport_2026-06-26/conversation.json --adapter chat_export --min-messages 5
```

## Formato de Salida

La herramienta genera conversaciones en formato JSONL (JSON Lines), donde cada línea representa una conversación con la siguiente estructura:
- `conversation_id`: Identificador único de la conversación
- `participants`: Lista de participantes en la conversación
- `start_time`: Marca de tiempo de inicio de la conversación
- `end_time`: Marca de tiempo de finalización de la conversación
- `message_count`: Número de mensajes en la conversación
- `raw_content`: Contenido completo de la conversación
- `summary`: Espacio reservado para futura funcionalidad de resumen

El archivo de salida por defecto es `conversaciones.jsonl` si no se especifica con el parámetro `--output`.

## Instalación

Para instalar y usar la herramienta:

1. Clona o descarga este repositorio
2. Instala en modo desarrollo:
   ```bash
   pip install -e .
   ```
3. Ejecuta con tu archivo de entrada:
   ```bash
   python -m chat_split --input <tu_archivo_entrada> --adapter <formato>
   ```

El sistema está diseñado para ser extensible, facilitando la adición de soporte para formatos adicionales en el futuro.