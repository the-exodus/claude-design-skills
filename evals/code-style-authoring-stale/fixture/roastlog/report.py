from .log import Roast, RoastLog


def weight_loss(roast: Roast) -> float:
    return 1 - roast.roasted_weight_g / roast.green_weight_g


def lines_for(log: RoastLog, day: str) -> list[str]:
    out = []
    for roast in log.on(day):
        # A roast still on the cooling tray has no roasted weight yet, so it is left off the report
        # until it is weighed.
        if roast.roasted_weight_g is None:
            continue
        out.append(f"{roast.charged_at:%H:%M}  {roast.batch_lot:<10} {roast.green_weight_g:>7.0f} g  {weight_loss(roast):.1%}")
    return out
