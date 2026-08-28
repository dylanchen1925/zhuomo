# Bootstrap + Adopt vault

## Bootstrap (new vault)

**Trigger:** `Bootstrap: raw …, vault …` optionally `+ ingest: …`

```
1. Create raw/ tree: inbox/, web/, video/, books/, assets/, processed/
2. Wiki skeleton: index, log, overview, help, domain-map, notes/ tree
3. cp templates/AGENTS.md → vault/AGENTS.md — replace {{RAW_PATH}} {{VAULT_PATH}} {{BOOTSTRAP_DATE}}
4. Write ~/.zhuomo/config.json (paths only — no corpus text):
   { "version": 1, "vault_path": "...", "raw_path": "...", "wiki_subdir": "wiki/" }
5. First source on same line → Ingest
6. log.md bootstrap; closing block
```

---

## Adopt (existing Obsidian vault)

**Trigger:** `Adopt vault: <path>`, `接入已有库: <path>`

**Non-destructive** — do not overwrite existing concepts/sources.

```
1. python3 ~/zhuomo/scripts/vault-adopt-check.py <vault>/wiki
   - Exit 0: empty or zhuomo-marked vault → proceed
   - Exit 1: non-empty corpus without zhuomo marker → refuse overwrite; offer merge checklist
2. Ensure wiki/help.md exists (copy template if missing)
3. Merge or create AGENTS.md from templates/AGENTS.md (preserve user edits in tail)
4. Add zhuomo marker file: wiki/.zhuomo-adopted (date + repo version)
5. If overview.md / domain-map.md missing → create from templates; else add row only if user asks
6. Update ~/.zhuomo/config.json paths
7. log.md: adopt | path; closing block
```

### Adopt rules

| Do | Don't |
|----|-------|
| Add help, AGENTS, config | Batch rewrite concept Claim |
| Add missing log.md | Move user files |
| Offer `Lint` after adopt | Delete existing pages |

---

## Config location

`~/.zhuomo/config.json` — version + paths only. Private wiki text never stored here.

Show: `python3 ~/zhuomo/scripts/zhuomo_config.py show`
