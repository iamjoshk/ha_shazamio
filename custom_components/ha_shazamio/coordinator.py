"""DataUpdateCoordinator for ShazamIO integration."""
from datetime import timedelta
import logging

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


class ShazamIODataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from ShazamIO API."""

    def __init__(self, hass: HomeAssistant) -> None:
        """Initialize."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(minutes=30),
        )

    async def _async_update_data(self):
        """Update data via library."""
        # This coordinator is a placeholder for future features that may need polling
        # Currently, all ShazamIO operations are triggered via services
        return {}

