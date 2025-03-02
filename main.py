# pylint: disable=all

from time import sleep
from ugly_events.manager import dispatch
import events

def main():
    dispatch("base_event")
    sleep(2)
    dispatch("base_event")

if __name__ == '__main__':
    main()
