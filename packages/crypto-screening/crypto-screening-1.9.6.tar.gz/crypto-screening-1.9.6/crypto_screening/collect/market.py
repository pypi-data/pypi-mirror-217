# market.py

from dataclasses import dataclass
from typing import Iterable, Dict, Optional, Union, Any, ClassVar

from represent import represent, Modifiers

from crypto_screening.market.screeners.base import BaseScreener
from crypto_screening.dataset import BIDS, ASKS
from crypto_screening.symbols import symbol_to_parts

__all__ = [
    "assets_market_state",
    "AssetsMarketState",
    "validate_assets_market_state_prices_symbol",
    "assets_market_state",
    "assets_market_price",
    "is_symbol_in_market_state_prices",
    "SymbolsMarketState",
    "symbols_market_state"
]

AssetsPrices = Dict[str, Dict[str, Dict[str, float]]]
SymbolsPrices = Dict[str, Dict[str, float]]
Screeners = Union[Iterable[BaseScreener], Dict[str, BaseScreener]]

def is_symbol_in_market_state_prices(
        symbol: str, prices: AssetsPrices, separator: Optional[str] = None
) -> bool:
    """
    Checks if the symbol is in the prices' data.

    :param symbol: The symbol to search.
    :param prices: The price data to process.
    :param separator: The separator of the assets.

    :return: The validation value.
    """

    base, quote = symbol_to_parts(symbol=symbol, separator=separator)

    if base not in prices:
        return False
    # end if

    if quote not in prices[base]:
        return False
    # end if

    return True
# end is_symbol_in_market_state_prices

def validate_assets_market_state_prices_symbol(
        exchange: str,
        symbol: str,
        prices: AssetsPrices,
        separator: Optional[str] = None,
        provider: Optional[Any] = None
) -> None:
    """
    Checks if the symbol is in the prices' data.

    :param exchange: The exchange name.
    :param symbol: The symbol to search.
    :param separator: The separator of the assets.
    :param prices: The price data to process.
    :param provider: The data provider.

    :return: The validation value.
    """

    base, quote = symbol_to_parts(symbol=symbol, separator=separator)

    if exchange not in prices:
        raise ValueError(
            f"exchange '{exchange}' is not found inside the prices of"
            f"{f' of {provider}' if provider is not None else ''}. "
            f"Found exchanges for are: {', '.join(prices.keys())}"
        )
    # end if

    if base not in prices[exchange]:
        raise ValueError(
            f"base asset '{base}' is not found in '{exchange}' prices of"
            f"{f' of {provider}' if provider is not None else ''}. "
            f"Found base '{exchange}' assets are: {', '.join(prices[exchange].keys())}"
        )
    # end if

    if quote not in prices[exchange][base]:
        raise ValueError(
            f"quote asset '{quote}' is not found in the quote "
            f"assets of the '{base}' base asset in the prices"
            f"{f' of {provider}' if provider is not None else ''}. "
            f"Found quote assets for the '{base}' base asset in "
            f"the prices are: {', '.join(prices[exchange][base].keys())}"
        )
    # end if
# end validate_assets_market_state_prices_symbol

def validate_symbols_market_state_prices_symbol(
        exchange: str,
        symbol: str,
        prices: SymbolsPrices,
        provider: Optional[Any] = None
) -> None:
    """
    Checks if the symbol is in the prices' data.

    :param exchange: The exchange name.
    :param symbol: The symbol to search.
    :param prices: The price data to process.
    :param provider: The data provider.

    :return: The validation value.
    """

    if exchange not in prices:
        raise ValueError(
            f"exchange '{exchange}' is not found inside the prices of"
            f"{f' of {provider}' if provider is not None else ''}. "
            f"Found exchanges for are: {', '.join(prices.keys())}"
        )
    # end if

    if symbol not in prices[exchange]:
        raise ValueError(
            f"symbol '{symbol}' is not found in '{exchange}' prices of"
            f"{f' of {provider}' if provider is not None else ''}. "
            f"Found symbols for '{exchange}' prices are: "
            f"{', '.join(prices[exchange].keys())}"
        )
    # end if
# end validate_symbols_market_state_prices_symbol

def assets_market_price(
        exchange: str,
        symbol: str,
        prices: AssetsPrices,
        separator: Optional[str] = None,
        provider: Optional[Any] = None
) -> float:
    """
    Checks if the symbol is in the prices' data.

    :param exchange: The exchange name.
    :param symbol: The symbol to search.
    :param separator: The separator of the assets.
    :param prices: The price data to process.
    :param provider: The data provider.

    :return: The validation value.
    """

    validate_assets_market_state_prices_symbol(
        symbol=symbol, prices=prices, exchange=exchange,
        separator=separator, provider=provider
    )

    base, quote = symbol_to_parts(symbol=symbol, separator=separator)

    return float(prices[exchange][base][quote])
# end assets_market_price

def symbols_market_price(
        exchange: str,
        symbol: str,
        prices: SymbolsPrices,
        provider: Optional[Any] = None
) -> float:
    """
    Checks if the symbol is in the prices' data.

    :param exchange: The exchange name.
    :param symbol: The symbol to search.
    :param prices: The price data to process.
    :param provider: The data provider.

    :return: The validation value.
    """

    validate_symbols_market_state_prices_symbol(
        exchange=exchange, symbol=symbol,
        prices=prices, provider=provider
    )

    return float(prices[exchange][symbol])
