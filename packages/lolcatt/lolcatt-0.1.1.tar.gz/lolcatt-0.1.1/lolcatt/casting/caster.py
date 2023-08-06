#!/usr/bin/env python3
import subprocess
import time
from dataclasses import dataclass
from typing import List
from typing import Optional

from catt.api import CattDevice
from catt.api import discover
from catt.cli import get_config_as_dict


@dataclass
class CastState:
    """Dataclass for cast state, encapsulating info dictionaries of a catt controller."""

    cast_info: dict
    info: dict
    is_loading: bool = False


class Caster:
    """
    Class encapsulating the catt.api.CattDevice.

    Provides a simple interface and enables exchange of the CattDevice on the fly.
    """

    CATT_ARGS = []
    CAST_ARGS = ['-f']

    def __init__(self, name_or_alias: str = 'default', update_interval: float = 0.5):
        self._device = None
        self._available_devices = None
        self._catt_call = None
        self._catt_config = get_config_as_dict()
        if name_or_alias == 'default':
            self._device_name = self._catt_config['options'].get('device')
        elif name_or_alias is not None:
            self._device_name = self._catt_config['aliases'].get(name_or_alias, name_or_alias)
        else:
            self._device_name = None

        if self._device_name is not None:
            self._device = CattDevice(self._device_name)

        self._update_interval = update_interval
        self._state_last_updated = time.time()
        self._loading_started = None
        self._is_loading_cast = False
        self._loading_timeout = 8

    def cast(self, url_or_path: str):
        """
        Casts the given url or path to the currently active device.

        :param url_or_path: The url or path to cast.
        """
        if self._catt_call is not None:
            self._catt_call.kill()
        if self._device is None:
            raise ValueError('Can\'t cast: No device selected.')
        self._catt_call = subprocess.Popen(
            [
                'catt',
                *self.CATT_ARGS,
                '-d',
                self._device_name,
                'cast',
                *self.CAST_ARGS,
                url_or_path,
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        self._loading_started = time.time()
        self._is_loading_cast = True

    def get_available_devices(self) -> List[str]:
        """
        Runs Chromecast discovery and returns a list of available CattDevices.

        :return: A list of available CattDevices.
        """
        self._available_devices = discover()
        return self._available_devices

    def change_device(self, name_or_alias: str):
        """
        Changes the currently active device to the given name or alias. If the device is not
        available, a ValueError is raised.

        :param name_or_alias: The name or alias of the device to change to.
        """
        self._device_name = self._catt_config['aliases'].get(name_or_alias, name_or_alias)
        for device in self.get_available_devices():
            if device.name == self._device_name:
                self._device = device
                return
        raise ValueError('Can\'t change device: Device not found.')

    def get_device(self) -> CattDevice:
        """
        Returns the currently active CattDevice.

        :return: The currently active CattDevice.
        """
        return self._device

    def get_device_name(self) -> Optional[str]:
        """
        Returns the name of the currently active CattDevice.

        :return: The name of the currently active CattDevice.
        """
        return self._device_name

    def get_cast_state(self) -> CastState:
        """
        Returns a CastState object encapsulating the info dictionaries of the currently active
        CattDevice.

        :return: A CastState object
        """
        if self._device is None:
            raise ValueError('Can\'t get cast state: No device selected.')

        if time.time() - self._state_last_updated > self._update_interval:
            self._device.controller._update_status()
            self._state_last_updated = time.time()

        if self._is_loading_cast and time.time() - self._loading_started > self._loading_timeout:
            self._loading_started = None
            self._is_loading_cast = False

        return CastState(
            self._device.controller.cast_info, self._device.controller.info, self._is_loading_cast
        )

    def get_update_interval(self) -> float:
        """
        Returns the update interval of the CastState. Determines how often UI elements are need to
        be updated.

        :return: The update interval of the CastState.
        """
        return self._update_interval
