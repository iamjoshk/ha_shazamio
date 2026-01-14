# ShazamIO Home Assistant Integration

A comprehensive Home Assistant custom integration that provides a complete wrapper for [ShazamIO](https://github.com/shazamio/ShazamIO), enabling all ShazamIO functionality through Home Assistant service actions.

> ## THIS IS VERY ALPHA RIGHT NOW

## Features

- **Complete ShazamIO API Coverage**: All ShazamIO methods are available as Home Assistant services
- **Templatable Parameters**: Service data supports Home Assistant templates for dynamic automation
- **HACS Compatible**: Easy installation through HACS (Home Assistant Community Store)
- **Event-Based Responses**: Results are published as Home Assistant events for flexible automation
- **Up-to-Date**: Always uses the latest release of ShazamIO (v0.8.1+)
- **Add-on Architecture**: Runs ShazamIO in a separate container with full Rust support for optimal performance

## Architecture

This integration uses a two-part architecture:
1. **ShazamIO Add-on**: Runs in a separate Docker container with Rust compiler support, providing a FastAPI REST service
2. **ShazamIO Integration**: Lightweight integration that communicates with the add-on and exposes services to Home Assistant

This architecture ensures compatibility with ShazamIO's Rust-based audio fingerprinting while maintaining a clean integration.

## Installation

**Important**: You must install both the add-on AND the integration for this to work.

### Step 1: Install the ShazamIO Add-on

1. Go to Settings → Add-ons → Add-on Store
2. Click the three dots in the top right → Repositories
3. Add `https://github.com/iamjoshk/ha_shazamio` as a repository
4. Find "ShazamIO Service" in the add-on store
5. Click "Install"
6. Once installed, click "Start"
7. Enable "Start on boot" if desired

### Step 2: Install the ShazamIO Integration

#### Via HACS (Recommended)

1. Open HACS in your Home Assistant instance
2. Click on "Integrations"
3. Click the three dots in the top right corner
4. Select "Custom repositories"
5. Add `https://github.com/iamjoshk/ha_shazamio` as an Integration
6. Click "Install"
7. Restart Home Assistant
8. Go to Settings → Devices & Services → Add Integration
9. Search for "ShazamIO" and add it

#### Manual Installation

1. Copy the `custom_components/ha_shazamio` folder to your Home Assistant `custom_components` directory
2. Restart Home Assistant
3. Go to Settings → Devices & Services → Add Integration
4. Search for "ShazamIO" and add it

## Available Services

All services support templatable parameters for maximum flexibility in automations.

### 1. `ha_shazamio.recognize`
Recognize a track from audio file or data.

**Parameters:**
- `audio_path` (optional): Path to audio file
- `audio_data` (optional): Audio data as bytes
- `language` (optional, default: "en-US"): Language code for results
- `endpoint_country` (optional, default: "GB"): Country code for API endpoint

**Example:**
```yaml
service: ha_shazamio.recognize
data:
  audio_path: "/config/audio/song.mp3"
  language: "en-US"
```

### 2. `ha_shazamio.artist_about`
Get detailed information about an artist.

**Parameters:**
- `artist_id` (required): Shazam artist ID
- `views` (optional): List of views to include (e.g., ["top-songs", "full-albums"])
- `extend` (optional): List of extended info (e.g., ["artistBio", "origin"])
- `language` (optional): Language code
- `endpoint_country` (optional): Country code

**Example:**
```yaml
service: ha_shazamio.artist_about
data:
  artist_id: 43328183
  views: ["top-songs", "full-albums"]
  extend: ["artistBio"]
```

### 3. `ha_shazamio.track_about`
Get detailed information about a track.

**Parameters:**
- `track_id` (required): Shazam track ID
- `language` (optional): Language code
- `endpoint_country` (optional): Country code

**Example:**
```yaml
service: ha_shazamio.track_about
data:
  track_id: 552406075
```

### 4. `ha_shazamio.search_artist`
Search for artists by name.

**Parameters:**
- `query` (required): Artist name or search prefix
- `limit` (optional, default: 10): Maximum results (1-100)
- `offset` (optional, default: 0): Number of results to skip
- `language` (optional): Language code
- `endpoint_country` (optional): Country code

**Example:**
```yaml
service: ha_shazamio.search_artist
data:
  query: "Drake"
  limit: 5
```

### 5. `ha_shazamio.search_track`
Search for tracks by title.

**Parameters:**
- `query` (required): Track title or search prefix
- `limit` (optional, default: 10): Maximum results
- `offset` (optional, default: 0): Results offset
- `language` (optional): Language code
- `endpoint_country` (optional): Country code

**Example:**
```yaml
service: ha_shazamio.search_track
data:
  query: "{{ states('input_text.song_search') }}"
  limit: 10
```

### 6. `ha_shazamio.related_tracks`
Get tracks similar to a given track.

**Parameters:**
- `track_id` (required): Shazam track ID
- `limit` (optional, default: 20): Maximum results
- `offset` (optional, default: 0): Results offset
- `language` (optional): Language code
- `endpoint_country` (optional): Country code

### 7. `ha_shazamio.top_world_tracks`
Get top tracks worldwide.

**Parameters:**
- `limit` (optional, default: 200): Maximum results
- `offset` (optional, default: 0): Results offset
- `language` (optional): Language code
- `endpoint_country` (optional): Country code

### 8. `ha_shazamio.top_country_tracks`
Get top tracks in a specific country.

**Parameters:**
- `country_code` (required): ISO 3166-2 country code (e.g., "US", "GB")
- `limit` (optional, default: 200): Maximum results
- `offset` (optional, default: 0): Results offset
- `language` (optional): Language code
- `endpoint_country` (optional): Country code

**Example:**
```yaml
service: ha_shazamio.top_country_tracks
data:
  country_code: "US"
  limit: 50
```

### 9. `ha_shazamio.top_city_tracks`
Get top tracks in a specific city.

**Parameters:**
- `country_code` (required): ISO 3166-2 country code
- `city_name` (required): Name of the city
- `limit` (optional, default: 200): Maximum results
- `offset` (optional, default: 0): Results offset
- `language` (optional): Language code
- `endpoint_country` (optional): Country code

**Example:**
```yaml
service: ha_shazamio.top_city_tracks
data:
  country_code: "US"
  city_name: "New York"
  limit: 20
```

### 10. `ha_shazamio.top_world_genre_tracks`
Get top tracks worldwide for a specific genre.

**Parameters:**
- `genre` (required): Genre code (1-18, see below)
- `limit` (optional, default: 100): Maximum results
- `offset` (optional, default: 0): Results offset
- `language` (optional): Language code
- `endpoint_country` (optional): Country code

**Genre Codes:**
- 1: POP
- 2: HIP_HOP_RAP
- 3: DANCE
- 4: ELECTRONIC
- 5: RNB_SOUL
- 6: ALTERNATIVE
- 7: ROCK
- 8: LATIN
- 9: FILM_TV_STAGE
- 10: COUNTRY
- 11: AFRO_BEATS
- 12: WORLDWIDE
- 13: REGGAE_DANCE_HALL
- 14: HOUSE
- 15: K_POP
- 16: FRENCH_POP
- 17: SINGER_SONGWRITER
- 18: REGIONAL_MEXICANO

**Example:**
```yaml
service: ha_shazamio.top_world_genre_tracks
data:
  genre: "7"  # Rock
  limit: 50
```

### 11. `ha_shazamio.top_country_genre_tracks`
Get top tracks in a country for a specific genre.

**Parameters:**
- `country_code` (required): ISO 3166-2 country code
- `genre` (required): Genre code (see above)
- `limit` (optional, default: 200): Maximum results
- `offset` (optional, default: 0): Results offset
- `language` (optional): Language code
- `endpoint_country` (optional): Country code

### 12. `ha_shazamio.artist_albums`
Get all albums by an artist.

**Parameters:**
- `artist_id` (required): Shazam artist ID
- `limit` (optional, default: 10): Maximum results
- `offset` (optional, default: 0): Results offset
- `language` (optional): Language code
- `endpoint_country` (optional): Country code

### 13. `ha_shazamio.search_album`
Get information about an album.

**Parameters:**
- `album_id` (required): Shazam album ID
- `language` (optional): Language code
- `endpoint_country` (optional): Country code

### 14. `ha_shazamio.listening_counter`
Get listening count for a track.

**Parameters:**
- `track_id` (required): Shazam track ID
- `language` (optional): Language code
- `endpoint_country` (optional): Country code

### 15. `ha_shazamio.listening_counter_many`
Get listening counts for multiple tracks.

**Parameters:**
- `track_ids` (required): Comma-separated list of track IDs
- `language` (optional): Language code
- `endpoint_country` (optional): Country code

**Example:**
```yaml
service: ha_shazamio.listening_counter_many
data:
  track_ids: "552406075,549952578,546891609"
```

## Receiving Results

All service calls fire a `ha_shazamio_response` event with the result data. You can listen to these events in your automations:

```yaml
automation:
  - alias: "Process Shazam Recognition"
    trigger:
      - platform: event
        event_type: ha_shazamio_response
        event_data:
          service: recognize
    action:
      - service: notify.mobile_app
        data:
          message: >
            Recognized: {{ trigger.event.data.data.track.title }} 
            by {{ trigger.event.data.data.track.subtitle }}
```

## Advanced Usage with Templates

The integration supports Home Assistant templates for all string parameters:

```yaml
service: ha_shazamio.search_track
data:
  query: "{{ states('input_text.song_name') }}"
  limit: "{{ states('input_number.search_limit') | int }}"
  language: "{{ states('input_select.language') }}"
```

## Example Automation: Daily Top Tracks

```yaml
automation:
  - alias: "Get Daily Top Tracks"
    trigger:
      - platform: time
        at: "08:00:00"
    action:
      - service: ha_shazamio.top_country_tracks
        data:
          country_code: "{{ states('input_select.country') }}"
          limit: 10
      - wait_for_trigger:
          - platform: event
            event_type: ha_shazamio_response
            event_data:
              service: top_country_tracks
        timeout: "00:00:30"
      - service: notify.persistent_notification
        data:
          title: "Top 10 Tracks Today"
          message: "Received {{ wait.trigger.event.data.data.tracks | length }} tracks"
```

## Support

- **Issues**: [GitHub Issues](https://github.com/iamjoshk/ha_shazamio/issues)
- **ShazamIO Documentation**: [ShazamIO GitHub](https://github.com/shazamio/ShazamIO)

## License

This integration follows the same license as ShazamIO (MIT License).

## Credits

- [ShazamIO](https://github.com/shazamio/ShazamIO) - The underlying Python library
- Home Assistant Community
