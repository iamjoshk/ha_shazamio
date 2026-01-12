# ShazamIO Add-on

Add-on for ShazamIO service with full Rust support for fast audio recognition.

## Installation

1. Add this repository to your Home Assistant Add-on Store
2. Install the "ShazamIO Service" add-on
3. Start the add-on
4. Install the ShazamIO custom integration from HACS
5. Add the integration through Settings → Devices & Services

## Configuration

The add-on supports the following configuration options:

- **log_level**: Set the logging level (debug, info, warning, error). Default: info

## Architecture

This add-on runs a FastAPI service that provides ShazamIO functionality via REST API. The custom integration communicates with this add-on to provide Home Assistant service actions.

Benefits:
- Full Rust compiler support for fast audio recognition
- Latest ShazamIO version with all features
- Isolated environment from Home Assistant core
