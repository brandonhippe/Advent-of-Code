import re
import sys
from copy import deepcopy
from pathlib import Path
from typing import Any, Iterable, Optional, Tuple, Callable

import rerun as rr
import rerun.blueprint as rrb
import yaml

sys.path.append(Path(__file__).parent.parent)
from aoc.languages import LANGS


BLUEPRINT_DIR: Path = Path(__file__).parent
BLUEPRINT_YAMLS: dict[str, dict] = {}
LOGGERS = []


def map_to_entity_path(entity_path: list[Any]) -> str:
    """
    Convert a list of entities to an entity path
    """
    if not entity_path or not entity_path[0].startswith("+"):
        entity_path = [""] + entity_path
    return "/".join(map(str, entity_path))


def get_instantiator(k: str) -> Tuple[Optional[Callable], bool]:
    check_mods = [rr, rrb, rrb.components, rrb.views, rrb.archetypes]
    for mod in check_mods:
        if k in dir(mod):
            if isinstance(getattr(mod, k), Callable):
                return getattr(mod, k), False

    m = globals().get(k, None)
    if m and isinstance(m, Callable):
        return m, True
    return None, True


def regex_replace(k: str, **kwargs):
    regex_match = re.search(r"\$\{(.+?)\}", k)
    if not regex_match:
        return k

    name = regex_match.group(1)
    if name in kwargs:
        return k[:regex_match.start()] + kwargs[name] + k[regex_match.end():]
    
    type_instantiator = get_instantiator(k)
    if type_instantiator:
        return type_instantiator()
    
    return k


def construct_bp(iter: Iterable, *args, **kwargs) -> rrb.BlueprintLike | Iterable:
    if not isinstance(iter, Iterable):
        return iter
    
    if isinstance(iter, str):
        iter = regex_replace(iter, **kwargs)
        type_instantiator, include_passed_args = get_instantiator(iter)
        if type_instantiator:
            if include_passed_args:
                return type_instantiator(*args, **kwargs)
            else:
                return type_instantiator()
        return iter
    
    if isinstance(iter, dict):
        return_dict = {}
        return_list = []
        
        for k, v in iter.items():
            del_key = None
            if isinstance(v, dict) and "del_key" in v:
                del_key = v["del_key"]
                del v["del_key"]

            v = construct_bp(v, **kwargs)
            type_instantiator, include_passed_args = get_instantiator(k)
            if type_instantiator:
                if del_key is None:
                    del_key = True
                new_args = []
                new_kwargs = {}
                if include_passed_args:
                    new_args = args[:]
                    new_kwargs = kwargs.copy()

                if isinstance(v, (list, set, tuple)):
                    for v1 in v:
                        if isinstance(v1, dict):
                            new_kwargs.update(v1)
                        else:
                            new_args.append(v1)
                elif isinstance(v, dict):
                    new_kwargs.update(v)
                else:
                    new_args.append(v)

                v = type_instantiator(*new_args, **new_kwargs)

            if del_key:
                if isinstance(v, (list, set, tuple)):
                    return_list.extend(v)
                elif isinstance(v, dict):
                    return_list.extend(v.values())
                else:
                    return_list.append(v)
            else:
                return_dict[k] = v

        if return_list:
            if return_dict:
                return return_list + [return_dict]
            
            if len(return_list) == 1:
                return return_list[0]
            return return_list
        return return_dict

    return_list = []
    for i in iter:
        v = construct_bp(i, **kwargs)
        if isinstance(v, (list, set, tuple)):
            return_list.extend(v)
        else:
            return_list.append(v)

    return return_list


def load_blueprint(filepath: Path, blueprint_dir: Optional[Path]=None, loggers: list[Any]=[], **kwargs) -> Optional[rrb.BlueprintLike]:
    """
    Load a blueprint from yaml file for the rerun viewer
    """
    if blueprint_dir:
        globals()["BLUEPRINT_DIR"] = blueprint_dir

    if loggers:
        globals()["LOGGERS"] = loggers

    if str(filepath) not in BLUEPRINT_YAMLS:
        # self.print(f"Loading blueprint from {filepath}")
        with open(filepath) as f:
            BLUEPRINT_YAMLS[str(filepath)] = yaml.safe_load(f)

    v = construct_bp(deepcopy(BLUEPRINT_YAMLS[str(filepath)]), **kwargs)
    if isinstance(v, list):
        v = v[0]

    return v


def get_language_views(path: Path="", bp_dir: bool=False, **kwargs) -> rrb.BlueprintLike | Iterable:
    """
    Generate blueprint views for all languages
    """
    if bp_dir:
        path = Path(BLUEPRINT_DIR, path)

    views = {}
    for lang in sorted(LANGS.values()):
        if not len(lang):
            continue

        views[lang] = load_blueprint(path, lang=lang.lang, lang_title=lang.lang.title(), **kwargs)

    if not views:
        views = [rrb.TextDocumentView(origin="/", name="No languages found", contents="+ $origin/no-langs")]
    return views


def get_languages_list(path_ext: list[str], **kwargs) -> rrb.BlueprintLike | Iterable:
    """
    Generate a list of entity paths for all languages
    """
    return [map_to_entity_path(["+ $origin", lang] + path_ext) for lang in sorted(LANGS.keys()) if len(LANGS[lang])]


def get_logger_views(path: Path="", bp_dir: bool=False, **kwargs) -> rrb.BlueprintLike | Iterable:
    """
    Generate blueprint views for all loggers
    """
    if bp_dir:
        path = Path(BLUEPRINT_DIR, path)

    views = []
    for logger in LOGGERS:
        views.append(load_blueprint(Path(path, f"{logger.name}.yml"), **kwargs))

    return views
    

__all__ = ["load_blueprint", "get_language_views", "get_languages_list", "get_logger_views"]
