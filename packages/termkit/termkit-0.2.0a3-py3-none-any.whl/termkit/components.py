# SPDX-License-Identifier: BSD-3-Clause
# SPDX-FileCopyrightText: 2023 Thomas Mahé <contact@tmahe.dev>

import argparse
import inspect
import logging
import os
import sys
import typing
from abc import ABC
from pathlib import Path
from typing import Optional, Callable, Union, Dict, Any

import yaml

from termkit.helpers import get_callback_arguments
from termkit.groups import ArgumentGroup, MutuallyExclusiveGroup

from termkit.formatters import TermkitDefaultFormatter
from termkit.arguments import Argument
from termkit.exceptions import TermkitError, InconsistentTypingError


class Component(ABC):
    name: Optional[str]
    help: Optional[str]
    description: Optional[str]


class Termkit(Component):
    _callback: Optional[Callable]
    _childs: typing.List[Component]

    def __init__(self,
                 name: Optional[str] = None,
                 callback: Optional[Callable] = None,
                 description: Optional[str] = None,
                 named_profile: bool = False):

        # Legacy argparse default for prog name
        if name is None:
            name = os.path.basename(sys.argv[0])

        if callback is not None and not inspect.isfunction(callback):
            raise TermkitError("termkit.Command callback must be a function")

        self.description = description

        if description is None:
            self.help = None
        else:
            self.help = description.splitlines()[0]

        self._profile = None
        if named_profile:
            self._profile = ProfileResolver()

        self.name = name

        self._callback = callback
        self._childs = list()

    def add(self, app_or_command: typing.Union[Component, Callable]):
        # Adding sub-app
        if isinstance(app_or_command, Termkit):
            if app_or_command.name == os.path.basename(sys.argv[0]):
                raise TermkitError('cannot add unnamed Termkit application')
            if self._profile:
                app_or_command._profile = ProfileResolver(ctx=self._profile.ctx + [app_or_command.name],
                                                          content=self._profile._content,
                                                          selected=self._profile._selected)
            self._childs.append(app_or_command)

        # Adding command
        elif isinstance(app_or_command, Command):
            self._childs.append(app_or_command)

        # Adding function
        elif inspect.isfunction(app_or_command):
            self._childs.append(Command(name=app_or_command.__name__,
                                        callback=app_or_command))

        # Raise error on incompatible type
        else:
            raise TermkitError(f'cannot add object of type {type(app_or_command)} to Termkit application')

        child_names = [e.name for e in self._childs]
        duplicates = set([e for e in child_names if child_names.count(e) > 1])
        if len(duplicates) > 0:
            self._childs.pop()
            raise TermkitError(f"duplicated command or sub-app name {duplicates} in application '{self.name}'")

    def command(self, name: Optional[str] = None):
        def _decorated_callable(callback: Callable, _name=name):
            if _name is None:
                _name = callback.__name__
            c = Command(name=_name, callback=callback)
            if self._profile:
                c._profile = ProfileResolver(ctx=self._profile.ctx + [_name],
                                             content=self._profile._content,
                                             selected=self._profile._selected)
            self._childs.append(c)
            return callback

        return _decorated_callable

    def callback(self):
        def _decorated_callable(callback: Callable):
            if inspect.isfunction(callback):
                self._callback = callback
            else:
                raise TermkitError(f"cannot set object of type '{type(callback).__name__}' as callback for Termkit application")
            return callback

        return _decorated_callable

    def __call__(self, argcomplete=False, *args, **kwargs):
        parser = TermkitParser(self)

        if argcomplete:  # pragma: nocover
            import argcomplete as _argcomplete
            _argcomplete.autocomplete(parser)

        args = parser.parse_args()

        callbacks = [f for k, f in args.__dict__.items() if "__TERMKIT_CALLBACK_" in k]

        for callback in callbacks:
            callback(**get_callback_arguments(callback, args))

        sys.exit(0)


