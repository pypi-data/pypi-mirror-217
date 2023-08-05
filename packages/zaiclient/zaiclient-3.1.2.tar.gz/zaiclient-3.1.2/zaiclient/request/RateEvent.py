import time
from typing import Union
from zaiclient.request.BaseEvent import BaseEvent


class RateEvent(BaseEvent):

    __default_event_type = "rate"

    def __init__(
        self,
        user_id: str,
        item_id: str,
        rating: Union[float, int],
        timestamp: Union[float, None] = None
    ):

        if not isinstance(user_id, str):
            raise TypeError("User ID must be a string value.")

        if not isinstance(item_id, str):
            raise TypeError("Item ID must be a string value.")

        if not isinstance(rating, ( float, int )):
            raise TypeError("Rating must be a float or integer value.")

        _item_ids = [item_id]
        _event_values = [str(rating)]
        _timestamp = timestamp if timestamp is not None else time.time()

        super().__init__(
            user_id, _item_ids, _timestamp, self.__default_event_type, _event_values
        )
