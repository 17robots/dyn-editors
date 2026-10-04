# Publishing

GitHub releases are built and tested by `.github/workflows/release.yml` when a
`v*` tag is pushed. The tag must match `vscode/package.json`. Use non-colocated jj:

```sh
jj tag set v0.1.1 -r main
jj git push --tag v0.1.1
```

Before the next release, update the extension versions, `sublime/packages.json`,
the README's release links and Mason registry pin, and `RELEASE_NOTES.md`.
Run `python scripts/sync.py --check`. The workflow checks Linux, macOS and
Windows and publishes only after every required check succeeds.

## VS Code Marketplace and Open VSX

Both accept the released `dyn-0.1.1.vsix`; no separate extension implementation
is needed. Download the VSIX and `SHA256SUMS` from the release and verify its hash.

- [Visual Studio Marketplace](https://marketplace.visualstudio.com/manage):
  register the `17robots` publisher, then upload the VSIX through its management
  page. [Publishing guide](https://code.visualstudio.com/api/working-with-extensions/publishing-extension).
- [Open VSX](https://open-vsx.org): sign in, complete the Eclipse publisher
  agreement, and create/claim the `17robots` namespace. Publish the same VSIX
  using the Open VSX CLI with your account token.
  [Publishing guide](https://github.com/eclipse-openvsx/openvsx/wiki/Publishing-Extensions).

Account registration, agreement acceptance and credentials belong to the owner.
Never commit tokens or paste them into issues/chat. These listings are not live
merely because the GitHub release exists.

## Zed

The registry supports a subdirectory in a repository. Its Dyn entry will use
`submodule = "extensions/dyn"`, `path = "zed"`, and `version = "0.1.1"`, with
the submodule pointing to this repository at the released commit.
Follow the [publishing guide](https://zed.dev/docs/extensions/publishing/publishing-guide).

The [registry's AI policy](https://github.com/zed-industries/extensions/blob/main/AI_POLICY.md)
prohibits autonomous agent contributions and AI-generated maintainer communication.
The maintainer must make this submission and explain it in their own words.
Until accepted, use the documented dev-extension installation.

## Sublime, Helix and Neovim

Sublime users can install through the public custom repository documented in the
README. The release's `.sublime-package` contains only Sublime files. An entry in
Package Control's default channel requires a separate maintainer review.

Helix and Neovim configuration bundles are available in the release. The Mason
registry is published in the same release as `registry.json.zip` and
`checksums.txt`; the README pins it explicitly because this is a GitHub prerelease.
Mason installs the compiler SDK; the Neovim configuration remains a separate step.
