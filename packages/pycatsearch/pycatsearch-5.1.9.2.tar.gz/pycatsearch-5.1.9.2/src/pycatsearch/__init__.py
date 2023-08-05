# coding=utf-8
from __future__ import annotations

import argparse
import platform
import sys
from datetime import datetime, timedelta, timezone

from .catalog import Catalog

__author__ = 'StSav012'
__original_name__ = 'py''cat''search'

try:
    from ._version import __version__
except ImportError:
    __version__ = ''


def _version_tuple(version_string: str) -> tuple[int | str, ...]:
    result: tuple[int | str, ...] = tuple()
    part: str
    for part in version_string.split('.'):
        try:
            result += (int(part),)
        except ValueError:
            # follow `pkg_resources` version 0.6a9: remove dashes to sort letters after digits
            result += (part.replace('-', ''),)
    return result


def _warn_about_outdated_package(package_name: str, package_version: str, release_time: datetime) -> None:
    """ Display a warning about an outdated package a year after the package released """
    if datetime.now(tz=timezone.utc) - release_time > timedelta(days=366):
        import tkinter.messagebox
        tkinter.messagebox.showwarning(
            title='Package Outdated',
            message=f'Please update {package_name} package to {package_version} or newer')


def _make_old_qt_compatible_again() -> None:
    from qtpy import QT6, PYSIDE2
    from qtpy.QtCore import QLibraryInfo, Qt
    from qtpy.QtWidgets import QApplication, QDialog

    def to_iso_format(s: str) -> str:
        if sys.version_info < (3, 11):
            import re
            from typing import Callable

            if s.endswith('Z'):
                # '2011-11-04T00:05:23Z'
                s = s[:-1] + '+00:00'

            def from_iso_datetime(m: re.Match[str]) -> str:
                groups: dict[str, str] = m.groupdict('')
                date: str = f"{m['year']}-{m['month']}-{m['day']}"
                time: str = \
                    f"{groups['hour']:0>2}:{groups['minute']:0>2}:{groups['second']:0>2}.{groups['fraction']:0<6}"
                return date + 'T' + time + groups['offset']

            def from_iso_calendar(m: re.Match[str]) -> str:
                from datetime import date

                groups: dict[str, str] = m.groupdict('')
                date: str = \
                    date.fromisocalendar(year=int(m['year']), week=int(m['week']), day=int(m['dof'])).isoformat()
                time: str = \
                    f"{groups['hour']:0>2}:{groups['minute']:0>2}:{groups['second']:0>2}.{groups['fraction']:0<6}"
                return date + 'T' + time + groups['offset']

            patterns: dict[str, Callable[[re.Match[str]], str]] = {
                # '20111104', '20111104T000523283'
                r'(?P<year>\d{4})(?P<month>\d{2})(?P<day>\d{2})'
                r'(.(?P<hour>\d{2})(?P<minute>\d{2})(?P<second>\d{2})(?P<fraction>\d+)?)?'
                r'(?P<offset>[+\-].+)?': from_iso_datetime,
                # '2011-11-04', '2011-11-04T00:05:23.283', '2011-11-04T00:05:23.283+00:00'
                r'(?P<year>\d{4})-(?P<month>\d{1,2})-(?P<day>\d{1,2})'
                r'(.(?P<hour>\d{1,2}):(?P<minute>\d{1,2}):(?P<second>\d{1,2})(\.(?P<fraction>\d+))?)?'
                r'(?P<offset>[+\-].+)?': from_iso_datetime,
                # '2011-W01-2T00:05:23.283'
                r'(?P<year>\d{4})-W(?P<week>\d{1,2})-(?P<dof>\d{1,2})'
                r'(.(?P<hour>\d{1,2}):(?P<minute>\d{1,2}):(?P<second>\d{1,2})(\.(?P<fraction>\d+))?)?'
                r'(?P<offset>[+\-].+)?': from_iso_calendar,
                # '2011W0102T000523283'
                r'(?P<year>\d{4})-W(?P<week>\d{2})-(?P<dof>\d{2})'
                r'(.(?P<hour>\d{1,2})(?P<minute>\d{1,2})(?P<second>\d{1,2})(?P<fraction>\d+)?)?'
                r'(?P<offset>[+\-].+)?': from_iso_calendar,
            }
            match: re.Match[str] | None
            for p in patterns:
                match = re.fullmatch(p, s)
                if match is not None:
                    s = patterns[p](match)
                    break

        return s

    if PYSIDE2:
        QApplication.exec = QApplication.exec_
        QDialog.exec = QDialog.exec_

    if not QT6:
        QApplication.setAttribute(Qt.ApplicationAttribute.AA_EnableHighDpiScaling)
        QApplication.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps)

    from qtpy import __version__

    if _version_tuple(__version__) < _version_tuple('2.3.1'):
        _warn_about_outdated_package(package_name='QtPy', package_version='2.3.1',
                                     release_time=datetime.fromisoformat(to_iso_format('2023-03-28T23:06:05Z')))
        if QT6:
            QLibraryInfo.LibraryLocation = QLibraryInfo.LibraryPath
    if _version_tuple(__version__) < _version_tuple('2.4.0'):
        # 2.4.0 is not released yet, so no warning until there is the release time
        if not QT6:
            QLibraryInfo.path = lambda *args, **kwargs: QLibraryInfo.location(*args, **kwargs)
            QLibraryInfo.LibraryPath = QLibraryInfo.LibraryLocation


