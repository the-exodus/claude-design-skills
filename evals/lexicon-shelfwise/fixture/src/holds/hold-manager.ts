/**
 * Hold lifecycle: placing holds, allocating returned items to the head of a
 * title's hold queue, and lapsing uncollected holds. (lexicon: HoldManager)
 */
import { config } from "../config";
import type { RequestContext } from "../http/context";
import type { NotificationQueue } from "../notifications/notification-queue";
import { requireMember } from "../patrons/patron";
import type { HoldRepository } from "../storage/repository";
import type { Hold } from "./hold";

export class HoldManager {
  constructor(private holds: HoldRepository, private notices: NotificationQueue) {}

  async place(ctx: RequestContext, titleId: string, pickupBranchId: string): Promise<Hold> {
    const patron = requireMember(ctx);
    const hold: Hold = {
      id: crypto.randomUUID(), patronId: patron.id, titleId, pickupBranchId,
      placedAt: ctx.now().toISOString(), status: "waiting",
    };
    await this.holds.save(hold);
    return hold;
  }

  /**
   * Called when a returned item is checked in at the pickup branch of the
   * oldest waiting hold on its title. The pickup window starts here, when the
   * item is checked in at the pickup branch, not when the patron is notified;
   * notices can lag when the notification queue is backed up.
   */
  async markReadyForPickup(ctx: RequestContext, hold: Hold): Promise<void> {
    hold.status = "ready";
    hold.readyAt = ctx.now().toISOString();
    await this.holds.save(hold);
    this.notices.enqueuePickupReady(hold);
  }

  /** Lapses ready holds whose pickup window has passed; the item goes to the next hold. */
  async lapseExpired(ctx: RequestContext): Promise<number> {
    const windowMs = config.holds.pickupWindowDays * 86_400_000;
    let lapsed = 0;
    for (const hold of await this.holds.ready()) {
      if (ctx.now().getTime() - Date.parse(hold.readyAt!) > windowMs) {
        hold.status = "lapsed";
        await this.holds.save(hold);
        lapsed++;
      }
    }
    return lapsed;
  }
}
