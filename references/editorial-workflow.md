# Editorial workflow

## Audience and voice

Write for complete AI beginners and curious non-technical readers.

- Sound like a knowledgeable friend.
- Use gentle humor and a slightly absurd visual idea.
- Do not use stale memes, hostile jokes, ridicule, or fast-expiring internet slang.
- Never explain one unexplained term with another unexplained term.
- Expand an English abbreviation on first use when it helps comprehension.
- Prefer concrete verbs and everyday objects over abstract nouns.

## Accuracy rules

1. Treat course notes as clues, not ground truth.
2. Verify unstable or product-specific claims with current official documentation or primary sources.
3. State the scope: generic concept, vendor implementation, or a specific product feature.
4. Do not turn a useful analogy into a literal definition.
5. Flag simplifications that would create a wrong mental model.
6. Avoid predictions, rankings, or product lists unless they are necessary and verified at drafting time.

Example: do not define a Codex Skill as “a system prompt.” A safer beginner explanation is that it is a reusable instruction package whose core is normally a `SKILL.md` file and which may include scripts, references, and assets. “Employee handbook” is an analogy, not the technical definition.

## Notes-mode selection format

```markdown
本期共同主题：<one short sentence>

| 类型 | 名词 | 为什么值得讲 | 与本期的关系 |
|---|---|---|---|
| 主选 1 | ... | ... | ... |
| 主选 2 | ... | ... | ... |
| 主选 3 | ... | ... | ... |
| 主选 4 | ... | ... | ... |
| 主选 5 | ... | ... | ... |
| 备选 1 | ... | ... | ... |
| 备选 2 | ... | ... | ... |
| 备选 3 | ... | ... | ... |

请确认 5 个主选，或用备选词进行替换。
```

## Copy-review format

Start with the issue number and shared theme. Then repeat this block five times:

```markdown
### 01｜<term>（<optional Chinese gloss>）

- 准确定义：<what it is; scope first>
- 人话翻译：<one direct sentence suitable for orange emphasis>
- 下沉类比：<one everyday analogy and the limit of that analogy when needed>
- 页面模块：<生动比喻 | 工具/案例 | 别搞混了 | 它怎么工作>
- 模块内容：<one concrete example, contrast, or mini-process>
- 视觉情境：<one original absurd-cat scene whose action or prop supports the concept>
- 核实说明：<scope, caveat, or corrected misconception>
- 主要来源：<primary links>
```

End with: `请确认或逐条修改文案；确认前不会生成图片。`

## Image-copy limits

These limits apply to the text that appears on a term image, not to fact-check notes.

- Term: preferably 2–12 Chinese characters or a short English expression.
- Optional gloss: no more than 12 Chinese characters.
- Accurate definition: 22–42 Chinese characters.
- Plain-language restatement: 14–28 Chinese characters.
- Lower-module text: 20–44 Chinese characters.
- Total term-page copy: target 55–95 Chinese characters so the generated scene stays dominant.
- Use one analogy, not a chain of analogies.

If copy does not fit, rewrite it. Do not hide overflow, reduce contrast, or shrink text into unreadability.

## Text accuracy gate

- Freeze the approved on-image wording before image generation.
- Compare final images character-for-character with that wording.
- Check Chinese characters, English capitalization, abbreviations, punctuation, screen text, book labels, and handwritten accents.
- Reject any page containing gibberish, an invented character, a missing or extra character, a wrong label, or unreadable text.
- Fix text with deterministic raster typesetting. Never accept a near match because the generated image looks good.

## Choosing the adaptive module

- `生动比喻`: abstract concepts that need an everyday object or role.
- `工具/案例`: a concrete product, workflow, or real use case is essential.
- `别搞混了`: two commonly confused terms need a clean contrast.
- `它怎么工作`: a short sequence explains the term better than a static definition.

Use exactly one module per page.
