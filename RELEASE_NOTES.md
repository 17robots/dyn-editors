Editor support for Dyn, licensed under MIT.

- VS Code/forks: download the VSIX and use **Install from VSIX**.
- Zed: use **Install Dev Extension** on the repository's `zed/` directory until a registry listing is available.
- Helix/Neovim: use the configuration and queries in the source tree or release archives.
- Sublime: install LSP using Package Control, add the repository URL from the README, then install Dyn.
- Mason: add `github:17robots/dyn-editors@v0.1.11` to your registries and install `dyn`.

The compiler SDK is installed separately. This release pins Dyn **0.1.0-preview.41**
with verified checksums for Linux x64, macOS ARM64, and Windows x64. Mise and
Mason install the complete SDK.

The pinned Tree-sitter grammar follows the preview 41 language (next-design):
it parses `<T>` generics, `T!E` / `A | B` error returns, `try` / `catch` / `fail` /
`errdefer`, `nocopy struct`, `#take`, shebangs, raw backtick strings, labeled
`break`/`continue`, `.Variant` shorthand, `.len`, and alias-first `use`, and is now
pure `grammar.js` without `scanner.c`. Helix, Neovim, Zed, VS Code, and Sublime
highlighting queries and grammars are updated to match.

Code from preview 40 needs the
[preview 41 migration](https://github.com/17robots/dyn/blob/v0.1.0-preview.41/docs/migrations/0.1.0-preview.41.md):
generics use `<T>`, `std/fail` is replaced by `T!E` return errors, `#len(xs)`
becomes `xs.len`, and import aliases come before the path.
Restart `dyn lsp` after upgrading the SDK.

See the README for installation steps and supported platforms. Marketplace listings
are separate from this GitHub release. `SHA256SUMS` covers the downloadable packages.