def main() -> int:
    ap: argparse.ArgumentParser = argparse.ArgumentParser(
        allow_abbrev=True,
        description='Yet another implementation of JPL and CDMS spectroscopy catalogs offline search.\n'
                    f'Find more at https://github.com/{__author__}/{__original_name__}.')
    ap.add_argument('catalog', type=str, help='the catalog location to load',
                    nargs=argparse.ZERO_OR_MORE)
    ap_group = ap.add_argument_group(title='Search options',
                                     description='If any of the following arguments specified, a search conducted.')
    ap_group.add_argument('-f''min', '--min-frequency', type=float, help='the lower frequency [MHz] to take')
    ap_group.add_argument('-f''max', '--max-frequency', type=float, help='the upper frequency [MHz] to take')
    ap_group.add_argument('-i''min', '--min-intensity', type=float,
                          help='the minimal intensity [log10(nm²×MHz)] to take')
    ap_group.add_argument('-i''max', '--max-intensity', type=float,
                          help='the maximal intensity [log10(nm²×MHz)] to take')
    ap_group.add_argument('-T', '--temperature', type=float,
                          help='the temperature [K] to calculate the line intensity at, use the catalog intensity if not set')
    ap_group.add_argument('-t', '--tag', '--species-tag', type=int, dest='species_tag',
                          help='a number to match the `species''tag` field')
    ap_group.add_argument('-n', '--any-name-or-formula', type=str,
                          help='a string to match any field used by `any_name` and `any_formula` options')
    ap_group.add_argument('-a', '--anything', type=str, help='a string to match any field at all')
    ap_group.add_argument('--any-name', type=str, help='a string to match the `trivial''name` or the `name` field')
    ap_group.add_argument('--any-formula', type=str,
                          help='a string to match the `structural''formula`, `molecule''symbol`, '
                               '`stoichiometric''formula`, or `isotopolog` field')
    ap_group.add_argument('--InChI-key', '--inchi-key', type=str, dest='inchi_key',
                          help='a string to match the `inchikey` field, '
                               'which contains the IUPAC International Chemical Identifier (InChI™)')
    ap_group.add_argument('--trivial-name', type=str, help='a string to match the `trivial''name` field')
    ap_group.add_argument('--structural-formula', type=str,
                          help='a string to match the `structural''formula` field')
    ap_group.add_argument('--name', type=str, help='a string to match the `name` field')
    ap_group.add_argument('--stoichiometric-formula', type=str,
                          help='a string to match the `stoichiometric''formula` field')
    ap_group.add_argument('--isotopolog', type=str, help='a string to match the `isotopolog` field')
    ap_group.add_argument('--state', type=str, help='a string to match the `state` or `state_html` field')
    ap_group.add_argument('--dof', '--degrees_of_freedom', type=int, dest='degrees_of_freedom',
                          help='0 for atoms, 2 for linear molecules, and 3 for nonlinear molecules')

    args: argparse.Namespace = ap.parse_intermixed_args()

    arg_names: list[str] = ['min_frequency', 'max_frequency', 'min_intensity', 'max_intensity',
                            'temperature', 'species_tag', 'any_name_or_formula', 'anything', 'any_name', 'any_formula',
                            'inchi_key', 'trivial_name', 'structural_formula', 'name', 'stoichiometric_formula',
                            'isotopolog', 'state', 'degrees_of_freedom']
    search_args: dict[str, str | float | int] = dict((arg, getattr(args, arg)) for arg in arg_names
                                                     if getattr(args, arg) is not None)
    if search_args:
        c: Catalog = Catalog(*args.catalog)
        c.print(**search_args)
        return 0

    return main_gui()


def main_gui() -> int:
    ap: argparse.ArgumentParser = argparse.ArgumentParser(
        description='Yet another implementation of JPL and CDMS spectroscopy catalogs offline search.\n'
                    f'Find more at https://github.com/{__author__}/{__original_name__}.')
    ap.add_argument('catalog', type=str, help='the catalog location to load',
                    nargs=argparse.ZERO_OR_MORE)

    try:
        _make_old_qt_compatible_again()

        from . import gui
    except Exception as ex:
        import traceback
        from contextlib import suppress

        traceback.print_exc()

        error_message: str
        if isinstance(ex, SyntaxError):
            error_message = ('Python ' + platform.python_version() + ' is not supported.\n' +
                             'Get a newer Python!')
        elif isinstance(ex, ImportError):
            error_message = ('Module ' + repr(ex.name) +
                             ' is either missing from the system or cannot be loaded for another reason.\n' +
                             'Try to install or reinstall it.')
        else:
            error_message = str(ex)

        try:
            import tkinter
            import tkinter.messagebox
        except ModuleNotFoundError:
            input(error_message)
        else:
            print(error_message, file=sys.stderr)

            root: tkinter.Tk = tkinter.Tk()
            root.withdraw()
            if isinstance(ex, SyntaxError):
                tkinter.messagebox.showerror(title='Syntax Error', message=error_message)
            elif isinstance(ex, ImportError):
                tkinter.messagebox.showerror(title='Package Missing', message=error_message)
            else:
                tkinter.messagebox.showerror(title='Error', message=error_message)
            root.destroy()
        return 1
    else:
        return gui.run()


def download() -> None:
    from . import downloader

    downloader.download()


def async_download() -> None:
    from . import async_downloader

    async_downloader.download()
