#!/usr/bin/env python3

import re
import tomllib
from argparse import ArgumentParser
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape


def latex_escape(text):
    """From https://stackoverflow.com/questions/16259923/how-can-i-escape-latex-special-characters-inside-django-templates"""
    conv = {
        "&": r"{\&}",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\^{}",
        "\\": r"\textbackslash{}",
        "<": r"\textless{}",
        ">": r"\textgreater{}",
    }

    regex = re.compile(
        "|".join(
            re.escape(str(key))
            for key in sorted(conv.keys(), key=lambda item: -len(item))
        )
    )

    return regex.sub(lambda match: conv[match.group()], text)


def get_parser():
    parser = ArgumentParser(prog="Checklist LaTeX Renderer")
    parser.add_argument("--template-path", type=str, default=".")
    parser.add_argument("--template", type=str, default="checklist.tex.jinja2")
    parser.add_argument("checklist_definition", type=str)

    return parser


def _load_multifile_definition(definition_path):
    section_files = sorted(
        (x for x in definition_path.iterdir() if x.is_file()), key=lambda x: x.name
    )

    with section_files[0].open("rb") as f:
        section = tomllib.load(f)

    checklist_data = {
        "title": section["title"],
        "description": section["description"],
        "sections": section["sections"],
    }

    for section_file in section_files[1:]:
        if section_file.is_file():
            with section_file.open("rb") as f:
                section = tomllib.load(f)

            checklist_data["sections"].extend(section["sections"])

    return checklist_data


def main(args):
    env = Environment(
        loader=FileSystemLoader(args.template_path),
        autoescape=select_autoescape(),
        block_start_string="[%",
        block_end_string="%]",
        variable_start_string="[[",
        variable_end_string="]]",
        comment_start_string="[#",
        comment_end_string="#]",
        trim_blocks=True,
        lstrip_blocks=True,
    )

    env.filters["elatex"] = latex_escape
    template = env.get_template(args.template)

    definition_path = Path(args.checklist_definition)

    if definition_path.is_dir():
        checklist_data = _load_multifile_definition(definition_path)
    else:
        with definition_path.open("rb") as f:
            checklist_data = tomllib.load(f)

    print(template.render(**checklist_data))


if __name__ == "__main__":
    parser = get_parser()
    main(parser.parse_args())