# end symbols_market_price

@dataclass(repr=False, slots=True)
@represent
class AssetsMarketState:
    """
    A class to represent the current market state.

    This object contains the state of the market, as Close,
    bids and asks prices of specific assets, gathered from the network.

    attributes:

    - screeners:
        The screener objects to collect the prices of the assets.

    - prices:
        The close price of the assets.

    - bids:
        The bids prices of the assets.

    - asks:
        The asks prices of the assets.

    >>> from crypto_screening.collect.market import AssetsMarketState
    >>>
    >>> state = assets_market_state(["BTC", "ETH", "LTC"], currency="USDT")
    """

    screeners: Screeners
    bids: AssetsPrices
    asks: AssetsPrices

    __modifiers__: ClassVar[Modifiers] = Modifiers(
        excluded=["screeners", "bids", "asks"]
    )

    def __hash__(self) -> int:
        """
        Returns the hash of the object.

        :return: The hash of the object.
        """

        return id(self)
    # end __hash__

    def bid(self, exchange: str, symbol: str, separator: Optional[str] = None) -> float:
        """
        Returns the bid price for the symbol.

        :param exchange: The exchange name.
        :param symbol: The symbol to find its bid price.
        :param separator: The separator of the assets.

        :return: The bid price for the symbol.
        """

        return assets_market_price(
            exchange=exchange, symbol=symbol, prices=self.bids,
            separator=separator, provider=self
        )
    # end bid

    def ask(self, exchange: str, symbol: str, separator: Optional[str] = None) -> float:
        """
        Returns the ask price for the symbol.

        :param exchange: The exchange name.
        :param symbol: The symbol to find its ask price.
        :param separator: The separator of the assets.

        :return: The ask price for the symbol.
        """

        return assets_market_price(
            exchange=exchange, symbol=symbol, prices=self.asks,
            separator=separator, provider=self
        )
    # end ask
# end MarketState

def assets_market_state(
        screeners: Optional[Screeners] = None,
        separator: Optional[str] = None
) -> AssetsMarketState:
    """
    Fetches the prices and relations between the assets.

    :param screeners: The price screeners.
    :param separator: The separator of the assets.

    :return: The prices of the assets.
    """

    bids: AssetsPrices = {}
    asks: AssetsPrices = {}

    for screener in screeners:
        base, quote = symbol_to_parts(
            symbol=screener.symbol, separator=separator
        )

        if len(screener.market) == 0:
            continue
        # end if

        bids.setdefault(screener.exchange, {}).setdefault(base, {}).setdefault(
            quote, screener.market[BIDS][-1]
        )
        asks.setdefault(screener.exchange, {}).setdefault(base, {}).setdefault(
            quote, screener.market[ASKS][-1]
        )
    # end for

    return AssetsMarketState(
        screeners=screeners, bids=bids, asks=asks
    )
# end assets_market_state

@dataclass(repr=False, slots=True)
@represent
class SymbolsMarketState:
    """
    A class to represent the current market state.

    This object contains the state of the market, as Close,
    bids and asks prices of specific assets, gathered from the network.

    attributes:

    - screeners:
        The screener objects to collect the prices of the assets.

    - prices:
        The close price of the assets.

    - bids:
        The bids prices of the assets.

    - asks:
        The asks prices of the assets.

    >>> from crypto_screening.collect.market import AssetsMarketState
    >>>
    >>> state = assets_market_state(["BTC", "ETH", "LTC"], currency="USDT")
    """

    screeners: Screeners
    bids: SymbolsPrices
    asks: SymbolsPrices

    __modifiers__: ClassVar[Modifiers] = Modifiers(
        excluded=["screeners", "bids", "asks"]
    )

    def __hash__(self) -> int:
        """
        Returns the hash of the object.

        :return: The hash of the object.
        """

        return id(self)
    # end __hash__

    def bid(self, exchange: str, symbol: str) -> float:
        """
        Returns the bid price for the symbol.

        :param exchange: The exchange name.
        :param symbol: The symbol to find its bid price.

        :return: The bid price for the symbol.
        """

        return symbols_market_price(
            exchange=exchange, symbol=symbol,
            prices=self.bids, provider=self
        )
    # end bid

    def ask(self, exchange: str, symbol: str) -> float:
        """
        Returns the ask price for the symbol.

        :param exchange: The exchange name.
        :param symbol: The symbol to find its ask price.

        :return: The ask price for the symbol.
        """

        return symbols_market_price(
            exchange=exchange, symbol=symbol,
            prices=self.asks, provider=self
        )
    # end ask
# end SymbolsMarketState

def symbols_market_state(screeners: Optional[Screeners] = None) -> SymbolsMarketState:
    """
    Fetches the prices and relations between the assets.

    :param screeners: The price screeners.

    :return: The prices of the assets.
    """

    bids: SymbolsPrices = {}
    asks: SymbolsPrices = {}

    for screener in screeners:
        if len(screener.market) == 0:
            continue
        # end if

        bids.setdefault(screener.exchange, {}).setdefault(
            screener.symbol, screener.market[BIDS][-1]
        )
        asks.setdefault(screener.exchange, {}).setdefault(
            screener.symbol, screener.market[ASKS][-1]
        )
    # end for

    return SymbolsMarketState(
        screeners=screeners, bids=bids, asks=asks
    )
# end symbols_market_state