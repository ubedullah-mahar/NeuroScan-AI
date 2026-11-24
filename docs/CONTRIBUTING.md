# Contributing

Contributions should be reviewable, reproducible, and respectful of the separation between the Streamlit interface, inference code, research notebooks, and model artifacts.

## Branching

Create a short-lived branch from the team's current integration branch. Use a descriptive prefix:

- `feature/<short-description>`
- `fix/<short-description>`
- `docs/<short-description>`
- `research/<short-description>`

Do not assume the project has a protected default branch; follow the repository host's configured branch policy.

## Commit messages

Use the Conventional Commits style with a short, imperative summary:

```text
docs: clarify segmentation checkpoint setup
fix: handle invalid uploaded image
feat: add classification result details
```

Use `docs:`, `fix:`, `feat:`, `test:`, or `chore:` as appropriate. Keep unrelated work in separate commits. Do not commit credentials, private datasets, or unapproved model weights.

## Pull requests

Open a pull request against the team's designated integration branch. Include:

- A concise description of the change and its motivation.
- The affected workflows, modules, dependencies, and artifacts.
- Tests, static checks, or manual verification performed; state when they were not run.
- Screenshots for visible UI changes when the interface can safely be run.
- Documentation updates and any required data/model setup.

Keep PRs focused. Request review from the owners of the impacted UI or ML area before changes that cross those boundaries.

## Python and documentation standards

- Follow the style and naming already used by the surrounding module.
- Keep inference interfaces and serialization formats explicit and stable.
- Add focused tests for new behavior where the test suite can isolate it from external models and datasets.
- Avoid hard-coded machine-specific paths in new reusable code.
- Use repository-relative links in Markdown and keep setup commands copyable.
- Distinguish measured results, notebook outputs, and unverified assumptions. Never invent performance metrics or medical claims.
- Record new runtime dependencies in `requirements.txt` only when required; identify optional research tools separately and avoid unnecessary version pins.

## Protecting existing ML functionality

- Do not change classification preprocessing, feature extraction, class mapping, SVM behavior, segmentation preprocessing, U-Net architecture, checkpoint keys, or inference outputs as part of UI or documentation-only work.
- Preserve compatibility with `predict_classification()` and `predict_segmentation()` unless a separately reviewed ML change explicitly updates their contract and callers.
- Do not replace or retrain model artifacts without approval, provenance, metadata, and a documented evaluation.
- Keep datasets and checkpoints out of Git unless their ownership, license, size, and storage method have been approved.
- When changing an inference interface, document migration impact and verify all callers and tests.

## Current repository caveats

The files in `tests/` currently execute inference at module import and use hard-coded image paths. They are not isolated pytest tests. Refactor them into safe, deterministic tests before treating automated test discovery as a required PR check. The segmentation checkpoint is also absent from the repository; see the [setup guide](SETUP_GUIDE.md).
