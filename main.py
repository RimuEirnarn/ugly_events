# pylint: disable=all

from ugly_events.manager import dispatch
import events

def main():
    dispatch("base_event")

if __name__ == '__main__':
    main()
