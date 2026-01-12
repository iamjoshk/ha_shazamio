"""FastAPI application for ShazamIO Add-on."""
import asyncio
import logging
from typing import Optional, List, Any, Dict
import base64

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from shazamio import Shazam, GenreMusic
from shazamio.schemas.artists import ArtistQuery
from shazamio.schemas.enums import ArtistView, ArtistExtend

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="ShazamIO Service", version="1.0.0")


# Request models
class RecognizeRequest(BaseModel):
    audio_data: Optional[str] = None  # Base64 encoded
    audio_path: Optional[str] = None
    language: str = "en-US"
    endpoint_country: str = "GB"


class ArtistAboutRequest(BaseModel):
    artist_id: int
    views: Optional[List[str]] = None
    extend: Optional[List[str]] = None
    language: str = "en-US"
    endpoint_country: str = "GB"


class TrackAboutRequest(BaseModel):
    track_id: int
    language: str = "en-US"
    endpoint_country: str = "GB"


class SearchRequest(BaseModel):
    query: str
    limit: int = 10
    offset: int = 0
    language: str = "en-US"
    endpoint_country: str = "GB"


class TracksRequest(BaseModel):
    limit: int = 200
    offset: int = 0
    language: str = "en-US"
    endpoint_country: str = "GB"


class CountryTracksRequest(BaseModel):
    country_code: str
    limit: int = 200
    offset: int = 0
    language: str = "en-US"
    endpoint_country: str = "GB"


class CityTracksRequest(BaseModel):
    country_code: str
    city_name: str
    limit: int = 200
    offset: int = 0
    language: str = "en-US"
    endpoint_country: str = "GB"


class GenreTracksRequest(BaseModel):
    genre: str
    limit: int = 100
    offset: int = 0
    language: str = "en-US"
    endpoint_country: str = "GB"


class CountryGenreTracksRequest(BaseModel):
    country_code: str
    genre: str
    limit: int = 200
    offset: int = 0
    language: str = "en-US"
    endpoint_country: str = "GB"


class AlbumsRequest(BaseModel):
    artist_id: int
    limit: int = 10
    offset: int = 0
    language: str = "en-US"
    endpoint_country: str = "GB"


class AlbumRequest(BaseModel):
    album_id: int
    language: str = "en-US"
    endpoint_country: str = "GB"


class ListeningCounterRequest(BaseModel):
    track_id: int
    language: str = "en-US"
    endpoint_country: str = "GB"


class ListeningCounterManyRequest(BaseModel):
    track_ids: List[int]
    language: str = "en-US"
    endpoint_country: str = "GB"


class RelatedTracksRequest(BaseModel):
    track_id: int
    limit: int = 20
    offset: int = 0
    language: str = "en-US"
    endpoint_country: str = "GB"


@app.get("/")
async def root():
    """Health check endpoint."""
    return {"status": "ok", "service": "ShazamIO"}


@app.post("/api/recognize")
async def recognize(request: RecognizeRequest) -> Dict[str, Any]:
    """Recognize a track from audio data or file path."""
    try:
        shazam = Shazam(language=request.language, endpoint_country=request.endpoint_country)
        
        if request.audio_path:
            result = await shazam.recognize(request.audio_path)
        elif request.audio_data:
            # Decode base64 audio data
            audio_bytes = base64.b64decode(request.audio_data)
            result = await shazam.recognize(audio_bytes)
        else:
            raise HTTPException(status_code=400, detail="Either audio_data or audio_path must be provided")
        
        return result
    except Exception as e:
        logger.error(f"Error in recognize: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/artist_about")
async def artist_about(request: ArtistAboutRequest) -> Dict[str, Any]:
    """Get information about an artist."""
    try:
        shazam = Shazam(language=request.language, endpoint_country=request.endpoint_country)
        
        query = None
        if request.views or request.extend:
            views = [ArtistView(v) for v in request.views] if request.views else []
            extend = [ArtistExtend(e) for e in request.extend] if request.extend else []
            query = ArtistQuery(views=views, extend=extend)
        
        result = await shazam.artist_about(request.artist_id, query=query)
        return result
    except Exception as e:
        logger.error(f"Error in artist_about: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/track_about")
async def track_about(request: TrackAboutRequest) -> Dict[str, Any]:
    """Get information about a track."""
    try:
        shazam = Shazam(language=request.language, endpoint_country=request.endpoint_country)
        result = await shazam.track_about(track_id=request.track_id)
        return result
    except Exception as e:
        logger.error(f"Error in track_about: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/search_artist")
async def search_artist(request: SearchRequest) -> Dict[str, Any]:
    """Search for artists."""
    try:
        shazam = Shazam(language=request.language, endpoint_country=request.endpoint_country)
        result = await shazam.search_artist(
            query=request.query,
            limit=request.limit,
            offset=request.offset
        )
        return result
    except Exception as e:
        logger.error(f"Error in search_artist: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/search_track")
