#!/usr/bin/env node
// docs 以下の .md / .mdx を走査し、```mermaid```コードブロックを抽出して
// mermaid-cli (mmdc) で構文検証。エラーがあれば詳細を出力し exit 1。

import { promises as fs } from "node:fs";
import path from "node:path";
import os from "node:os";
import { execFile } from "node:child_process";
import { promisify } from "node:util";
import fg from "fast-glob";

const execFileAsync = promisify(execFile);

const ARGS = process.argv.slice(2);

function extractMermaidBlocks(content) {
  const lines = content.split(/\r?\n/);
  const blocks = [];
  let inBlock = false;
  let startLine = 0;
  let buf = [];

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];

    // ```mermaid または ```mermaid { ... } を検出
    if (!inBlock && /^```mermaid(\s|$)/.test(line)) {
      inBlock = true;
      startLine = i + 2; // 1-originかつフェンス直後の行から開始
      buf = [];
      continue;
    }
    if (inBlock && /^```$/.test(line)) {
      // 終了フェンス
      blocks.push({ code: buf.join("\n"), startLine, endLine: i + 1 });
      inBlock = false;
      buf = [];
      continue;
    }
    if (inBlock) buf.push(line);
  }
  return blocks;
}

function resolveMmdcPath() {
  // 明示指定 > ローカルnode_modules/.bin > グローバルPATH
  if (process.env.MERMAID_CLI) return process.env.MERMAID_CLI;
  const local = path.join(process.cwd(), "node_modules", ".bin", process.platform === "win32" ? "mmdc.cmd" : "mmdc");
  return local;
}

async function validateWithMmdc(mermaidCode) {
  const mmdcCmd = resolveMmdcPath();
  const tmpDir = await fs.mkdtemp(path.join(os.tmpdir(), "mmd-"));
  const inFile = path.join(tmpDir, "snippet.mmd");
  const outFile = path.join(tmpDir, "snippet.svg");
  await fs.writeFile(inFile, mermaidCode, "utf8");

  try {
    await execFileAsync(mmdcCmd, ["-i", inFile, "-o", outFile, "--quiet"], {
      timeout: 20000,
      maxBuffer: 1024 * 1024,
    });
    return { ok: true, message: "" };
  } catch (err) {
    const stderr = err?.stderr?.toString?.() || err?.message || "Unknown error from mmdc";
    return { ok: false, message: stderr.trim() };
  } finally {
    try {
      await fs.rm(tmpDir, { recursive: true, force: true });
    } catch {}
  }
}

(async () => {
  // 引数がなければ docs 配下を全走査
  let files = [];
  let displayTarget = "docs";
  if (ARGS.length === 0) {
    const TARGET_DIR = "docs";
    const GLOB_PATTERN = [`${TARGET_DIR.replace(/\/+$/, "")}/**/*.{md,mdx}`];
    files = await fg(GLOB_PATTERN, { dot: false, onlyFiles: true });
  } else {
    // lint-staged からの引数(ファイル/ディレクトリ)を受け取り、
    // md/mdx ファイルのみに限定
    const collected = new Set();
    for (const p of ARGS) {
      try {
        const stat = await fs.stat(p);
        if (stat.isDirectory()) {
          const list = await fg([
            `${p.replace(/\/+$/, "")}/**/*.{md,mdx}`,
          ], { dot: false, onlyFiles: true });
          for (const f of list) collected.add(f);
        } else if (stat.isFile()) {
          if (/\.(md|mdx)$/i.test(p)) collected.add(p);
        }
      } catch {
        // 存在しない/削除済などは無視
      }
    }
    files = [...collected];
    displayTarget = "inputs";
  }
  let totalBlocks = 0;
  let errorCount = 0;
  const reports = [];

  for (const file of files) {
    const content = await fs.readFile(file, "utf8");
    const blocks = extractMermaidBlocks(content);
    if (blocks.length === 0) continue;

    for (const b of blocks) {
      totalBlocks += 1;
      const res = await validateWithMmdc(b.code);
      if (!res.ok) {
        errorCount += 1;
        const firstLine = res.message.split("\n")[0];
        reports.push({ file, line: b.startLine, error: firstLine });
      }
    }
  }

  if (errorCount === 0) {
    console.log(`Mermaid syntax OK: ${displayTarget} (checked ${totalBlocks} block(s))`);
    process.exit(0);
  } else {
    console.error(`Mermaid syntax errors: ${errorCount} block(s) failed\n`);
    const byFile = new Map();
    for (const r of reports) {
      const list = byFile.get(r.file) || [];
      list.push(r);
      byFile.set(r.file, list);
    }
    for (const [file, list] of byFile) {
      console.error(`- ${file}`);
      for (const r of list) {
        console.error(`  L${r.line}: ${r.error}`);
      }
    }
    process.exit(1);
  }
})().catch((e) => {
  console.error("Validator crashed:", e?.stack || e?.message || e);
  process.exit(2);
});
