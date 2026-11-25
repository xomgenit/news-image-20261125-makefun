// News-image entry: "The World in One Day" — Wednesday 25 November 2026.
//
// The picture itself is entry.png beside this file. It was drawn in this
// session by render.py (PIL, Noto fonts): a serif broadsheet with a
// masthead naming the day, one big hero story (the CIA/ODNI cyber breach),
// a numbers strip, and 28 more verified stories from 7 regions.
// This program only carries the finished picture to the output folder
// and checks that the copy is whole before it reports success.
//
// Run it with:  mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, existsSync, mkdirSync, readFileSync, statSync } from "node:fs";
import { join } from "node:path";

const outDir = process.env.MAKEFUN_OUTPUT_DIR || "out";
const source = new URL("./entry.png", import.meta.url);
const target = join(outDir, "entry.png");

mkdirSync(outDir, { recursive: true });
copyFileSync(source, target);

const head = readFileSync(target).subarray(0, 8);
const pngMagic = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
if (!head.equals(pngMagic)) {
  throw new Error("entry.png is not a PNG after copying");
}
const bytes = statSync(target).size;
if (bytes > 1048576) {
  throw new Error(`entry.png is ${bytes} bytes, over the 1 MiB gate`);
}
// The gate also caps the picture at 1024 by 1024 pixels; read the size
// straight out of the PNG header (IHDR: width and height at bytes 16-23).
const ihdr = readFileSync(target).subarray(16, 24);
const width = ihdr.readUInt32BE(0);
const height = ihdr.readUInt32BE(4);
if (width > 1024 || height > 1024) {
  throw new Error(`entry.png is ${width}x${height}, over the 1024x1024 gate`);
}
console.log(`entry.png: ${width}x${height}, ${bytes} bytes -> ${target}`);
