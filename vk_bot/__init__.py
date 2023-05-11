from .events import map_events
from .methods import BotMethod


class Bot(BotMethod):

    def __init__(self, token_community, token_user, db=None):
        super().__init__(token_community, token_user, db=db)

    def run(self):
        for event in self._longpoll.listen():
            for func, messages in zip(*self._map()):
                for message in messages:
                    if map_events.get(message):
                        if not map_events[message](event):
                            break
                else:
                    func(event)

