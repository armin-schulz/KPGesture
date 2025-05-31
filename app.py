import logging
import sys

from app_util import setup_logging
from painting import painting
from exploration import exploration
from config import DEFAULT_MODE
from painting_static import painting_static

logger = logging.getLogger(__name__)


def get_mode(args: list[str] | None = None) -> str:
    mode = None
    for arg in args:
        comps = arg.split('=')
        if len(comps) == 2 and comps[0] == 'MODE':
            logger.info(f'Set mode as {comps[1]}.')
            mode = comps[1]
            break
    if mode is None:
        logger.info(f'Can not get value from key MODE. Use default value: {DEFAULT_MODE} ')
        mode = DEFAULT_MODE
    return mode


def main(args):
    mode = get_mode(args)
    match mode:
        case 'painting':
            painting(args)
        case  'exploration':
            exploration()
        case 'painting_static':
            painting_static(args)
        case _:
            logger.error('No mode selected')


if __name__ == '__main__':
    setup_logging()
    main(sys.argv[1:])
