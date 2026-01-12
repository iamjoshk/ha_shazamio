"""Service handlers for ShazamIO integration."""
import asyncio
import logging
from typing import Any

from shazamio import Shazam, GenreMusic
from shazamio.schemas.artists import ArtistQuery
from shazamio.schemas.enums import ArtistView, ArtistExtend

from homeassistant.core import HomeAssistant, ServiceCall
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


async def async_setup_services(hass: HomeAssistant) -> None:
    """Set up services for ShazamIO integration."""

    async def handle_recognize(call: ServiceCall) -> None:
        """Handle recognize service call."""
        try:
            # Render templates
            audio_data = _render_template(hass, call.data.get("audio_data"))
            audio_path = _render_template(hass, call.data.get("audio_path"))
            language = _render_template(hass, call.data.get("language", "en-US"))
            endpoint_country = _render_template(hass, call.data.get("endpoint_country", "GB"))
            
            shazam = Shazam(language=language, endpoint_country=endpoint_country)
            
            if audio_path:
                result = await shazam.recognize(audio_path)
            elif audio_data:
                result = await shazam.recognize(audio_data)
            else:
                _LOGGER.error("Either audio_data or audio_path must be provided")
                return
            
            # Fire event with result
            hass.bus.async_fire(
                EVENT_SHAZAMIO_RESPONSE,
                {"service": SERVICE_RECOGNIZE, "data": result}
            )
            
        except Exception as err:
            _LOGGER.error("Error in recognize service: %s", err)

    async def handle_artist_about(call: ServiceCall) -> None:
        """Handle artist_about service call."""
        try:
            artist_id = int(_render_template(hass, call.data.get("artist_id")))
            language = _render_template(hass, call.data.get("language", "en-US"))
            endpoint_country = _render_template(hass, call.data.get("endpoint_country", "GB"))
            
            # Optional query parameters
            views_list = call.data.get("views", [])
            extend_list = call.data.get("extend", [])
            
            shazam = Shazam(language=language, endpoint_country=endpoint_country)
            
            query = None
            if views_list or extend_list:
                views = [ArtistView(v) for v in views_list] if views_list else []
                extend = [ArtistExtend(e) for e in extend_list] if extend_list else []
                query = ArtistQuery(views=views, extend=extend)
            
            result = await shazam.artist_about(artist_id, query=query)
            
            hass.bus.async_fire(
                EVENT_SHAZAMIO_RESPONSE,
                {"service": SERVICE_ARTIST_ABOUT, "data": result}
            )
            
        except Exception as err:
            _LOGGER.error("Error in artist_about service: %s", err)

    async def handle_track_about(call: ServiceCall) -> None:
        """Handle track_about service call."""
        try:
            track_id = int(_render_template(hass, call.data.get("track_id")))
            language = _render_template(hass, call.data.get("language", "en-US"))
            endpoint_country = _render_template(hass, call.data.get("endpoint_country", "GB"))
            
            shazam = Shazam(language=language, endpoint_country=endpoint_country)
            result = await shazam.track_about(track_id=track_id)
            
            hass.bus.async_fire(
                EVENT_SHAZAMIO_RESPONSE,
                {"service": SERVICE_TRACK_ABOUT, "data": result}
            )
            
        except Exception as err:
            _LOGGER.error("Error in track_about service: %s", err)

    async def handle_search_artist(call: ServiceCall) -> None:
        """Handle search_artist service call."""
        try:
            query = _render_template(hass, call.data.get("query"))
            limit = int(_render_template(hass, call.data.get("limit", 10)))
            offset = int(_render_template(hass, call.data.get("offset", 0)))
            language = _render_template(hass, call.data.get("language", "en-US"))
            endpoint_country = _render_template(hass, call.data.get("endpoint_country", "GB"))
            
            shazam = Shazam(language=language, endpoint_country=endpoint_country)
            result = await shazam.search_artist(query=query, limit=limit, offset=offset)
            
            hass.bus.async_fire(
                EVENT_SHAZAMIO_RESPONSE,
                {"service": SERVICE_SEARCH_ARTIST, "data": result}
            )
            
        except Exception as err:
            _LOGGER.error("Error in search_artist service: %s", err)

    async def handle_search_track(call: ServiceCall) -> None:
        """Handle search_track service call."""
        try:
            query = _render_template(hass, call.data.get("query"))
            limit = int(_render_template(hass, call.data.get("limit", 10)))
            offset = int(_render_template(hass, call.data.get("offset", 0)))
            language = _render_template(hass, call.data.get("language", "en-US"))
            endpoint_country = _render_template(hass, call.data.get("endpoint_country", "GB"))
            
            shazam = Shazam(language=language, endpoint_country=endpoint_country)
            result = await shazam.search_track(query=query, limit=limit, offset=offset)
            
            hass.bus.async_fire(
                EVENT_SHAZAMIO_RESPONSE,
                {"service": SERVICE_SEARCH_TRACK, "data": result}
            )
            
        except Exception as err:
            _LOGGER.error("Error in search_track service: %s", err)

    async def handle_related_tracks(call: ServiceCall) -> None:
        """Handle related_tracks service call."""
        try:
            track_id = int(_render_template(hass, call.data.get("track_id")))
            limit = int(_render_template(hass, call.data.get("limit", 20)))
            offset = int(_render_template(hass, call.data.get("offset", 0)))
            language = _render_template(hass, call.data.get("language", "en-US"))
            endpoint_country = _render_template(hass, call.data.get("endpoint_country", "GB"))
            
            shazam = Shazam(language=language, endpoint_country=endpoint_country)
            result = await shazam.related_tracks(track_id=track_id, limit=limit, offset=offset)
            
            hass.bus.async_fire(
                EVENT_SHAZAMIO_RESPONSE,
                {"service": SERVICE_RELATED_TRACKS, "data": result}
            )
            
        except Exception as err:
            _LOGGER.error("Error in related_tracks service: %s", err)

    async def handle_top_world_tracks(call: ServiceCall) -> None:
        """Handle top_world_tracks service call."""
        try:
            limit = int(_render_template(hass, call.data.get("limit", 200)))
            offset = int(_render_template(hass, call.data.get("offset", 0)))
            language = _render_template(hass, call.data.get("language", "en-US"))
            endpoint_country = _render_template(hass, call.data.get("endpoint_country", "GB"))
            
            shazam = Shazam(language=language, endpoint_country=endpoint_country)
            result = await shazam.top_world_tracks(limit=limit, offset=offset)
            
            hass.bus.async_fire(
                EVENT_SHAZAMIO_RESPONSE,
                {"service": SERVICE_TOP_WORLD_TRACKS, "data": result}
            )
            
        except Exception as err:
            _LOGGER.error("Error in top_world_tracks service: %s", err)

    async def handle_top_country_tracks(call: ServiceCall) -> None:
        """Handle top_country_tracks service call."""
        try:
            country_code = _render_template(hass, call.data.get("country_code"))
            limit = int(_render_template(hass, call.data.get("limit", 200)))
            offset = int(_render_template(hass, call.data.get("offset", 0)))
            language = _render_template(hass, call.data.get("language", "en-US"))
            endpoint_country = _render_template(hass, call.data.get("endpoint_country", "GB"))
            
            shazam = Shazam(language=language, endpoint_country=endpoint_country)
            result = await shazam.top_country_tracks(country_code=country_code, limit=limit, offset=offset)
            
            hass.bus.async_fire(
                EVENT_SHAZAMIO_RESPONSE,
                {"service": SERVICE_TOP_COUNTRY_TRACKS, "data": result}
            )
            
        except Exception as err:
            _LOGGER.error("Error in top_country_tracks service: %s", err)

    async def handle_top_city_tracks(call: ServiceCall) -> None:
        """Handle top_city_tracks service call."""
        try:
            country_code = _render_template(hass, call.data.get("country_code"))
            city_name = _render_template(hass, call.data.get("city_name"))
            limit = int(_render_template(hass, call.data.get("limit", 200)))
            offset = int(_render_template(hass, call.data.get("offset", 0)))
            language = _render_template(hass, call.data.get("language", "en-US"))
            endpoint_country = _render_template(hass, call.data.get("endpoint_country", "GB"))
            
            shazam = Shazam(language=language, endpoint_country=endpoint_country)
            result = await shazam.top_city_tracks(
                country_code=country_code, 
                city_name=city_name, 
                limit=limit, 
                offset=offset
            )
            
            hass.bus.async_fire(
                EVENT_SHAZAMIO_RESPONSE,
                {"service": SERVICE_TOP_CITY_TRACKS, "data": result}
            )
            
        except Exception as err:
            _LOGGER.error("Error in top_city_tracks service: %s", err)

    async def handle_top_world_genre_tracks(call: ServiceCall) -> None:
        """Handle top_world_genre_tracks service call."""
        try:
            genre = _render_template(hass, call.data.get("genre"))
            limit = int(_render_template(hass, call.data.get("limit", 100)))
            offset = int(_render_template(hass, call.data.get("offset", 0)))
            language = _render_template(hass, call.data.get("language", "en-US"))
            endpoint_country = _render_template(hass, call.data.get("endpoint_country", "GB"))
            
            # Convert genre string to GenreMusic enum
            genre_enum = GenreMusic(genre) if isinstance(genre, str) else genre
            
            shazam = Shazam(language=language, endpoint_country=endpoint_country)
            result = await shazam.top_world_genre_tracks(genre=genre_enum, limit=limit, offset=offset)
            
            hass.bus.async_fire(
                EVENT_SHAZAMIO_RESPONSE,
                {"service": SERVICE_TOP_WORLD_GENRE_TRACKS, "data": result}
            )
            
        except Exception as err:
            _LOGGER.error("Error in top_world_genre_tracks service: %s", err)

    async def handle_top_country_genre_tracks(call: ServiceCall) -> None:
        """Handle top_country_genre_tracks service call."""
        try:
            country_code = _render_template(hass, call.data.get("country_code"))
            genre = _render_template(hass, call.data.get("genre"))
            limit = int(_render_template(hass, call.data.get("limit", 200)))
            offset = int(_render_template(hass, call.data.get("offset", 0)))
            language = _render_template(hass, call.data.get("language", "en-US"))
            endpoint_country = _render_template(hass, call.data.get("endpoint_country", "GB"))
            
            # Convert genre string to GenreMusic enum
            genre_enum = GenreMusic(genre) if isinstance(genre, str) else genre
            
            shazam = Shazam(language=language, endpoint_country=endpoint_country)
            result = await shazam.top_country_genre_tracks(
                country_code=country_code, 
                genre=genre_enum, 
                limit=limit, 
                offset=offset
            )
            
            hass.bus.async_fire(
                EVENT_SHAZAMIO_RESPONSE,
                {"service": SERVICE_TOP_COUNTRY_GENRE_TRACKS, "data": result}
            )
            
        except Exception as err:
            _LOGGER.error("Error in top_country_genre_tracks service: %s", err)

    async def handle_artist_albums(call: ServiceCall) -> None:
        """Handle artist_albums service call."""
        try:
            artist_id = int(_render_template(hass, call.data.get("artist_id")))
            limit = int(_render_template(hass, call.data.get("limit", 10)))
            offset = int(_render_template(hass, call.data.get("offset", 0)))
            language = _render_template(hass, call.data.get("language", "en-US"))
            endpoint_country = _render_template(hass, call.data.get("endpoint_country", "GB"))
            
            shazam = Shazam(language=language, endpoint_country=endpoint_country)
            result = await shazam.artist_albums(artist_id=artist_id, limit=limit, offset=offset)
            
            hass.bus.async_fire(
                EVENT_SHAZAMIO_RESPONSE,
                {"service": SERVICE_ARTIST_ALBUMS, "data": result}
            )
            
        except Exception as err:
            _LOGGER.error("Error in artist_albums service: %s", err)

    async def handle_search_album(call: ServiceCall) -> None:
        """Handle search_album service call."""
        try:
            album_id = int(_render_template(hass, call.data.get("album_id")))
            language = _render_template(hass, call.data.get("language", "en-US"))
            endpoint_country = _render_template(hass, call.data.get("endpoint_country", "GB"))
            
            shazam = Shazam(language=language, endpoint_country=endpoint_country)
            result = await shazam.search_album(album_id=album_id)
            
            hass.bus.async_fire(
                EVENT_SHAZAMIO_RESPONSE,
                {"service": SERVICE_SEARCH_ALBUM, "data": result}
            )
            
        except Exception as err:
            _LOGGER.error("Error in search_album service: %s", err)

    async def handle_listening_counter(call: ServiceCall) -> None:
        """Handle listening_counter service call."""
        try:
            track_id = int(_render_template(hass, call.data.get("track_id")))
            language = _render_template(hass, call.data.get("language", "en-US"))
            endpoint_country = _render_template(hass, call.data.get("endpoint_country", "GB"))
            
            shazam = Shazam(language=language, endpoint_country=endpoint_country)
            result = await shazam.listening_counter(track_id=track_id)
            
            hass.bus.async_fire(
                EVENT_SHAZAMIO_RESPONSE,
                {"service": SERVICE_LISTENING_COUNTER, "data": result}
            )
            
        except Exception as err:
            _LOGGER.error("Error in listening_counter service: %s", err)

    async def handle_listening_counter_many(call: ServiceCall) -> None:
        """Handle listening_counter_many service call."""
        try:
            track_ids_str = _render_template(hass, call.data.get("track_ids"))
            track_ids = [int(tid.strip()) for tid in track_ids_str.split(",")]
            language = _render_template(hass, call.data.get("language", "en-US"))
            endpoint_country = _render_template(hass, call.data.get("endpoint_country", "GB"))
            
            shazam = Shazam(language=language, endpoint_country=endpoint_country)
            result = await shazam.listening_counter_many(track_ids=track_ids)
            
            hass.bus.async_fire(
                EVENT_SHAZAMIO_RESPONSE,
                {"service": SERVICE_LISTENING_COUNTER_MANY, "data": result}
            )
            
        except Exception as err:
            _LOGGER.error("Error in listening_counter_many service: %s", err)

    # Register all services
    hass.services.async_register(DOMAIN, SERVICE_RECOGNIZE, handle_recognize)
    hass.services.async_register(DOMAIN, SERVICE_ARTIST_ABOUT, handle_artist_about)
    hass.services.async_register(DOMAIN, SERVICE_TRACK_ABOUT, handle_track_about)
    hass.services.async_register(DOMAIN, SERVICE_SEARCH_ARTIST, handle_search_artist)
    hass.services.async_register(DOMAIN, SERVICE_SEARCH_TRACK, handle_search_track)
    hass.services.async_register(DOMAIN, SERVICE_RELATED_TRACKS, handle_related_tracks)
    hass.services.async_register(DOMAIN, SERVICE_TOP_WORLD_TRACKS, handle_top_world_tracks)
    hass.services.async_register(DOMAIN, SERVICE_TOP_COUNTRY_TRACKS, handle_top_country_tracks)
    hass.services.async_register(DOMAIN, SERVICE_TOP_CITY_TRACKS, handle_top_city_tracks)
    hass.services.async_register(DOMAIN, SERVICE_TOP_WORLD_GENRE_TRACKS, handle_top_world_genre_tracks)
    hass.services.async_register(DOMAIN, SERVICE_TOP_COUNTRY_GENRE_TRACKS, handle_top_country_genre_tracks)
    hass.services.async_register(DOMAIN, SERVICE_ARTIST_ALBUMS, handle_artist_albums)
    hass.services.async_register(DOMAIN, SERVICE_SEARCH_ALBUM, handle_search_album)
    hass.services.async_register(DOMAIN, SERVICE_LISTENING_COUNTER, handle_listening_counter)
    hass.services.async_register(DOMAIN, SERVICE_LISTENING_COUNTER_MANY, handle_listening_counter_many)


def _render_template(hass: HomeAssistant, value: Any) -> Any:
    """Render template if value is a template string."""
    if value is None:
        return value
    
    if isinstance(value, str) and "{{" in value:
        tmpl = template.Template(value, hass)
        return tmpl.async_render(parse_result=False)
    
    return value

