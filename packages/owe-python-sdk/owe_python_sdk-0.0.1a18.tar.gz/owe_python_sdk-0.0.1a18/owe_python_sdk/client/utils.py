from . import Runner


def adapt_runner(RunnerClassExtension: type, config_override: dict={}):
    def __init__(self, *args, **kwargs):
        Runner.__init__(self)
        RunnerClassExtension.__init__(self, *args, **kwargs)

    # Raise Exception if RunnerClassExtension does not have a
    # Config property
    if not hasattr(RunnerClassExtension, "Config"):
        raise AttributeError(f"Runner class '{RunnerClassExtension.__name__}' is missing a Config class")

    # Override the config on the RunnerClassExtension
    for key, val in config_override.items():
        setattr(RunnerClassExtension.Config, key, val)

    AdaptedRunner = type(
        "AdaptedRunner",
        (RunnerClassExtension, Runner),
        {"__init__": __init__}
    )

    return AdaptedRunner