import type { Hold } from "../holds/hold";
import type { Loan } from "../loans/loan";

/** Persistence abstraction. Each aggregate has one repository; nothing else touches the database. */
export interface Repository<T extends { id: string }> {
  get(id: string): Promise<T | undefined>;
  save(entity: T): Promise<void>;
}

export interface LoanRepository extends Repository<Loan> {
  openLoans(): Promise<Loan[]>;
  returnedSince(since: Date): Promise<Loan[]>;
}

export interface HoldRepository extends Repository<Hold> {
  waitingFor(titleId: string): Promise<Hold[]>;
  ready(): Promise<Hold[]>;
}
