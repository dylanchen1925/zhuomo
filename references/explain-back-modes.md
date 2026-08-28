# Explain-back modes (agent protocol)

**Interactive default:** one prompt per turn.

| User says | Protocol |
|-----------|------------|
| `Explain-back [[x]]` | Default interactive |
| `Explain-back [[x]] cold` / `先测后读` | Hide Claim until session end |
| `Explain-back [[x]] feynman` | Child persona probes |
| `Promote [[x]] to solid` | Only if `explain_back: passed` |
| `Study continue: domain` | [continuous-study.md](continuous-study.md) |

**Stuck?** → [study-diagnosis.md](study-diagnosis.md)

---

## Default interactive

```
START: read concept → intro one-line → prompt 1 only
EACH REPLY: grade ✅/⚠️/❌ → brief fix → next prompt only
END: verdict passed|partial|fail → update frontmatter → offer Promote
```

| Verdict | Set |
|---------|-----|
| passed | `explain_back: passed`, `reviewed` + `updated`: today |
| partial | `attempted`, `reviewed`, `updated` |
| fail | `attempted`; suggest Revise Claim |

---

## Cold

- Do **not** quote Claim/body before user finishes prompts
- END: reveal missed `###` in Claim; Evidence only if Claim insufficient
- Tier A first pass: prefer cold

**Before cold (study-technical):** if External stale → 外搜 [[slug]] first.

---

## Feynman

- Persona: curious 12-year-old; 1–2 probes per round
- No full Claim dump; passed via feynman counts prompts covered for Promote
- Optional: `保存 feynman 笔记` → `notes/on-concept/<slug>.md`

---

## Ingest prompt quality

3–4 prompts; ≥1 contrast/scenario/trap; each covered in Claim `###`.

Human-facing detail: [REVIEW.md](../REVIEW.md)
