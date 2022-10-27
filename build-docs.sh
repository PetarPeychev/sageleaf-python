#!/usr/bin/env bash

# Generate html docs using pdoc.
pdoc3 --html --force --output-dir docs sageleaf
mv ./docs/sageleaf/* ./docs/
rmdir ./docs/sageleaf
