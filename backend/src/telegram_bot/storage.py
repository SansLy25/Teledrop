import json
from typing import Optional, Dict, Any, cast

from aiogram.fsm.state import State
from aiogram.fsm.storage.base import (
    BaseStorage,
    StorageKey,
    DefaultKeyBuilder,
    StateType,
)
from django.core.cache import cache


class DjangoCacheStorage(BaseStorage):
    def __init__(self):
        self._key_builder = DefaultKeyBuilder()

    def _get_key(self, key: StorageKey, part):
        return self._key_builder.build(key, part)

    async def set_state(
        self,
        key: StorageKey,
        state: StateType = None,
    ) -> None:
        key = self._get_key(key, "state")
        if state is None:
            await cache.adelete(key)
        else:
            await cache.aset(
                key,
                cast(str, state.state if isinstance(state, State) else state),
                timeout=60 * 60,
            )

    async def get_state(
        self,
        key: StorageKey,
    ) -> Optional[str]:
        key = self._get_key(key, "state")
        value = await cache.aget(key)
        if isinstance(value, bytes):
            return value.decode("utf-8")
        return cast(Optional[str], value)

    async def set_data(
        self,
        key: StorageKey,
        data: Dict[str, Any],
    ) -> None:
        key = self._get_key(key, "data")
        if not data:
            await cache.adelete(key)
            return

        await cache.aset(
            key,
            json.dumps(data),
            timeout=60 * 60,
        )

    async def get_data(
        self,
        key: StorageKey,
    ) -> Dict[str, Any]:
        key = self._get_key(key, "data")
        value = await cache.aget(key)
        if value is None:
            return {}
        if isinstance(value, bytes):
            value = value.decode("utf-8")
        return cast(Dict[str, Any], json.loads(value))

    async def close(self) -> None:
        pass
