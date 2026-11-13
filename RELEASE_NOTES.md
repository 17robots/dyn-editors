Editor support for Dyn, licensed under MIT.

- VS Code/forks: download the VSIX and use **Install from VSIX**.
- Zed: use **Install Dev Extension** on the repository's `zed/` directory until a registry listing is available.
- Helix/Neovim: use the configuration and queries in the source tree or release archives.
- Sublime: install LSP using Package Control, add the repository URL from the README, then install Dyn.
- Mason: add `github:17robots/dyn-editors@v0.1.6` to your registries and install `dyn`.

The compiler SDK is installed separately. This release pins Dyn **0.1.0-preview.35**
with verified checksums for Linux x64, macOS ARM64, and Windows x64. Mise and
Mason install the complete SDK.

The pinned Tree-sitter grammar now matches the preview 35 language: generic
structs, enums and types with one spelling, `#instance`, enum payloads and
values, field defaults, `#init`, `#assert` statements, and the `#max(T)` /
`#min(T)` integer limits. Helix, Neovim and Zed highlight the new builtins,
including `#offset` and `#slice`.

Code written for preview 28 or older needs the
[generics migration](https://github.com/17robots/dyn/blob/v0.1.0-preview.35/docs/migrations/generics-one-spelling.md)
and the [preview 31 migration guide](https://github.com/17robots/dyn/blob/v0.1.0-preview.35/docs/migrations/0.1.0-preview.31.md).
Restart `dyn lsp` after upgrading the SDK.

See the README for installation steps and supported platforms. Marketplace listings
are separate from this GitHub release. `SHA256SUMS` covers the downloadable packages.
