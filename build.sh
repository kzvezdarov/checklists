#! /bin/bash

set -euxo pipefail

if [[ ! -d "build" ]]; then
  mkdir build
fi

for definition_file in definitions/*; do
  basename="${definition_file##*/}"
  base_filename="${basename%.*}"

  ./render.py "$definition_file" > "$base_filename".tex
  tectonic "$base_filename".tex

  mv "$base_filename".pdf checklists/
  rm "$base_filename".tex
done
