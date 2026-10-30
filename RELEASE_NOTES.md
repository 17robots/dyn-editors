Editor support for Dyn, licensed under MIT.

- VS Code/forks: download the VSIX and use **Install from VSIX**.
- Zed: use **Install Dev Extension** on the repository's `zed/` directory until a registry listing is available.
- Helix/Neovim: use the configuration and queries in the source tree or release archives.
- Sublime: install LSP using Package Control, add the repository URL from the README, then install Dyn.
- Mason: add `github:17robots/dyn-editors@v0.1.5` to your registries and install `dyn`.

The compiler SDK is installed separately. This release pins Dyn **0.1.0-preview.28**
with verified checksums for Linux x64, macOS ARM64, and Windows x64. Mise and
Mason install the complete SDK.

Preview 28 improves compiler and language-server performance and expands the
standard library and desktop APIs. The existing editor adapters and pinned
Tree-sitter grammar are retained. When upgrading from older SDKs, follow the
[preview 27 migration guide](https://github.com/17robots/dyn/blob/v0.1.0-preview.28/docs/migrations/0.1.0-preview.27.md)
for pointer arena handles and standard-library changes. Restart `dyn lsp` after
upgrading the SDK.

See the README for installation steps and supported platforms. Marketplace listings
are separate from this GitHub release. `SHA256SUMS` covers the downloadable packages.
