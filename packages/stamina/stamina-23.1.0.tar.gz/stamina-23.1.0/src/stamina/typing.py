# SPDX-FileCopyrightText: 2022 Hynek Schlawack <hs@ox.cx>
#
# SPDX-License-Identifier: MIT

from __future__ import annotations

from typing import Protocol


class RetryHook(Protocol):
    """
    A callable that gets called after an attempt has failed and a retry has
    been scheduled.
    """

    def __call__(
        self,
        attempt: int,
        idle_for: float,
        exc: Exception,
        name: str,
        args: tuple[object, ...],
        kwargs: dict[str, object],
    ) -> None:
        ...
