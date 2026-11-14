Editor support for Dyn, licensed under MIT.

- VS Code/forks: download the VSIX and use **Install from VSIX**.
- Zed: use **Install Dev Extension** on the repository's `zed/` directory until a registry listing is available.
- Helix/Neovim: use the configuration and queries in the source tree or release archives.
- Sublime: install LSP using Package Control, add the repository URL from the README, then install Dyn.
- Mason: add `github:17robots/dyn-editors@v0.1.7` to your registries and install `dyn`.

The compiler SDK is installed separately. This release pins Dyn **0.1.0-preview.36**
with verified checksums for Linux x64, macOS ARM64, and Windows x64. Mise and
Mason install the complete SDK.

The pinned Tree-sitter grammar now matches the preview 36 language: `for x, i in xs`
index loops (the index is a named `index` field of `for_condition`), and struct
literals that always name their type, since `.{...}` is gone. Text `case`
patterns, the stricter rules (no chained comparisons, no shadowing) and the std
changes need no grammar changes.

Preview 36 is a breaking cleanup before the language freeze. Follow the
[standardization migration](https://github.com/17robots/dyn/blob/v0.1.0-preview.36/docs/migrations/standard-20261113.md)
and run `tools/migrate-standard.py`. Restart `dyn lsp` after upgrading the SDK.

See the README for installation steps and supported platforms. Marketplace listings
are separate from this GitHub release. `SHA256SUMS` covers the downloadable packages.
