/** A work as the library catalogs it: one edition, one ISBN. Holds are placed on titles. */
export interface Title {
  id: string;
  isbn: string;
  name: string;
  format: "book" | "dvd" | "audiobook";
}

/** One physical copy of a title, with its own barcode. Loans are of items. */
export interface Item {
  id: string;
  titleId: string;
  barcode: string;
  homeBranchId: string;
}
