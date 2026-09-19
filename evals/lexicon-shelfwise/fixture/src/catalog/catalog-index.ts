import type { RequestContext } from "../http/context";
import type { Title } from "./title";

/**
 * In-memory search index over titles. Rebuilt at startup and after each
 * catalog import, so searches never touch the database.
 */
export class CatalogIndex {
  private byWord = new Map<string, Set<string>>();

  rebuild(titles: Title[]): void {
    this.byWord.clear();
    for (const t of titles) {
      for (const word of t.name.toLowerCase().split(/\W+/)) {
        if (!this.byWord.has(word)) this.byWord.set(word, new Set());
        this.byWord.get(word)!.add(t.id);
      }
    }
  }

  search(ctx: RequestContext, query: string): string[] {
    const hits = this.byWord.get(query.toLowerCase()) ?? new Set<string>();
    ctx.log("catalog search", { query, hits: hits.size });
    return [...hits];
  }
}
