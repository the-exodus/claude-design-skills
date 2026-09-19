/**
 * Runtime configuration, loaded from shelfwise.config.json at startup.
 * Every key is documented for library administrators in docs/configuration.md.
 */
export interface Config {
  loans: {
    loanPeriodDays: number;
    gracePeriodDays: number;
    maxRenewals: number;
    maxExtensionDays: number;
  };
  fines: { dailyRateCents: number; capCents: number };
  holds: {
    /**
     * Days a patron has to collect a ready hold. Changing the default has
     * history; ask the circulation team before touching it.
     */
    pickupWindowDays: number;
  };
  reconciler: { sweepCron: string };
}

export const defaults: Config = {
  loans: { loanPeriodDays: 21, gracePeriodDays: 2, maxRenewals: 3, maxExtensionDays: 7 },
  fines: { dailyRateCents: 25, capCents: 1000 },
  holds: { pickupWindowDays: 7 },
  reconciler: { sweepCron: "0 3 * * *" },
};

export let config: Config = defaults;

export function loadConfig(overrides: Partial<Config>): void {
  config = { ...defaults, ...overrides } as Config;
}