class Command(Component):
    def __init__(self,
                 name: str,
                 callback: Callable):
        if not inspect.isfunction(callback):
            raise TermkitError("termkit.Command callback must be a function")

        self.name = str(name)
        self._callback = callback
        self._profile = None

        doc = inspect.getdoc(callback)
        if doc is None:
            self.help = ""
            self.description = ""
        else:
            self.help = doc.splitlines()[0]
            self.description = doc


class ProfileResolver:

    @staticmethod
    def get_selected_profile():
        parser = argparse.ArgumentParser(add_help=False)
        parser.add_argument("--profile", default="default", nargs="*")
        args, unk = parser.parse_known_args()
        return args.profile

    def __init__(self, ctx=None, content=None, selected=None):
        self.ctx = ctx
        if self.ctx is None:
            self.ctx = []

        self.app_name = os.path.basename(sys.argv[0])
        self._files = [
            Path.home().joinpath('.config').joinpath(self.app_name).joinpath("profile.yaml"),
            Path.home().joinpath('.config').joinpath(self.app_name).joinpath("profile.yml"),
            Path.cwd().joinpath(f'.{self.app_name}.yaml'),
            Path.cwd().joinpath(f'.{self.app_name}.yml'),
        ]
        if content is not None:
            self._content = content
        else:
            logger = logging.getLogger("termkit.components.ProfileResolver")
            self._content = []
            for file in self._files:
                if os.path.exists(file):
                    try:
                        with open(file, 'r') as f:
                            self._content.append(yaml.safe_load(f.read()))
                    except yaml.YAMLError:
                        logger.warning(f"[WARNING] Unable to parse {file}, profiles would not be imported.")
                        continue

        self._profiles = []
        for e in self._content:
            self._profiles += e.keys()

        self._selected = selected
        if self._selected is None:
            self._selected = self.get_selected_profile()

    def resolve(self, argument_name):
        out = None
        for p in self._selected:
            for f in self._content:
                ctx = f.get(p, {})
                for e in self.ctx:
                    ctx = ctx.get(e, {})
                    for name, value in ctx.items():
                        if name == argument_name:
                            out = value
        return out


