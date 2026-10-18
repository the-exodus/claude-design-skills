"""The permitted firing window, which is defined in site local time."""


def is_permitted(when, cfg):
    """True if `when` (aware, UTC) falls inside the permitted window.

    Both ends of the window are permitted firing times (ADR 0003).
    """
    local = when.astimezone(cfg.zone)
    if local.weekday() not in cfg.window_days:
        return False
    return cfg.window_start <= local.time() <= cfg.window_end
