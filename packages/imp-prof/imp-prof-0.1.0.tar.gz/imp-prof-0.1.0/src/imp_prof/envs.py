import json
import os
import typing
from dataclasses import dataclass

import environs

__date__ = "2022-01-05T13:55:00.00+00:00"
__all__ = ("load_environs",)

D = typing.TypeVar("D")  # default value type
N = typing.TypeVar("N")  # parsed none
T = typing.TypeVar("T")  # generic type
Conf = dict[str, typing.Any]
NoneParser = typing.Union[typing.Callable[[str], N], typing.Type[N]]


def type_name(obj) -> str:
    name = type(obj).__name__
    if "." not in name:
        return name
    return name.split("\\.")[-1]


@dataclass
class ParsedMonad(typing.Generic[T]):
    """Generic result of operation: value or error"""

    val: typing.Union[T, None] = None
    error: typing.Union[Exception, None] = None


class Env(environs.Env):
    __slots__ = ()

    def parse_item(
        self,
        key: str,
        default: D,
        none_parser: typing.Union[NoneParser, None] = None,
    ) -> ParsedMonad[typing.Union[D, N]]:
        """Parse env variable to type given by default"""
        parser_f: typing.Optional[typing.Callable] = none_parser
        if default:
            type_ = type_name(default)
            parser_f = getattr(self, type_, None)
        if parser_f is None:
            return ParsedMonad(error=TypeError(f"cannot parse '{key}' of type {type(default)}"))
        try:
            return ParsedMonad(val=parser_f(key))
        except (ValueError, TypeError) as e:
            return ParsedMonad(error=e)


def list_env_vars(prefix: typing.Optional[str] = None) -> set[str]:
    """
    Parse OS environment variables names

    :param prefix: return only environment variables stating with `namespace` prefix
    :return: parsed variables
    """
    prefix = prefix or ""
    return {k[len(prefix) :] for k in os.environ.keys() if k.startswith(prefix)}


def _parse_by_model(
    env: Env,
    model: Conf,
    none_parser: typing.Union[NoneParser, None] = None,
) -> Conf:
    """
    Try parse each key of model as model value type

    :param env: environ to parse from
    :param model: known data format
    :param none_parser: if defaults values contains none this function will be used to
        parse env-var; if none_parser=None -> defaults of None value will not be parsed
    :return: dict with parsed `key:value` pairs
    """
    setting = {}
    for k, v in model.items():
        if v is None and none_parser is None:
            continue
        parsed_monad = env.parse_item(k, default=v, none_parser=none_parser)
        if not parsed_monad.error:
            setting[k] = parsed_monad.val
    return setting


def _guess_types_parser(env: environs.Env, env_vars: typing.Collection[str]) -> Conf:
    """
    Parse required variables as string and try to cast them into more concrete type with json loads

    :param env: env representation object
    :param env_vars: parse these env_vars
    :return: dict with parsed `key:value` pairs
    """
    setting = {}
    for k in env_vars:
        setting[k] = env(k)
        try:
            setting[k] = json.loads(setting[k])
        except (ValueError, TypeError):
            continue
    return setting


def load_environs(
    model: Conf,
    prefix: typing.Union[None, str] = None,
    none_parser: typing.Union[NoneParser, None] = None,
) -> dict[str, typing.Any]:
    """
    Parse env variables into dictionary, respects types from default

    Flask usage:
        import envs
        app.config.from_mapping(
            envs.load_environs(
                model=app.config,
                prefix="ANKH_",
            )
        )

    :param model: defaults are used as list of keys to parse from ENV, and types of value is used to parse env-var
    :param prefix: parse only variables starting with this prefix
    :param none_parser: if defaults values contains none this function will be used to
        parse env-var; if none_parser=None -> defaults of None value will not be parsed
    :return: parsed name:value pairs
    """
    prefix = prefix or ""
    env = Env(expand_vars=True)
    env.read_env(".env", recurse=False)
    env_namespace_vars = list_env_vars(prefix=prefix)
    with env.prefixed(prefix or ""):
        # parse known typed variables
        setting = _parse_by_model(env, model, none_parser)
        # add unexpected variables
        additional = _guess_types_parser(env, env_vars=env_namespace_vars - setting.keys())
        setting.update(additional)
    return setting