class TermkitParser(argparse.ArgumentParser):
    _argument_groups: Dict[Union[ArgumentGroup, MutuallyExclusiveGroup], Any]

    def __init__(self, app: Termkit, *args, **kwargs):
        if not isinstance(app, Component):
            raise TermkitError(f"TermkitParser.app expected object of type [Termkit | Command], {type(app)} provided")

        super().__init__(prog=kwargs.get('prog', app.name), formatter_class=TermkitDefaultFormatter)
        self._positionals.title = "Positional arguments"
        self._optionals.title = "Optional arguments"
        self._required = super(TermkitParser, self).add_argument_group("Required arguments")

        self.description = app.description
        self.help = app.help

        # Re-order groups
        positional_group = self._action_groups.pop()
        self._action_groups.insert(1, positional_group)

        self._depth = kwargs.get("depth", 0)
        self._app = app
        self._argument_groups = dict()
        self._populate()

    @property
    def positionals(self):
        return self._positionals

    @property
    def required(self):
        return self._required

    @property
    def optionals(self):
        return self._optionals

    def _populate(self):
        if isinstance(self._app, Termkit):
            self._populate_termkit_app(app=self._app)
        else:
            self._populate_command(command=self._app)

    def _populate_termkit_app(self, app: Termkit):

        if app._callback is not None:
            command = Command(name=app._callback.__name__, callback=app._callback)
            if self.description is None:
                self.description = command.description
            else:
                self.description += f"\n\n{command.description}"
            self._populate_command(command)

        if len(app._childs) > 0:
            p = self.add_subparsers(title="Commands")

            for child in app._childs:
                p.add_parser(app=child, name=child.name, help=child.help, description=child.description, depth=self._depth+1)

    def _populate_command(self, command: Command):
        self.add_argument(f'__TERMKIT_CALLBACK_{self._depth}', action="store_const", const=command._callback,
                          help=argparse.SUPPRESS)
        if command._profile:
            self.add_argument(f'--profile', metavar="NAME", nargs="+", default="default",
                              help=f"Named profile to use\n(selected: {command._profile._selected})",
                              choices=command._profile._profiles)
        if sys.version_info >= (3, 9):
            type_hints = typing.get_type_hints(command._callback, include_extras=True)
        else:
            type_hints = typing.get_type_hints(command._callback)  # pragma: nocover

        for arg_name, arg_spec in inspect.signature(command._callback).parameters.items():

            if sys.version_info >= (3, 9) and isinstance(typing.get_origin(type_hints.get(arg_name, None)), typing.Annotated.__class__):
                annotated_type, argument = typing.get_args(type_hints.get(arg_name, None))
                if issubclass(type(argument), Argument):
                    if argument.type is not None and annotated_type != argument.type:
                        raise InconsistentTypingError(arg_name, command._callback, annotated_type, argument.type)
                    argument._populate(self, arg_name, annotated_type)
                else:
                    raise TermkitError(f"incompatible object for Termkit command: "
                                       f"'{arg_name}: Annotated[{annotated_type.__name__}, {argument.__class__.__name__}]'")

            elif isinstance(type_hints.get(arg_name, None), Argument):
                type_hints.get(arg_name)._populate(self, arg_name, None)

            elif isinstance(arg_spec.default, Argument):
                type_hint = type_hints.get(arg_name, None)
                if hasattr(arg_spec.default, "type"):
                    if None not in [type_hint, arg_spec.default.type] and arg_spec.default.type != type_hint:
                        raise InconsistentTypingError(arg_name, command._callback, type_hint, arg_spec.default.type)
                arg_spec.default._populate(self, arg_name, type_hints.get(arg_name, None))

            elif arg_spec.default is inspect.Parameter.empty:
                # implicit positional
                _type = type_hints.get(arg_name, str)
                self.positionals.add_argument(arg_name, metavar=arg_name.upper(), type=_type, help="(%(type)s)")
            else:
                # implicit option
                _type = type(arg_spec.default)
                if type_hints.get(arg_name, _type) != _type:
                    raise TermkitError(
                        f"default type mismatch with type hint ({_type.__name__} != {type_hints.get(arg_name).__name__}) for argument '{arg_name}'")
                self.optionals.add_argument(f"--{arg_name}", type=_type, default=arg_spec.default,
                                            metavar=_type.__name__.upper(), help="(default: %(default)s)")

    def add_argument_group(self,
                           title: Optional[str] = None,
                           description: Optional[str] = None,
                           group: Optional[Union[ArgumentGroup, MutuallyExclusiveGroup]] = None):

        if group is None:
            return super(self.__class__, self).add_argument_group(title=title, description=description)

        if group in self._argument_groups.keys():
            return self._argument_groups.get(group)

        parent_group = self

        if isinstance(group, MutuallyExclusiveGroup) and group.parent is not None:
            parent_group = self.add_argument_group(group=group.parent)

        if isinstance(group, MutuallyExclusiveGroup):
            self._argument_groups[group] = parent_group.add_mutually_exclusive_group(required=group.required)

        if isinstance(group, ArgumentGroup):
            self._argument_groups[group] = super(self.__class__, self).add_argument_group(title=group.title,
                                                                                          description=group.description)

        return self._argument_groups[group]


def run(func_or_app: Union[Callable, Termkit],
        argcomplete: bool = False):
    if inspect.isfunction(func_or_app):
        Termkit(name=func_or_app.__name__, callback=func_or_app)(argcomplete=argcomplete)
    elif isinstance(func_or_app, Termkit):
        func_or_app(argcomplete=argcomplete)
    else:
        raise TermkitError(f"cannot run object of type '{type(func_or_app).__name__}'")
