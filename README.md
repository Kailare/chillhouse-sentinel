# Chillhouse-Sentinel

Security-focused monitoring for new pump.fun Solana token launches. The scanner
listens to the PumpPortal websocket stream, detects tokens whose name or symbol
contains "Chillhouse" (case-insensitive), and emits neutral security alerts to
stdout as JSON. If an `OPENAI_API_KEY` is present, the agent uses an LLM to
generate a short security audit warning; otherwise it falls back to templates.

## Features

- Websocket listener for `wss://pumpportal.fun/api/data`
- Case-insensitive filter for "Chillhouse" in token name or symbol
- LLM-based security warnings with a template fallback
- JSON output for easy piping into other tools

## Quick Start

1. Create a virtual environment and install dependencies:

   ```bash
   python -m venv .venv
   .\.venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. Set your API key (optional):

   ```
   OPENAI_API_KEY=your_key_here
   OPENAI_MODEL=gpt-4o-mini
   ```

3. Run the monitor:

   ```bash
   python monitor.py
   ```

The output is one JSON line per matching token:

```json
{"alert":"Security Alert: Metadata mismatch observed across sources. Chillhouse (CHILL) | mint=...","token":{...}}
```

## Websocket Payload Reasoning (First Principles)

Websockets provide a long-lived, bidirectional channel where:

1. The client connects once (handshake).
2. The client sends a subscribe message describing which events it wants.
3. The server pushes events as they occur (no polling).

For PumpPortal:

- The endpoint is a single websocket URL.
- The server supports a **method-based** subscription, so you send a JSON object
  like `{ "method": "subscribeNewToken" }`.
- After subscribing, each incoming message is JSON. By inspecting the payload,
  you typically see a top-level object with a `data` field containing token
  metadata.

This is why `monitor.py`:

- Sends `{"method": "subscribeNewToken"}` after connecting.
- Treats messages as JSON and looks for a `data` object.
- Reads `name`, `symbol`, and `mint` from that object.

If PumpPortal ever changes the payload shape, the safe, first-principles update
is to log raw messages briefly and then adjust the field extraction.

## Anchor Instruction Discriminators (First Principles)

Anchor programs on Solana identify each instruction by a **discriminator**:

1. Anchor takes the instruction name (e.g., `initialize`).
2. It computes a SHA-256 hash of the string `"global:<instruction_name>"`.
3. The first 8 bytes of that hash become the discriminator.

When an instruction is sent, those 8 bytes are placed at the start of the
instruction data. This lets a program quickly know which instruction variant
the client intended, without an explicit enum tag in the IDL.

So to decode:

1. Read the first 8 bytes of instruction data.
2. Compare it against the known discriminators generated from the program's
   instruction names.
3. Once matched, parse the remaining bytes according to that instruction's
   argument layout.

This monitor does not decode Anchor instructions directly. If you later add
transaction decoding, you will need program IDLs and discriminator matching.

## Project Layout

```
chillhouse/
  monitor.py
  engine/
    brain.py
    warning_generator.py
    notifier.py
```

## Notes

- You can pipe JSON output to a file or your own internal alerting system.
- This tool is intended for passive monitoring and analysis only.
