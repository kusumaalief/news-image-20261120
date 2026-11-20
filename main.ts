// Entry point for the "Sum up 20 November's world news in one image"
// bounty (news-image-20261120). The image is pre-drawn by
// generate_image.py and shipped in this repo as entry.png; this program
// simply copies it to the grader's output directory, byte for byte, so
// both runs produce identical output. Node 22 standard library only.

import { copyFileSync, existsSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const OUTPUT_NAME = "entry.png";
const source = join(here, OUTPUT_NAME);
const outDir = process.env.MAKEFUN_OUTPUT_DIR || "/output";
const target = join(outDir, OUTPUT_NAME);

if (!existsSync(source)) {
  throw new Error(`entry.png not found next to main.ts: ${source}`);
}
mkdirSync(outDir, { recursive: true });
copyFileSync(source, target);
console.log(`wrote ${target}`);
