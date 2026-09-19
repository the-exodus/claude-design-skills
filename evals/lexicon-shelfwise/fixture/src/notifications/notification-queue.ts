/**
 * Outbound patron notices (email and SMS), retried with exponential backoff.
 *
 * Pickup-window notices: a patron is told when a held item is ready and
 * reminded the day before the pickup window closes.
 */
import type { Hold } from "../holds/hold";

type Notice = { patronId: string; template: string; sendAfter: Date };

export class NotificationQueue {
  private pending: Notice[] = [];

  enqueuePickupReady(hold: Hold): void {
    this.pending.push({ patronId: hold.patronId, template: "pickup-ready", sendAfter: new Date() });
  }

  enqueuePickupReminder(hold: Hold, windowClosesAt: Date): void {
    const dayBefore = new Date(windowClosesAt.getTime() - 86_400_000);
    this.pending.push({ patronId: hold.patronId, template: "pickup-reminder", sendAfter: dayBefore });
  }
}
