from vk_api.longpoll import VkEventType
from .constants import *


def message_new(event):
    if event.type == VkEventType.MESSAGE_NEW:
        return True


def message_me(event):
    if event.to_me:
        return True


map_events = {
    MESSAGE_NEW: message_new,
    MESSAGE_ME: message_me,
}
