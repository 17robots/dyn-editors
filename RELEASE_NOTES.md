Editor support for Dyn, licensed under MIT.

- VS Code/forks: download the VSIX and use **Install from VSIX**.
- Zed: use **Install Dev Extension** on the repository's `zed/` directory until a registry listing is available.
- Helix/Neovim: use the configuration and queries in the source tree or release archives.
- Sublime: install LSP using Package Control, add the repository URL from the README, then install Dyn.
- Mason: add `github:17robots/dyn-editors@v0.1.8` to your registries and install `dyn`.

The compiler SDK is installed separately. This release pins Dyn **0.1.0-preview.37**
with verified checksums for Linux x64, macOS ARM64, and Windows x64. Mise and
Mason install the complete SDK.

Preview 37 prints structs and enums from any expression in format templates and
keeps debugger scopes correct with overflow checks on. It changes no syntax, so
the pinned Tree-sitter grammar is unchanged from 0.1.7.

Code written for preview 35 or older needs the
[standardization migration](https://github.com/17robots/dyn/blob/v0.1.0-preview.37/docs/migrations/standard-20261113.md)
(`tools/migrate-standard.py`). Restart `dyn lsp` after upgrading the SDK.

See the README for installation steps and supported platforms. Marketplace listings
are separate from this GitHub release. `SHA256SUMS` covers the downloadable packages.
