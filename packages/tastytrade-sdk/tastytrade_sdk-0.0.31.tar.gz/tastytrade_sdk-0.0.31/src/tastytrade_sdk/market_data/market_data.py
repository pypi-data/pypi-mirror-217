from typing import List, Callable, Optional

from injector import inject

from tastytrade_sdk.api import Api
from tastytrade_sdk.market_data.streamer_symbol_translation import StreamerSymbolTranslationsFactory
from tastytrade_sdk.market_data.subscription import Subscription
from tastytrade_sdk.market_data.models import Candle, Quote


class MarketData:
    @inject
    def __init__(self, api: Api, streamer_symbol_translations_factory: StreamerSymbolTranslationsFactory):
        self.__api = api
        self.__streamer_symbol_translations_factory = streamer_symbol_translations_factory

    def subscribe(self, symbols: List[str], on_quote: Optional[Callable[[Quote], None]] = None,
                  on_candle: Optional[Callable[[Candle], None]] = None) -> Subscription:
        data = self.__api.get('/quote-streamer-tokens')['data']
        return Subscription(
            data['dxlink-url'],
            data['token'],
            self.__streamer_symbol_translations_factory.create(symbols),
            on_quote,
            on_candle
        )
