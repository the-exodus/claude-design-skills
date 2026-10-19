import math

from .log import Roast, RoastLog


def weight_loss(roast: Roast) -> float | None:
    if roast.roasted_weight_g is None:
        return None
    return 1 - roast.roasted_weight_g / roast.green_weight_g


def development_ratio(roast: Roast) -> int | None:
    if roast.first_crack_at is None or roast.dropped_at is None:
        return None
    development = (roast.dropped_at - roast.first_crack_at).total_seconds()
    total = (roast.dropped_at - roast.charged_at).total_seconds()
    # Floored, not rounded: the roaster's own screen floors, and the printed report is held up against it.
    return math.floor(development * 100 / total)


def lines_for(log: RoastLog, day: str) -> list[str]:
    out = []
    for roast in log.on(day):
        loss = weight_loss(roast)
        loss_text = "-" if loss is None else f"{loss:.1%}"
        ratio = development_ratio(roast)
        ratio_text = "-" if ratio is None else f"{ratio}%"
        out.append(f"{roast.charged_at:%H:%M}  {roast.batch_lot:<10} {roast.green_weight_g:>7.0f} g  {loss_text:>5}  {ratio_text:>4}")
    return out
