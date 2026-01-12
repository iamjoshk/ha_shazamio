#!/usr/bin/with-contenv bashio

# Get log level from options
LOG_LEVEL=$(bashio::config 'log_level' 'info')

bashio::log.info "Starting ShazamIO Service..."
bashio::log.info "Log level: ${LOG_LEVEL}"

# Start the FastAPI application
cd /app
exec python3 -m uvicorn app:app --host 0.0.0.0 --port 8099 --log-level "${LOG_LEVEL}"
