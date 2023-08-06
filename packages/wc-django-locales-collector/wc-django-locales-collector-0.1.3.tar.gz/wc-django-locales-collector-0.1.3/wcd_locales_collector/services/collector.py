from typing import List
import codecs
import os
from django.core.management.utils import popen_wrapper
from logging import getLogger
import shutil

from . import pathifier


__all__ = 'collect_locales',

logger = getLogger(__name__)


MSGMERGE_DEFAULT_ARGS = [
    'msgmerge', '-q', '--previous',
]
MSGCAT_DEFAULT_ARGS = [
    'msgcat', '--to-code=utf-8', '--use-first',
]
MSGUNFMT_DEFAULT_ARGS = [
    'msgunfmt',
]


def merge(path_from: str, path_to: str):
    os.makedirs(os.path.dirname(path_to), exist_ok=True)

    if not os.path.exists(path_to):
        shutil.copy(path_from, path_to)

    # Merging all source new occurences.
    r = popen_wrapper(
        MSGMERGE_DEFAULT_ARGS + [path_to, path_from, '-o', path_to],
    )

    if r[2] != 0:
        return r

    # Merging filled source data to an empty new.
    return popen_wrapper(
        MSGCAT_DEFAULT_ARGS + [path_to, path_from, '-o', path_to],
    )


def uncompile(path_from: str, path_to: str):
    _, errors, status = popen_wrapper(
        MSGUNFMT_DEFAULT_ARGS + [path_from, '-o', path_to],
    )

    return os.path.exists(path_to)


def collect_locales(
    modules: List[str],
    result_path: str,
    report_error: lambda *args: logger.warning(*args)
):
    result_path = os.path.abspath(result_path)

    for module in modules:
        path = pathifier.get_module_path(module)

        if not path:
            logger.warning('Module %s not found.' % module)
            continue

        module_path = pathifier.get_module_result_path(module, result_path)

        for root, dirs, files in os.walk(path):
            dir = os.path.join(module_path, root.replace(path, ''))

            rmfiles = []
            pofiles = [file for file in files if file.endswith('.po')]

            if len(pofiles) == 0:
                mofiles = [file for file in files if file.endswith('.mo')]

                for file in mofiles:
                    filepath = os.path.join(root, file)
                    path_to = filepath[:-3] + '.po'
                    result = uncompile(filepath, path_to)

                    if result:
                        pofiles.append(file[:-3] + '.po')
                        rmfiles.append(path_to)

            for file in pofiles:
                file_path = os.path.join(root, file)
                new_path = os.path.join(dir, file)

                _, errors, status = merge(file_path, new_path)

                if status != 0:
                    report_error(errors)

            if len(rmfiles):
                for rmfile in rmfiles:
                    os.unlink(rmfile)
