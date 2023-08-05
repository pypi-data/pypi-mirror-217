# -*- coding: utf-8 -*-

from argparse import Namespace
from typing import Callable

from fastapi import FastAPI
from uvicorn import run as uvicorn_run

app = FastAPI()


@app.get("/health")
async def root():
    return {}


def master_main(args: Namespace, printer: Callable[..., None] = print) -> int:
    assert args is not None
    assert printer is not None

    assert isinstance(args.bind, str)
    assert isinstance(args.port, int)
    assert isinstance(args.broker, str)

    uvicorn_run(app, host=args.bind, port=args.port)
    return 0
