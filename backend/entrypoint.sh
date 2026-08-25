#!/bin/sh
set -e

if [ "$#" -eq 2 ]; then
    prost "$@"
fi

exec uvicorn api.main:app --host 0.0.0.0
