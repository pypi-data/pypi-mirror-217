#!/usr/bin/env python3

import asyncio
import importlib
import logging
import time
from contextlib import suppress
from importlib.machinery import SourceFileLoader
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

from aiodocker import Docker
from quart import Quart

from docker_shaper import dynamic
from docker_shaper.utils import fs_changes, read_process_output, watchdog

CONFIG_FILE = Path("~/.docker_shaper/config.py").expanduser()


def log() -> logging.Logger:
    """Logger for this module"""
    return logging.getLogger("docker-shaper.server")


@watchdog
async def print_container_stats(global_state):
    while True:
        try:
            await dynamic.print_container_stats(global_state)
            await asyncio.sleep(global_state.intervals.get("container_stats"), 1)
        except Exception:
            log().exception("Unhandled exception caught!")
            await asyncio.sleep(5)


@watchdog
async def print_state(global_state):
    while True:
        try:
            await dynamic.dump_global_state(global_state)
            await asyncio.sleep(global_state.intervals.get("state", 1))
        except Exception:
            log().exception("Unhandled exception caught!")
            await asyncio.sleep(5)


@watchdog
async def watch_containers(global_state):
    # TODO: also use events to register
    try:
        docker = Docker()
        while True:
            try:
                await dynamic.watch_containers(docker, global_state)
                await asyncio.sleep(global_state.intervals.get("container_update", 1))
            except Exception:
                log().exception("Unhandled exception caught!")
                await asyncio.sleep(5)
    finally:
        await docker.close()


@watchdog
async def watch_images(global_state):
    # TODO: also use events to register
    try:
        docker = Docker()
        while True:
            try:
                await dynamic.watch_images(docker, global_state)
                await asyncio.sleep(global_state.intervals.get("image_update", 1))
            except Exception:
                log().exception("Unhandled exception caught!")
                await asyncio.sleep(5)
    finally:
        await docker.close()


def load_config(path, global_state):
    spec = spec_from_file_location("dynamic_config", path)
    if not (spec and spec.loader):
        raise RuntimeError("Could not load")
    module = module_from_spec(spec)
    print(module)
    # assert module
    # assert isinstance(spec.loader, SourceFileLoader)
    loader: SourceFileLoader = spec.loader
    loader.exec_module(module)
    try:
        module.modify(global_state)
        dynamic.reconfigure(global_state)
    except AttributeError:
        log().warning("File %s does not provide a `modify(global_state)` function")


@watchdog
async def watch_fs_changes(global_state):
    CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
    async for changed_file in fs_changes(
        Path(dynamic.__file__).parent, CONFIG_FILE.parent, timeout=1
    ):
        log().info("file %s changed - reload module", changed_file)
        try:
            if changed_file == Path(dynamic.__file__):
                importlib.reload(dynamic)
            elif changed_file == CONFIG_FILE:
                load_config(CONFIG_FILE, global_state)

        except Exception:
            log().exception("Reloading dynamic part failed!")
            await asyncio.sleep(5)
    assert False


@watchdog
async def handle_docker_events(global_state):
    try:
        docker = Docker()
        async for line in read_process_output("docker events"):
            try:
                await dynamic.handle_docker_event_line(docker, global_state, line)
            except Exception:
                log().exception("Unhandled exception caught!")
                await asyncio.sleep(5)
    finally:
        await docker.close()


@watchdog
async def cleanup(global_state):
    try:
        docker = Docker()
        while True:
            try:
                await dynamic.cleanup(docker, global_state)
                await asyncio.sleep(global_state.intervals.get("cleanup", 3600))
            except Exception:
                log().exception("Unhandled exception caught in cleanup()!")
                await asyncio.sleep(5)
    finally:
        await docker.close()


def no_serve():
    global_state = dynamic.GlobalState()
    load_config(CONFIG_FILE, global_state)
    with suppress(KeyboardInterrupt, BrokenPipeError):
        asyncio.ensure_future(watch_fs_changes(global_state))
        asyncio.ensure_future(print_container_stats(global_state))
        asyncio.ensure_future(print_state(global_state))
        asyncio.ensure_future(watch_containers(global_state))
        asyncio.ensure_future(watch_images(global_state))
        asyncio.ensure_future(handle_docker_events(global_state))
        asyncio.ensure_future(cleanup(global_state))
        asyncio.get_event_loop().run_forever()


def serve():
    """"""
    app = Quart(__name__)
    app.config["TEMPLATES_AUTO_RELOAD"] = True

    global_state = dynamic.GlobalState()
    load_config(CONFIG_FILE, global_state)

    @watchdog
    async def self_destroy():
        await app.terminator.wait()
        print("BOOM")
        app.shutdown()
        asyncio.get_event_loop().stop()
        print("!!!!")

    @app.route("/shutdown")
    def route_shutdown():
        app.terminator.set()
        return "Server shutting down..."

    @app.route("/containers")
    async def route_containers():
        return await dynamic.container_table_html(global_state)

    @app.route("/images")
    async def route_images():
        return await dynamic.image_table_html(global_state)

    @app.route("/", methods=["GET"])
    async def route_dashboard():
        return await dynamic.dashboard(global_state)

    @app.before_serving
    async def create_db_pool():
        asyncio.ensure_future(self_destroy())
        asyncio.ensure_future(watch_fs_changes(global_state))
        # asyncio.ensure_future(print_container_stats(global_state))
        asyncio.ensure_future(print_state(global_state))
        asyncio.ensure_future(watch_containers(global_state))
        asyncio.ensure_future(watch_images(global_state))
        asyncio.ensure_future(handle_docker_events(global_state))
        asyncio.ensure_future(cleanup(global_state))

    app.terminator = asyncio.Event()
    app.run(
        host="0.0.0.0",
        port=5432,
        debug=False,
        use_reloader=False,
        loop=asyncio.get_event_loop(),
    )
