# pylint: disable=all
from ugly_events import register

@register("base_event")
def base_event_one():
    print("This is base event 1")

@register("base_event")
def base_event_two():
    print("Base event 2")
