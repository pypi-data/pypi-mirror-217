# waiting.py

import datetime as dt
import time
from dataclasses import dataclass
from typing import (
    Optional, Union, Iterable, ClassVar,
    Generic, TypeVar, Callable, List
)

from represent import represent, Modifiers

from crypto_screening.market.foundation.protocols import (
    BaseScreenerProtocol, BaseMultiScreenerProtocol
)

__all__ = [
    "base_wait_for_update",
    "base_wait_for_initialization",
    "WaitingState",
    "base_wait_for_dynamic_update",
    "base_wait_for_dynamic_initialization"
]

_BaseScreener = TypeVar(
    "_BaseScreener", BaseScreenerProtocol, BaseMultiScreenerProtocol
)

@dataclass(repr=False, slots=True)
@represent
class WaitingState(Generic[_BaseScreener]):
    """A class to represent the waiting state of screener objects."""

    screeners: Iterable[Union[_BaseScreener]]
    start: dt.datetime
    end: dt.datetime
    stop: Optional[bool] = False
    delay: Optional[float] = 0
    count: Optional[int] = 0
    canceled: Optional[bool] = False
    cancel: Optional[Union[float, dt.timedelta, dt.datetime]] = None

    __modifiers__: ClassVar[Modifiers] = Modifiers(
        hidden=["screeners"], properties=["time"]
    )

    @property
    def time(self) -> dt.timedelta:
        """
        Returns the amount of waited time.

        :return: The waiting time.
        """

        return self.end - self.start
    # end time
# end WaitingState

def base_wait_for_dynamic_initialization(
        screeners: Iterable[_BaseScreener],
        stop: Optional[bool] = None,
        delay: Optional[Union[float, dt.timedelta]] = None,
        cancel: Optional[Union[float, dt.timedelta, dt.datetime]] = None,
        gatherer: Callable[[Iterable[_BaseScreener]], List[_BaseScreener]] = None
) -> WaitingState[_BaseScreener]:
    """
    Waits for all the create_screeners to update.

    :param screeners: The create_screeners to wait for them to update.
    :param delay: The delay for the waiting.
    :param stop: The value to stop the screener objects.
    :param cancel: The time to cancel the waiting.
    :param gatherer: The gathering callable to gather the screeners.

    :returns: The total delay.
    """

    if gatherer is None:
        gatherer = list
    # end if

    if cancel is None:
        cancel = 0
    # end if

    if delay is None:
        delay = 0
    # end if

    if isinstance(cancel, (int, float)):
        cancel = dt.timedelta(seconds=cancel)
    # end if

    if isinstance(delay, dt.timedelta):
        delay = delay.total_seconds()
    # end if

    start = dt.datetime.now()
    count = 0
    canceled = False

    while screeners:
        s = time.time()

        gathered_screeners = gatherer(screeners)

        if all(
            len(screener.market) > 0
            for screener in gathered_screeners
        ):
            break
        # end if

        if (
            isinstance(cancel, dt.timedelta) and
            (canceled := ((dt.datetime.now() - start) > cancel))
        ):
            break
        # end if

        count += 1

        e = time.time()

        if isinstance(delay, (int, float)):
            time.sleep(max([delay - (e - s), 0]))
        # end if
    # end while

    if stop:
        for screener in screeners:
            screener.stop()
        # end for
    # end if

    return WaitingState(
        screeners=screeners, delay=delay,
        count=count, end=dt.datetime.now(), start=start,
        cancel=cancel, canceled=canceled
    )
# end base_wait_for_dynamic_initialization

def base_wait_for_initialization(
        *screeners: _BaseScreener,
        stop: Optional[bool] = False,
        delay: Optional[Union[float, dt.timedelta]] = None,
        cancel: Optional[Union[float, dt.timedelta, dt.datetime]] = None,
        gatherer: Callable[[Iterable[_BaseScreener]], List[_BaseScreener]] = None
) -> WaitingState[_BaseScreener]:
    """
    Waits for all the create_screeners to update.

    :param screeners: The create_screeners to wait for them to update.
    :param delay: The delay for the waiting.
    :param stop: The value to stop the screener objects.
    :param cancel: The time to cancel the waiting.
    :param gatherer: The gathering callable to gather the screeners.

    :returns: The total delay.
    """

    return base_wait_for_dynamic_initialization(
        screeners, delay=delay, stop=stop,
        cancel=cancel, gatherer=gatherer
    )
# end base_wait_for_initialization

def base_wait_for_dynamic_update(
        screeners: Iterable[_BaseScreener],
        stop: Optional[bool] = False,
        delay: Optional[Union[float, dt.timedelta]] = None,
        cancel: Optional[Union[float, dt.timedelta, dt.datetime]] = None,
        gatherer: Callable[[Iterable[_BaseScreener]], List[_BaseScreener]] = None
) -> WaitingState[_BaseScreener]:
    """
    Waits for all the create_screeners to update.

    :param screeners: The create_screeners to wait for them to update.
    :param delay: The delay for the waiting.
    :param stop: The value to stop the screener objects.
    :param cancel: The time to cancel the waiting.
    :param gatherer: The gathering callable to gather the screeners.

    :returns: The total delay.
    """

    if cancel is None:
        cancel = 0
    # end if

    if delay is None:
        delay = 0
    # end if

    if isinstance(cancel, (int, float)):
        cancel = dt.timedelta(seconds=cancel)
    # end if

    if isinstance(delay, dt.timedelta):
        delay = delay.total_seconds()
    # end if

    start = dt.datetime.now()
    count = 0
    canceled = False

    wait = base_wait_for_dynamic_initialization(
        screeners, delay=delay, cancel=cancel, stop=stop
    )

    if not screeners:
        return wait
    # end if

    while screeners:
        s = time.time()

        checked_screeners = gatherer(screeners)

        indexes = {
            screener: len(screener.market)
            for screener in checked_screeners
        }

        if (
            isinstance(cancel, dt.timedelta) and
            (canceled := ((dt.datetime.now() - start) > cancel))
        ):
            break
        # end if

        e = time.time()

        if isinstance(delay, (int, float)):
            time.sleep(max([delay - (e - s), 0]))
        # end if

        count += 1

        new_indexes = {
            screener: len(screener.market)
            for screener in checked_screeners
        }

        if indexes == new_indexes:
            break
        # end if
    # end while

    if stop:
        for screener in screeners:
            screener.stop()
        # end for
    # end if

    return WaitingState(
        screeners=screeners, delay=delay,
        count=count, end=dt.datetime.now(), start=start,
        cancel=cancel, canceled=canceled
    )
# end base_wait_for_dynamic_update

def base_wait_for_update(
        *screeners: _BaseScreener,
        stop: Optional[bool] = False,
        delay: Optional[Union[float, dt.timedelta]] = None,
        cancel: Optional[Union[float, dt.timedelta, dt.datetime]] = None,
        gatherer: Callable[[Iterable[_BaseScreener]], List[_BaseScreener]] = None
) -> WaitingState[_BaseScreener]:
    """
    Waits for all the create_screeners to update.

    :param screeners: The create_screeners to wait for them to update.
    :param delay: The delay for the waiting.
    :param stop: The value to stop the screener objects.
    :param cancel: The time to cancel the waiting.
    :param gatherer: The gathering callable to gather the screeners.

    :returns: The total delay.
    """

    return base_wait_for_dynamic_update(
        screeners, delay=delay, stop=stop,
        cancel=cancel, gatherer=gatherer
    )
# end base_wait_for_update