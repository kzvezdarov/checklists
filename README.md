# Checklists

This repository contains a set of scripts, templates, and TOML definitions for generating checklists. The checklists currently defined are
mostly related to the [Falcon BMS](https://www.falcon-bms.com/) simulator. 

Checklists are defined in the TOML format, either as single files, or a directory of files. This is mostly for convenience of maintenance;
in both cases the definition is rendered as a single PDF file.

## Definition Format

The format is as follows:

1. Title header:
  ```toml
  title = "Checklist Title"
  description = "Checklist Description"
  ```
  The header sets the title and description headers which will be printed at the top of each page. For multi-file definitions,
  only the header in the first file (ordered lexicographically) is used.

2. Any number of checklist sections:
  ```toml
  [[sections]]
  title = "Section Title"
  ```
  This sets the title header of an individual section within the checklist definition; e.g. `Engine Start`.

3. Within a section, any number of steps:
  ```toml
  [[sections.steps]]
  label = "Step name"
  value = "Step action"
  ```
  or
  ```toml
  [[sections.steps]]
  title = "Step title"
  ```
  A step can be either a check -> action line, or a single title which acts as a subsection title.

4. Within a step, any number of substeps
  ```toml
  [[sections.steps.substeps]]
  label = "Substep name"
  value = "Substep action"
  ```
  Substeps are indented relative to steps and can only contain check -> action type steps. There can only be one level of
  substeps.

## LaTeX templates

Each definition is used to render a `LaTeX` template that's templated using Jinja2. The LaTeX is adapted from [https://github.com/theovesy/latexfschecklists](https://github.com/theovesy/latexfschecklists)
and rendered using [Tectonic](https://tectonic-typesetting.github.io/en-US/)

## Building

All checklist definitions can be rendered by executing the `build.sh` script, which will place the pdfs in the `checklists` folder.
