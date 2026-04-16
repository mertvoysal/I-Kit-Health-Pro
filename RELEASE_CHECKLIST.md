# Release Checklist

Use this checklist before sharing a new public update of `I-Kit Health Pro`.

## Code Quality

- [ ] Run the app locally (`python app.py`) and confirm no startup errors.
- [ ] Run a sample analysis flow end-to-end and verify diagnosis + doctor table output.
- [ ] Confirm map links open correct hospital pages.
- [ ] Ensure there are no unintended local files in `git status`.

## Documentation

- [ ] Verify `README.md` reflects the current UI and feature set.
- [ ] Confirm screenshots in `docs/images/` match the latest production look.
- [ ] Keep clinical safety wording consistent in UI and docs.

## Deployment

- [ ] Push latest commit to GitHub (`main`).
- [ ] Deploy to Hugging Face Space using `scripts/upload_to_hf_space.py`.
- [ ] Confirm Space status is `Running`.
- [ ] Re-test one live prediction on the Space endpoint.

## Final Gate

- [ ] Ensure no sensitive tokens/credentials are committed.
- [ ] Review release scope: only product-relevant files are included.
- [ ] Tag or note the release commit hash for traceability.
