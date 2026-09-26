Editor support for Dyn, licensed under MIT.

- VS Code/forks: download the VSIX and use **Install from VSIX**.
- Zed: use **Install Dev Extension** on the repository's `zed/` directory until a registry listing is available.
- Helix/Neovim: use the configuration and queries in the source tree or release archives.
- Sublime: install LSP using Package Control, add the repository URL from the README, then install Dyn.
- Mason: add `github:17robots/dyn-editors@v0.1.0` to your registries and install `dyn`.

The compiler SDK is installed separately. This release pins Dyn **0.1.0-preview.6**,
which fixes the Windows language-server stack overflow during references, rename,
and document highlighting.
The newer LLDB variable fixes and Windows/macOS debugger sidecars are not yet in
that compiler release. Debugger configurations are provided for testing with the
corresponding compiler changes; this editor release does not ship those fixes.

See the README for installation steps and supported platforms. Marketplace listings
are separate from this GitHub release. `SHA256SUMS` covers the downloadable packages.
