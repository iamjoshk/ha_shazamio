"""Service handlers for ShazamIO integration - Add-on API client."""
import asyncio
import logging
from typing import Any, Dict
import base64

import aiohttp
from homeassistant.core import HomeAssistant, ServiceCall, ServiceResponse, SupportsResponse

from homeassistant.helpers import template

from .const import (
    DOMAIN,
    EVENT_SHAZAMIO_RESPONSE,
    SERVICE_RECOGNIZE,
    SERVICE_ARTIST_ABOUT,
    SERVICE_TRACK_ABOUT,
    SERVICE_SEARCH_ARTIST,
    SERVICE_SEARCH_TRACK,
    SERVICE_RELATED_TRACKS,
    SERVICE_TOP_WORLD_TRACKS,
    SERVICE_TOP_COUNTRY_TRACKS,
    SERVICE_TOP_CITY_TRACKS,
    SERVICE_TOP_WORLD_GENRE_TRACKS,
    SERVICE_TOP_COUNTRY_GENRE_TRACKS,
    SERVICE_ARTIST_ALBUMS,
    SERVICE_SEARCH_ALBUM,
    SERVICE_LISTENING_COUNTER,
    SERVICE_LISTENING_COUNTER_MANY,
)

_LOGGER = logging.getLogger(__name__)

# Add-on service URL
ADDON_URL = "http://localhost:8099/api"


