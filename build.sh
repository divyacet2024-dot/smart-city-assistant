#!/usr/bin/env bash
# Disable Poetry and use pip
unset POETRY_VERSION
export PIP_DISABLE_PIP_VERSION_CHECK=1
pip install -r requirements.txt
