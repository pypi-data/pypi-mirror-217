import json
import pathlib
import timeit
from typing import List

from cloudspec import CloudSpec


def __init__(hub):
    hub.pop.sub.add(dyne_name="tool")
    hub.pop.sub.load_subdirs(hub.tool, recurse=True)
    hub.pop.sub.load_subdirs(hub.cloudspec, recurse=True)


def cli(hub):
    """
    Validate json from the cli
    """
    hub.pop.sub.add(dyne_name="output")
    hub.pop.config.load(["cloudspec", "rend", "pop_create"], cli="cloudspec")

    with open(hub.OPT.cloudspec.input_file, "w+") as fh:
        data = json.load(fh)

    if hub.SUBPARSER == "validate":
        validated_spec = CloudSpec(**data)
        hub.output[hub.OPT.rend.output].display(dict(validated_spec))
    elif hub.SUBPARSER == "create":
        root_directory = pathlib.Path(hub.OPT.pop_create.directory)
        ctx = hub.pop_create.idem_cloud.init.context(
            hub.pop_create.init.context(), root_directory
        )
        ctx.cloud_spec = data
        hub.cloudspec.init.run(ctx, root_directory, hub.OPT.cloudspec.create_plugins)
    else:
        hub.log.error(f"Unknown subparser: {hub.SUBPARSER}")


def run(
    hub,
    ctx,
    root_directory: pathlib.Path,
    create_plugins: List[str],
):
    start_time = timeit.default_timer()

    # Run through all external customization before running create plugin
    for customize_plugin in hub.cloudspec.customize._loaded:
        try:
            print(f"Running customization with plugin: {customize_plugin}")
            hub.cloudspec.customize[customize_plugin].run(ctx)
        except Exception as customization_err:
            hub.log.error(
                f"Failed to customize using {customize_plugin}: {customization_err}"
            )

    for create_plugin in create_plugins:
        try:
            hub.log.info(f"Running create plugin: {create_plugin}")
            hub.cloudspec.create[create_plugin].run(ctx, root_directory)
        except Exception as e:
            hub.log.error(f"Failed to run create plugin: {create_plugin}")
            hub.log.error(e)
            raise
    print(f"Total Duration: {timeit.default_timer() - start_time} seconds")
