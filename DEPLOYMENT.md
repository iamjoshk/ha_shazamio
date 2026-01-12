# Deployment Guide for ShazamIO Home Assistant Integration

This guide explains how to deploy and test the ShazamIO integration with its add-on.

## Architecture Overview

The ShazamIO integration consists of two components:

1. **ShazamIO Add-on** (`ha_shazamio_addon/`)
   - Runs in a separate Docker container
   - Includes Rust compiler for ShazamIO's native dependencies
   - Provides a FastAPI REST API on port 8099
   - Handles all ShazamIO library calls

2. **ShazamIO Integration** (`custom_components/ha_shazamio/`)
   - Lightweight Home Assistant custom integration
   - Communicates with the add-on via HTTP
   - Exposes 15 service actions to Home Assistant
   - Fires events with results

## Local Development Setup

### Testing the Add-on Locally

1. **Build the Docker image:**
   ```bash
   cd ha_shazamio_addon
   docker build -t ha-shazamio-addon .
   ```

2. **Run the container:**
   ```bash
   docker run -p 8099:8099 ha-shazamio-addon
   ```

3. **Test the API:**
   ```bash
   # Health check
   curl http://localhost:8099/

   # Test track search
   curl -X POST http://localhost:8099/api/search_track \
     -H "Content-Type: application/json" \
     -d '{"query": "Bohemian Rhapsody", "limit": 5}'
   ```

### Testing the Integration

1. **Copy the integration to your HA dev environment:**
   ```bash
   cp -r custom_components/ha_shazamio /path/to/homeassistant/config/custom_components/
   ```

2. **Ensure the add-on is running** (either locally or as a Home Assistant add-on)

3. **Restart Home Assistant**

4. **Add the integration:**
   - Go to Settings → Devices & Services
   - Click "+ Add Integration"
   - Search for "ShazamIO"
   - Click to add

5. **Test a service:**
   ```yaml
   service: ha_shazamio.search_track
   data:
     query: "Never Gonna Give You Up"
     limit: 5
   ```

## Production Deployment

### Step 1: Publish Add-on

The add-on needs to be available as a Home Assistant add-on repository.

1. **Push to GitHub:**
   ```bash
   git add ha_shazamio_addon/ repository.yaml
   git commit -m "Add ShazamIO add-on"
   git push
   ```

2. **Users add the repository:**
   - Settings → Add-ons → Add-on Store
   - Click three dots → Repositories
   - Add: `https://github.com/iamjoshk/ha_shazamio`

3. **Users install the add-on:**
   - Find "ShazamIO Service" in add-on store
   - Click Install
   - Click Start
   - Enable "Start on boot"

### Step 2: Publish Integration via HACS

1. **Ensure hacs.json is correct:**
   ```json
   {
     "name": "ShazamIO",
     "render_readme": true,
     "domains": ["ha_shazamio"]
   }
   ```

2. **Tag a release on GitHub:**
   ```bash
   git tag v1.0.0
   git push origin v1.0.0
   ```

3. **Submit to HACS:**
   - Go to https://github.com/hacs/default/issues
   - Open a new issue to add your integration
   - Provide your repository URL

4. **Users install via HACS:**
   - HACS → Integrations
   - Search for "ShazamIO"
   - Install
   - Restart Home Assistant
   - Add integration via UI

## Verification Checklist

Before deploying, verify:

### Add-on Verification
- [ ] Dockerfile builds successfully on all architectures (aarch64, amd64, armv7)
- [ ] Container starts without errors
- [ ] API responds to health check at http://localhost:8099/
- [ ] All 15 API endpoints respond correctly
- [ ] Rust dependencies compile successfully
- [ ] ShazamIO library loads without errors

### Integration Verification
- [ ] Integration loads in Home Assistant without errors
- [ ] All 15 services are registered
- [ ] Services can communicate with add-on
- [ ] Events are fired correctly with results
- [ ] Template rendering works in service calls
- [ ] No Python errors in Home Assistant logs

### Testing Scenarios

1. **Test basic recognition:**
   ```yaml
   service: ha_shazamio.search_track
   data:
     query: "{{ states('input_text.song_search') }}"
   ```

2. **Test event listening:**
   ```yaml
   automation:
     - trigger:
         platform: event
         event_type: shazamio_response
       action:
         service: notify.notify
         data:
           message: "Track found: {{ trigger.event.data.data }}"
   ```

3. **Test error handling:**
   - Try with invalid track ID
   - Try with network disconnected
   - Check logs for proper error messages

## Troubleshooting

### Add-on Won't Start

Check logs in Supervisor:
```bash
ha addons logs ha_shazamio
```

Common issues:
- Rust compilation failure: Check available disk space
- Port already in use: Ensure nothing else uses port 8099
- Python dependencies: Check requirements.txt versions

### Integration Can't Connect

1. Verify add-on is running:
   ```bash
   curl http://localhost:8099/
   ```

2. Check integration logs:
   Settings → System → Logs

3. Common issues:
   - Add-on not started
   - Firewall blocking port 8099
   - Wrong URL in services.py (should be `http://localhost:8099/api`)

### Services Not Appearing

1. Check integration loaded:
   - Settings → Devices & Services
   - Should see "ShazamIO" integration

2. Check service registration:
   - Developer Tools → Services
   - Search for "ha_shazamio"
   - Should see 15 services

3. Restart if needed:
   - Settings → System → Restart Home Assistant

## Multi-Architecture Support

The add-on supports three architectures:

- **aarch64**: Raspberry Pi 4, ODROID-N2, etc.
- **amd64**: Intel/AMD x86_64 systems
- **armv7**: Raspberry Pi 3, ODROID-XU4, etc.

Build configuration is in `build.yaml`. Each architecture uses the official Home Assistant base image.

## Performance Notes

- **Rust Compilation**: First build takes 10-20 minutes due to Rust compilation
- **Runtime Performance**: Fast audio fingerprinting thanks to Rust optimization
- **Memory Usage**: ~150-300MB for add-on container
- **API Latency**: <1 second for most calls, 2-5 seconds for audio recognition

## Security Considerations

- Add-on runs in isolated container
- No external network access required for integration
- Communication over localhost only
- No API keys or authentication needed for basic ShazamIO features
- Audio data never leaves your Home Assistant instance

## Updating

### Updating the Add-on

1. User goes to add-on page
2. Click "Update" if available
3. Restart add-on

### Updating the Integration

1. Via HACS: Click "Update" in HACS
2. Restart Home Assistant
3. Integration automatically uses new version

## Support

For issues or questions:
- GitHub Issues: https://github.com/iamjoshk/ha_shazamio/issues
- Home Assistant Community: Tag @iamjoshk