async def search_track(request: SearchRequest) -> Dict[str, Any]:
    """Search for tracks."""
    try:
        shazam = Shazam(language=request.language, endpoint_country=request.endpoint_country)
        result = await shazam.search_track(
            query=request.query,
            limit=request.limit,
            offset=request.offset
        )
        return result
    except Exception as e:
        logger.error(f"Error in search_track: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/related_tracks")
async def related_tracks(request: RelatedTracksRequest) -> Dict[str, Any]:
    """Get related tracks."""
    try:
        shazam = Shazam(language=request.language, endpoint_country=request.endpoint_country)
        result = await shazam.related_tracks(
            track_id=request.track_id,
            limit=request.limit,
            offset=request.offset
        )
        return result
    except Exception as e:
        logger.error(f"Error in related_tracks: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/top_world_tracks")
async def top_world_tracks(request: TracksRequest) -> Dict[str, Any]:
    """Get top world tracks."""
    try:
        shazam = Shazam(language=request.language, endpoint_country=request.endpoint_country)
        result = await shazam.top_world_tracks(limit=request.limit, offset=request.offset)
        return result
    except Exception as e:
        logger.error(f"Error in top_world_tracks: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/top_country_tracks")
async def top_country_tracks(request: CountryTracksRequest) -> Dict[str, Any]:
    """Get top country tracks."""
    try:
        shazam = Shazam(language=request.language, endpoint_country=request.endpoint_country)
        result = await shazam.top_country_tracks(
            country_code=request.country_code,
            limit=request.limit,
            offset=request.offset
        )
        return result
    except Exception as e:
        logger.error(f"Error in top_country_tracks: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/top_city_tracks")
async def top_city_tracks(request: CityTracksRequest) -> Dict[str, Any]:
    """Get top city tracks."""
    try:
        shazam = Shazam(language=request.language, endpoint_country=request.endpoint_country)
        result = await shazam.top_city_tracks(
            country_code=request.country_code,
            city_name=request.city_name,
            limit=request.limit,
            offset=request.offset
        )
        return result
    except Exception as e:
        logger.error(f"Error in top_city_tracks: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/top_world_genre_tracks")
async def top_world_genre_tracks(request: GenreTracksRequest) -> Dict[str, Any]:
    """Get top world genre tracks."""
    try:
        shazam = Shazam(language=request.language, endpoint_country=request.endpoint_country)
        genre_enum = GenreMusic(request.genre)
        result = await shazam.top_world_genre_tracks(
            genre=genre_enum,
            limit=request.limit,
            offset=request.offset
        )
        return result
    except Exception as e:
        logger.error(f"Error in top_world_genre_tracks: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/top_country_genre_tracks")
async def top_country_genre_tracks(request: CountryGenreTracksRequest) -> Dict[str, Any]:
    """Get top country genre tracks."""
    try:
        shazam = Shazam(language=request.language, endpoint_country=request.endpoint_country)
        genre_enum = GenreMusic(request.genre)
        result = await shazam.top_country_genre_tracks(
            country_code=request.country_code,
            genre=genre_enum,
            limit=request.limit,
            offset=request.offset
        )
        return result
    except Exception as e:
        logger.error(f"Error in top_country_genre_tracks: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/artist_albums")
async def artist_albums(request: AlbumsRequest) -> Dict[str, Any]:
    """Get artist albums."""
    try:
        shazam = Shazam(language=request.language, endpoint_country=request.endpoint_country)
        result = await shazam.artist_albums(
            artist_id=request.artist_id,
            limit=request.limit,
            offset=request.offset
        )
        return result
    except Exception as e:
        logger.error(f"Error in artist_albums: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/search_album")
async def search_album(request: AlbumRequest) -> Dict[str, Any]:
    """Get album information."""
    try:
        shazam = Shazam(language=request.language, endpoint_country=request.endpoint_country)
        result = await shazam.search_album(album_id=request.album_id)
        return result
    except Exception as e:
        logger.error(f"Error in search_album: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/listening_counter")
async def listening_counter(request: ListeningCounterRequest) -> Dict[str, Any]:
    """Get listening counter for a track."""
    try:
        shazam = Shazam(language=request.language, endpoint_country=request.endpoint_country)
        result = await shazam.listening_counter(track_id=request.track_id)
        return result
    except Exception as e:
        logger.error(f"Error in listening_counter: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/listening_counter_many")
async def listening_counter_many(request: ListeningCounterManyRequest) -> List[Dict[str, Any]]:
    """Get listening counters for multiple tracks."""
    try:
        shazam = Shazam(language=request.language, endpoint_country=request.endpoint_country)
        result = await shazam.listening_counter_many(track_ids=request.track_ids)
        return result
    except Exception as e:
        logger.error(f"Error in listening_counter_many: {e}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8099)
