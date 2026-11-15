Editor support for Dyn, licensed under MIT.

- VS Code/forks: download the VSIX and use **Install from VSIX**.
- Zed: use **Install Dev Extension** on the repository's `zed/` directory until a registry listing is available.
- Helix/Neovim: use the configuration and queries in the source tree or release archives.
- Sublime: install LSP using Package Control, add the repository URL from the README, then install Dyn.
- Mason: add `github:17robots/dyn-editors@v0.1.9` to your registries and install `dyn`.

The compiler SDK is installed separately. This release pins Dyn **0.1.0-preview.39**
with verified checksums for Linux x64, macOS ARM64, and Windows x64. Mise and
Mason install the complete SDK.

Preview 39 removes `union` types, and the pinned Tree-sitter grammar no longer
parses `union` declarations. Sublime and VS Code no longer highlight `is` as a
keyword; the grammar dropped it with type patterns.

Code that declares unions needs the
[preview 39 migration](https://github.com/17robots/dyn/blob/v0.1.0-preview.39/docs/migrations/0.1.0-preview.39.md):
`#bitcast` for bit reinterpretation, payload enums for one-of-several storage.
Restart `dyn lsp` after upgrading the SDK.

See the README for installation steps and supported platforms. Marketplace listings
are separate from this GitHub release. `SHA256SUMS` covers the downloadable packages.
