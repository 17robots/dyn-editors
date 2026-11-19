Editor support for Dyn, licensed under MIT.

- VS Code/forks: download the VSIX and use **Install from VSIX**.
- Zed: use **Install Dev Extension** on the repository's `zed/` directory until a registry listing is available.
- Helix/Neovim: use the configuration and queries in the source tree or release archives.
- Sublime: install LSP using Package Control, add the repository URL from the README, then install Dyn.
- Mason: add `github:17robots/dyn-editors@v0.1.9` to your registries and install `dyn`.

The compiler SDK is installed separately. This release pins Dyn **0.1.0-preview.40**
with verified checksums for Linux x64, macOS ARM64, and Windows x64. Mise and
Mason install the complete SDK.

The pinned Tree-sitter grammar follows the preview 40 language: it parses
`#wrapping`, `#step`, the floating-point builtins (`#sqrt`, `#floor`, `#ceil`,
`#trunc`, `#round`, `#fma`) and bare `{ }` blocks, and no longer parses loop
labels, `for *const` or `#offset`. Helix, Neovim and Zed queries come from it;
VS Code and Sublime already match any `#name` as a builtin.

Code from preview 39 needs the
[preview 40 migration](https://github.com/17robots/dyn/blob/v0.1.0-preview.40/docs/migrations/0.1.0-preview.40.md):
failures go on a `fail.Status` (or `nil`), lookups return their value,
iterators set `ended`, and `dyn fix` handles the mechanical parts.
Restart `dyn lsp` after upgrading the SDK.

See the README for installation steps and supported platforms. Marketplace listings
are separate from this GitHub release. `SHA256SUMS` covers the downloadable packages.
