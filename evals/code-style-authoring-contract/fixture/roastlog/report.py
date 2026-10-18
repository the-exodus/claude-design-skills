from .log import Roast, RoastLog


def weight_loss(roast: Roast) -> float | None:
    if roast.roasted_weight_g is None:
        return None
    return 1 - roast.roasted_weight_g / roast.green_weight_g


def lines_for(log: RoastLog, day: str) -> list[str]:
    out = []
    for roast in log.on(day):
        loss = weight_loss(roast)
        loss_text = "-" if loss is None else f"{loss:.1%}"
        out.append(f"{roast.charged_at:%H:%M}  {roast.batch_lot:<10} {roast.green_weight_g:>7.0f} g  {loss_text}")
    return out
