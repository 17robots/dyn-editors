Editor support for Dyn, licensed under MIT.

- VS Code/forks: download the VSIX and use **Install from VSIX**.
- Zed: use **Install Dev Extension** on the repository's `zed/` directory until a registry listing is available.
- Helix/Neovim: use the configuration and queries in the source tree or release archives.
- Sublime: install LSP using Package Control, add the repository URL from the README, then install Dyn.
- Mason: add `github:17robots/dyn-editors@v0.1.4` to your registries and install `dyn`.

The compiler SDK is installed separately. This release pins Dyn **0.1.0-preview.23**
with verified checksums for Linux x64, macOS ARM64, and Windows x64. It includes
`#wrap` highlighting and uses the merged compact Tree-sitter grammar. Helix,
Neovim and Zed queries match the grammar's direct block children; Helix parameter
textobjects match call arguments without the removed expression wrapper.

Preview 23 improves compiler check/build speed and memory use without changing
Dyn source syntax or checked-arithmetic guarantees.

See the README for installation steps and supported platforms. Marketplace listings
are separate from this GitHub release. `SHA256SUMS` covers the downloadable packages.
