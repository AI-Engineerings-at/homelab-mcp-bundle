#!/usr/bin/env node
/**
 * secret-scan.mjs — P0-SEC-01 Secret Scanner
 * Checks for secrets/tokens accidentally tracked in git or left in plaintext files.
 * Exit 0 = PASS, Exit 1 = FAIL
 */

import { execSync } from 'child_process';
import { readFileSync, readdirSync, statSync } from 'fs';
import { join, extname } from 'path';

const ROOT = new URL('..', import.meta.url).pathname;
let failures = [];
let warnings = [];

// ── 1. Git-tracked secrets ────────────────────────────────────────────────────
console.log('\n[1/4] Checking git-tracked .env files...');
try {
  const tracked = execSync('git ls-files', { cwd: ROOT }).toString();
  const envFiles = tracked.split('\n').filter(f => f.match(/\.env(\.|$)/i));
  if (envFiles.length > 0) {
    failures.push(`FAIL: .env files tracked in git: ${envFiles.join(', ')}`);
  } else {
    console.log('  ✓ No .env files tracked in git');
  }
} catch (e) {
  warnings.push(`WARN: Could not run git ls-files: ${e.message}`);
}

// ── 2. Secret patterns in staged/committed files ──────────────────────────────
console.log('[2/4] Checking git history for secret patterns...');
const SECRET_PATTERNS = [
  /['\"]?[A-Za-z_]*TOKEN['\"]?\s*[:=]\s*['"]?[A-Za-z0-9_\-\.]{20,}/,
  /['\"]?[A-Za-z_]*PASSWORD['\"]?\s*[:=]\s*['"]?.{6,}/i,
  /['\"]?[A-Za-z_]*SECRET['\"]?\s*[:=]\s*['"]?[A-Za-z0-9_\-\.]{10,}/i,
  /['\"]?[A-Za-z_]*API_KEY['\"]?\s*[:=]\s*['"]?[A-Za-z0-9_\-\.]{16,}/i,
];
try {
  const diff = execSync('git log --all -p --follow -- .env 2>/dev/null || true', { cwd: ROOT }).toString();
  let found = false;
  for (const pat of SECRET_PATTERNS) {
    if (pat.test(diff)) { found = true; break; }
  }
  if (found) {
    warnings.push('WARN: Secret-like patterns found in .env git history — consider git history rewrite if repo goes public');
  } else {
    console.log('  ✓ No secret patterns detected in git log');
  }
} catch (e) {
  warnings.push(`WARN: git log check failed: ${e.message}`);
}

// ── 3. Plaintext secrets in source files ─────────────────────────────────────
console.log('[3/4] Scanning source files for hardcoded secrets...');
const SCAN_EXTS = ['.py', '.js', '.mjs', '.ts', '.sh', '.yaml', '.yml', '.json'];
const SKIP_DIRS = ['node_modules', '.git', '__pycache__', 'venv', '.venv', 'evidence'];

function scanDir(dir) {
  let items;
  try { items = readdirSync(dir); } catch { return; }
  for (const item of items) {
    if (SKIP_DIRS.includes(item)) continue;
    const full = join(dir, item);
    try {
      const st = statSync(full);
      if (st.isDirectory()) { scanDir(full); continue; }
      if (!SCAN_EXTS.includes(extname(item))) continue;
      const content = readFileSync(full, 'utf8');
      // Look for clearly hardcoded tokens (long alphanum strings after = or :)
      const lines = content.split('\n');
      lines.forEach((line, i) => {
        // Skip comments and template placeholders
        if (line.trim().startsWith('#') || line.trim().startsWith('//')) return;
        if (line.includes('REDACTED') || line.includes('YOUR_') || line.includes('<')) return;
        for (const pat of SECRET_PATTERNS) {
          if (pat.test(line)) {
            warnings.push(`WARN: Possible secret in ${full.replace(ROOT,'')}:${i+1}`);
          }
        }
      });
    } catch { /* skip unreadable */ }
  }
}
scanDir(ROOT);
console.log('  ✓ Source file scan complete');

// ── 4. .gitignore coverage ───────────────────────────────────────────────────
console.log('[4/4] Checking .gitignore coverage...');
try {
  const gi = readFileSync(join(ROOT, '.gitignore'), 'utf8');
  const required = ['.env', '*.env', 'secrets/', 'credentials/'];
  const missing = required.filter(r => !gi.includes(r));
  if (missing.length > 0) {
    failures.push(`FAIL: .gitignore missing entries: ${missing.join(', ')}`);
  } else {
    console.log('  ✓ .gitignore covers required patterns');
  }
} catch {
  failures.push('FAIL: No .gitignore found');
}

// ── Result ───────────────────────────────────────────────────────────────────
console.log('\n══════════════════════════════════════');
if (warnings.length > 0) {
  console.log('\nWARNINGS:');
  warnings.forEach(w => console.log(' ', w));
}
if (failures.length > 0) {
  console.log('\nFAILURES:');
  failures.forEach(f => console.log(' ', f));
  console.log('\nResult: ❌ FAIL\n');
  process.exit(1);
} else {
  console.log('\nResult: ✅ PASS\n');
  process.exit(0);
}
