// Round-trip check: the pattern in each grader file on disk, read back the way a YAML
// single-quoted scalar is read, equals the pattern in the table that test-graders.mjs tried.
// Also catches a frontmatter cut short by three dashes. Run from the repository root.
import { readFileSync, readdirSync } from "node:fs";
import { cases } from "./gen-graders.mjs";

let bad = 0;
for (const [name, c] of Object.entries(cases)) {
  const dir = `evals/${name}/graders`;
  const onDisk = new Set(readdirSync(dir));
  for (const g of c.graders) {
    const f = `${g.name}.md`;
    if (!onDisk.delete(f)) { console.log("missing", name, f); bad++; continue; }
    const text = readFileSync(`${dir}/${f}`, "utf8");
    const fm = text.match(/^---\n([\s\S]*?)\n---\n/);
    if (!fm || !/^type: /m.test(fm[1])) { console.log("frontmatter lacks type (a --- inside it?)", name, f); bad++; }
    if (g.why && g.why.includes("---")) { console.log("--- in comment", name, f); bad++; }
    if (g.pattern) {
      const m = text.match(/^pattern: '(.*)'$/m);
      const back = m && m[1].replace(/''/g, "'");
      if (back !== g.pattern) { console.log("pattern differs", name, f); bad++; }
      new RegExp(back, g.flags ?? "");
    }
  }
  for (const extra of onDisk) { console.log("unexpected file", name, extra); bad++; }
}
console.log(bad ? `${bad} problems` : "grader files match the tested patterns");