async def _call_addon_api(endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
    """Call the ShazamIO add-on API."""
    url = f"{ADDON_URL}/{endpoint}"
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(url, json=data, timeout=aiohttp.ClientTimeout(total=60)) as response:
                response.raise_for_status()
                return await response.json()
        except aiohttp.ClientError as err:
            _LOGGER.error(f"Error calling add-on API {endpoint}: {err}")
            raise
        except asyncio.TimeoutError:
            _LOGGER.error(f"Timeout calling add-on API {endpoint}")
            raise


async def async_setup_services(hass: HomeAssistant) -> None:
    """Set up services for ShazamIO integration."""

    async def handle_recognize(call: ServiceCall) -> ServiceResponse:
        """Handle recognize service call."""
        try:
            audio_data = _render_template(hass, call.data.get("audio_data"))
            audio_path = _render_template(hass, call.data.get("audio_path"))
            language = _render_template(hass, call.data.get("language", "en-US"))
            endpoint_country = _render_template(hass, call.data.get("endpoint_country", "GB"))
            
            payload = {
                "language": language,
                "endpoint_country": endpoint_country
            }
            
            if audio_path:
                # Read the file and send as base64 (add-on can't access HA filesystem)
                try:
                    def read_audio_file():
                        with open(audio_path, "rb") as f:
                            return f.read()
                    
                    audio_bytes = await hass.async_add_executor_job(read_audio_file)
                    payload["audio_data"] = base64.b64encode(audio_bytes).decode()
                except FileNotFoundError:
                    _LOGGER.error(f"Audio file not found: {audio_path}")
                    return {}
            elif audio_data:
                # If audio_data is already base64, use it; otherwise encode it
                if isinstance(audio_data, bytes):
                    payload["audio_data"] = base64.b64encode(audio_data).decode()
                else:
                    payload["audio_data"] = audio_data
            else:
                _LOGGER.error("Either audio_data or audio_path must be provided")
                return {}
            
            result = await _call_addon_api("recognize", payload)
            
            # Fire event for backwards compatibility
            hass.bus.async_fire(
                EVENT_SHAZAMIO_RESPONSE,
                {"service": SERVICE_RECOGNIZE, "data": result}
            )
            
            # Return data for response_variable
            return result
            
        except Exception as err:
            _LOGGER.error("Error in recognize service: %s", err)
            return {}

    async def handle_artist_about(call: ServiceCall) -> ServiceResponse:
        """Handle artist_about service call."""
        try:
            payload = {
                "artist_id": int(_render_template(hass, call.data.get("artist_id"))),
                "language": _render_template(hass, call.data.get("language", "en-US")),
                "endpoint_country": _render_template(hass, call.data.get("endpoint_country", "GB")),
                "views": call.data.get("views", []),
                "extend": call.data.get("extend", [])
            }
            
            result = await _call_addon_api("artist_about", payload)
            
            hass.bus.async_fire(
                EVENT_SHAZAMIO_RESPONSE,
                {"service": SERVICE_ARTIST_ABOUT, "data": result}
            )
            
            return result
            
        except Exception as err:
            _LOGGER.error("Error in artist_about service: %s", err)
            return {}

    async def handle_track_about(call: ServiceCall) -> ServiceResponse:
        """Handle track_about service call."""
        try:
            payload = {
                "track_id": int(_render_template(hass, call.data.get("track_id"))),
                "language": _render_template(hass, call.data.get("language", "en-US")),
                "endpoint_country": _render_template(hass, call.data.get("endpoint_country", "GB"))
            }
            
            result = await _call_addon_api("track_about", payload)
            
            hass.bus.async_fire(
                EVENT_SHAZAMIO_RESPONSE,
                {"service": SERVICE_TRACK_ABOUT, "data": result}
            )
            
            return result
            
        except Exception as err:
            _LOGGER.error("Error in track_about service: %s", err)
            return {}

    async def handle_search_artist(call: ServiceCall) -> ServiceResponse:
        """Handle search_artist service call."""
        try:
            payload = {
                "query": _render_template(hass, call.data.get("query")),
                "limit": int(_render_template(hass, call.data.get("limit", 10))),
                "offset": int(_render_template(hass, call.data.get("offset", 0))),
                "language": _render_template(hass, call.data.get("language", "en-US")),
                "endpoint_country": _render_template(hass, call.data.get("endpoint_country", "GB"))
            }
            
            result = await _call_addon_api("search_artist", payload)
            
            hass.bus.async_fire(
                EVENT_SHAZAMIO_RESPONSE,
                {"service": SERVICE_SEARCH_ARTIST, "data": result}
            )
            
            return result
            
        except Exception as err:
            _LOGGER.error("Error in search_artist service: %s", err)
            return {}

    async def handle_search_track(call: ServiceCall) -> ServiceResponse:
        """Handle search_track service call."""
        try:
            payload = {
                "query": _render_template(hass, call.data.get("query")),
                "limit": int(_render_template(hass, call.data.get("limit", 10))),
                "offset": int(_render_template(hass, call.data.get("offset", 0))),
                "language": _render_template(hass, call.data.get("language", "en-US")),
                "endpoint_country": _render_template(hass, call.data.get("endpoint_country", "GB"))
            }
            
            result = await _call_addon_api("search_track", payload)
            
            hass.bus.async_fire(
                EVENT_SHAZAMIO_RESPONSE,
                {"service": SERVICE_SEARCH_TRACK, "data": result}
            )
            
            return result
            
        except Exception as err:
            _LOGGER.error("Error in search_track service: %s", err)
            return {}

    async def handle_related_tracks(call: ServiceCall) -> ServiceResponse:
        """Handle related_tracks service call."""
        try:
            payload = {
                "track_id": int(_render_template(hass, call.data.get("track_id"))),
                "limit": int(_render_template(hass, call.data.get("limit", 20))),
                "offset": int(_render_template(hass, call.data.get("offset", 0))),
                "language": _render_template(hass, call.data.get("language", "en-US")),
                "endpoint_country": _render_template(hass, call.data.get("endpoint_country", "GB"))
            }
            
            result = await _call_addon_api("related_tracks", payload)
            
            hass.bus.async_fire(
                EVENT_SHAZAMIO_RESPONSE,
                {"service": SERVICE_RELATED_TRACKS, "data": result}
            )
            
            return result
            
        except Exception as err:
            _LOGGER.error("Error in related_tracks service: %s", err)
            return {}

    async def handle_top_world_tracks(call: ServiceCall) -> ServiceResponse:
        """Handle top_world_tracks service call."""
        try:
            payload = {
                "limit": int(_render_template(hass, call.data.get("limit", 200))),
                "offset": int(_render_template(hass, call.data.get("offset", 0))),
                "language": _render_template(hass, call.data.get("language", "en-US")),
                "endpoint_country": _render_template(hass, call.data.get("endpoint_country", "GB"))
            }
            
            result = await _call_addon_api("top_world_tracks", payload)
            
            hass.bus.async_fire(
                EVENT_SHAZAMIO_RESPONSE,
                {"service": SERVICE_TOP_WORLD_TRACKS, "data": result}
            )
            
            return result
            
        except Exception as err:
            _LOGGER.error("Error in top_world_tracks service: %s", err)
            return {}

    async def handle_top_country_tracks(call: ServiceCall) -> ServiceResponse:
        """Handle top_country_tracks service call."""
        try:
            payload = {
                "country_code": _render_template(hass, call.data.get("country_code")),
                "limit": int(_render_template(hass, call.data.get("limit", 200))),
                "offset": int(_render_template(hass, call.data.get("offset", 0))),
                "language": _render_template(hass, call.data.get("language", "en-US")),
                "endpoint_country": _render_template(hass, call.data.get("endpoint_country", "GB"))
            }
            
            result = await _call_addon_api("top_country_tracks", payload)
            
            hass.bus.async_fire(
                EVENT_SHAZAMIO_RESPONSE,
                {"service": SERVICE_TOP_COUNTRY_TRACKS, "data": result}
            )
            
            return result
            
        except Exception as err:
            _LOGGER.error("Error in top_country_tracks service: %s", err)
            return {}

    async def handle_top_city_tracks(call: ServiceCall) -> ServiceResponse:
        """Handle top_city_tracks service call."""
        try:
            payload = {
                "country_code": _render_template(hass, call.data.get("country_code")),
                "city_name": _render_template(hass, call.data.get("city_name")),
                "limit": int(_render_template(hass, call.data.get("limit", 200))),
                "offset": int(_render_template(hass, call.data.get("offset", 0))),
                "language": _render_template(hass, call.data.get("language", "en-US")),
                "endpoint_country": _render_template(hass, call.data.get("endpoint_country", "GB"))
            }
            
            result = await _call_addon_api("top_city_tracks", payload)
            
            hass.bus.async_fire(
                EVENT_SHAZAMIO_RESPONSE,
                {"service": SERVICE_TOP_CITY_TRACKS, "data": result}
            )
            
            return result
            
        except Exception as err:
            _LOGGER.error("Error in top_city_tracks service: %s", err)
            return {}

    async def handle_top_world_genre_tracks(call: ServiceCall) -> ServiceResponse:
        """Handle top_world_genre_tracks service call."""
        try:
            payload = {
                "genre": _render_template(hass, call.data.get("genre")),
                "limit": int(_render_template(hass, call.data.get("limit", 100))),
                "offset": int(_render_template(hass, call.data.get("offset", 0))),
                "language": _render_template(hass, call.data.get("language", "en-US")),
                "endpoint_country": _render_template(hass, call.data.get("endpoint_country", "GB"))
            }
            
            result = await _call_addon_api("top_world_genre_tracks", payload)
            
            hass.bus.async_fire(
                EVENT_SHAZAMIO_RESPONSE,
                {"service": SERVICE_TOP_WORLD_GENRE_TRACKS, "data": result}
            )
            
            return result
            
        except Exception as err:
            _LOGGER.error("Error in top_world_genre_tracks service: %s", err)
            return {}

    async def handle_top_country_genre_tracks(call: ServiceCall) -> ServiceResponse:
        """Handle top_country_genre_tracks service call."""
        try:
            payload = {
                "country_code": _render_template(hass, call.data.get("country_code")),
                "genre": _render_template(hass, call.data.get("genre")),
                "limit": int(_render_template(hass, call.data.get("limit", 200))),
                "offset": int(_render_template(hass, call.data.get("offset", 0))),
                "language": _render_template(hass, call.data.get("language", "en-US")),
                "endpoint_country": _render_template(hass, call.data.get("endpoint_country", "GB"))
            }
            
            result = await _call_addon_api("top_country_genre_tracks", payload)
            
            hass.bus.async_fire(
                EVENT_SHAZAMIO_RESPONSE,
                {"service": SERVICE_TOP_COUNTRY_GENRE_TRACKS, "data": result}
            )
            
            return result
            
        except Exception as err:
            _LOGGER.error("Error in top_country_genre_tracks service: %s", err)
            return {}

    async def handle_artist_albums(call: ServiceCall) -> ServiceResponse:
        """Handle artist_albums service call."""
        try:
            payload = {
                "artist_id": int(_render_template(hass, call.data.get("artist_id"))),
                "limit": int(_render_template(hass, call.data.get("limit", 10))),
                "offset": int(_render_template(hass, call.data.get("offset", 0))),
                "language": _render_template(hass, call.data.get("language", "en-US")),
                "endpoint_country": _render_template(hass, call.data.get("endpoint_country", "GB"))
            }
            
            result = await _call_addon_api("artist_albums", payload)
            
            hass.bus.async_fire(
                EVENT_SHAZAMIO_RESPONSE,
                {"service": SERVICE_ARTIST_ALBUMS, "data": result}
            )
            
            return result
            
        except Exception as err:
            _LOGGER.error("Error in artist_albums service: %s", err)
            return {}

    async def handle_search_album(call: ServiceCall) -> ServiceResponse:
        """Handle search_album service call."""
        try:
            payload = {
                "album_id": int(_render_template(hass, call.data.get("album_id"))),
                "language": _render_template(hass, call.data.get("language", "en-US")),
                "endpoint_country": _render_template(hass, call.data.get("endpoint_country", "GB"))
            }
            
            result = await _call_addon_api("search_album", payload)
            
            hass.bus.async_fire(
                EVENT_SHAZAMIO_RESPONSE,
                {"service": SERVICE_SEARCH_ALBUM, "data": result}
            )
            
            return result
            
        except Exception as err:
            _LOGGER.error("Error in search_album service: %s", err)
            return {}

    async def handle_listening_counter(call: ServiceCall) -> ServiceResponse:
        """Handle listening_counter service call."""
        try:
            payload = {
                "track_id": int(_render_template(hass, call.data.get("track_id"))),
                "language": _render_template(hass, call.data.get("language", "en-US")),
                "endpoint_country": _render_template(hass, call.data.get("endpoint_country", "GB"))
            }
            
            result = await _call_addon_api("listening_counter", payload)
            
            hass.bus.async_fire(
                EVENT_SHAZAMIO_RESPONSE,
                {"service": SERVICE_LISTENING_COUNTER, "data": result}
            )
            
            return result
            
        except Exception as err:
            _LOGGER.error("Error in listening_counter service: %s", err)
            return {}

    async def handle_listening_counter_many(call: ServiceCall) -> ServiceResponse:
        """Handle listening_counter_many service call."""
        try:
            track_ids_str = _render_template(hass, call.data.get("track_ids"))
            track_ids = [int(tid.strip()) for tid in track_ids_str.split(",")]
            
            payload = {
                "track_ids": track_ids,
                "language": _render_template(hass, call.data.get("language", "en-US")),
                "endpoint_country": _render_template(hass, call.data.get("endpoint_country", "GB"))
            }
            
            result = await _call_addon_api("listening_counter_many", payload)
            
            hass.bus.async_fire(
                EVENT_SHAZAMIO_RESPONSE,
                {"service": SERVICE_LISTENING_COUNTER_MANY, "data": result}
            )
            
            return result
            
        except Exception as err:
            _LOGGER.error("Error in listening_counter_many service: %s", err)
            return {}

    # Register all services with response support
    hass.services.async_register(
        DOMAIN, SERVICE_RECOGNIZE, handle_recognize, supports_response=SupportsResponse.OPTIONAL
    )
    hass.services.async_register(
        DOMAIN, SERVICE_ARTIST_ABOUT, handle_artist_about, supports_response=SupportsResponse.OPTIONAL
    )
    hass.services.async_register(
        DOMAIN, SERVICE_TRACK_ABOUT, handle_track_about, supports_response=SupportsResponse.OPTIONAL
    )
    hass.services.async_register(
        DOMAIN, SERVICE_SEARCH_ARTIST, handle_search_artist, supports_response=SupportsResponse.OPTIONAL
    )
    hass.services.async_register(
        DOMAIN, SERVICE_SEARCH_TRACK, handle_search_track, supports_response=SupportsResponse.OPTIONAL
    )
    hass.services.async_register(
        DOMAIN, SERVICE_RELATED_TRACKS, handle_related_tracks, supports_response=SupportsResponse.OPTIONAL
    )
    hass.services.async_register(
        DOMAIN, SERVICE_TOP_WORLD_TRACKS, handle_top_world_tracks, supports_response=SupportsResponse.OPTIONAL
    )
    hass.services.async_register(
        DOMAIN, SERVICE_TOP_COUNTRY_TRACKS, handle_top_country_tracks, supports_response=SupportsResponse.OPTIONAL
    )
    hass.services.async_register(
        DOMAIN, SERVICE_TOP_CITY_TRACKS, handle_top_city_tracks, supports_response=SupportsResponse.OPTIONAL
    )
    hass.services.async_register(
        DOMAIN, SERVICE_TOP_WORLD_GENRE_TRACKS, handle_top_world_genre_tracks, supports_response=SupportsResponse.OPTIONAL
    )
    hass.services.async_register(
        DOMAIN, SERVICE_TOP_COUNTRY_GENRE_TRACKS, handle_top_country_genre_tracks, supports_response=SupportsResponse.OPTIONAL
    )
    hass.services.async_register(
        DOMAIN, SERVICE_ARTIST_ALBUMS, handle_artist_albums, supports_response=SupportsResponse.OPTIONAL
    )
    hass.services.async_register(
        DOMAIN, SERVICE_SEARCH_ALBUM, handle_search_album, supports_response=SupportsResponse.OPTIONAL
    )
    hass.services.async_register(
        DOMAIN, SERVICE_LISTENING_COUNTER, handle_listening_counter, supports_response=SupportsResponse.OPTIONAL
    )
    hass.services.async_register(
        DOMAIN, SERVICE_LISTENING_COUNTER_MANY, handle_listening_counter_many, supports_response=SupportsResponse.OPTIONAL
    )


def _render_template(hass: HomeAssistant, value: Any) -> Any:
    """Render template if value is a template string."""
    if value is None:
        return value
    
    if isinstance(value, str) and "{{" in value:
        tmpl = template.Template(value, hass)
        return tmpl.async_render(parse_result=False)
    
    return value

