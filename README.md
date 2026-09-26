# Dyn editor integrations

One home for editor adapters, using the compiler's `dyn lsp` and the pinned
[Tree-sitter grammar](https://github.com/17robots/tree-sitter-dyn). Compiler and
grammar sources remain in their own repositories. Preview packages are available from [GitHub Releases](https://github.com/17robots/dyn-editors/releases/tag/v0.1.0).
Editor marketplace listings require separate approval/publication; use the methods below meanwhile.

## Install the compiler

Keep the **whole SDK**, including `lib/dyn` and `share/dyn`.
The pinned release supports Linux x64 (glibc 2.39+), macOS 15+ ARM64, and Windows x64.
Copy `shared/mise.toml` into a project as `mise.toml`, then run `mise install`.
Use `mise exec -- dyn version` to check it. For editors launched from a desktop,
put mise's shims on PATH or configure the absolute executable from `mise which dyn`.
Manual SDK downloads are on [Dyn releases](https://github.com/17robots/dyn/releases).
Do not configure two competing Dyn installations in the same editor.

All adapters recognize `.dyn` and start `dyn lsp`. Open the project directory as
an editor workspace. Helix and Neovim discover roots with `dyn.project`, `.git`,
or `.jj`; no marker is required for a standalone file. VS Code, Zed and Sublime
use their opened workspace. You do not need to add a project manifest for LSP.

## Editors

| Editor | Installation | Executable override |
| --- | --- | --- |
| VS Code / compatible forks | Download `dyn-0.1.0.vsix` from Releases, then **Extensions: Install from VSIX** | `dyn.server.path`, `dyn.server.args` |
| Zed | **zed: install dev extension**, select `zed/`; requires Rust and `wasm32-wasip2` | `lsp.dyn.binary.path`, `lsp.dyn.binary.arguments` |
| Helix | Merge `helix/languages.toml` into your config; copy `helix/runtime/queries/dyn` into your runtime queries; run `hx --grammar fetch` and `hx --grammar build` | `[language-server.dyn] command`, `args` |
| Neovim 0.11+ | Add `neovim/` to runtimepath and call `require('dyn').setup()` | `setup({cmd = {'/path/to/dyn', 'lsp'}})` |
| Sublime Text 4 | Install **LSP** using Package Control; add the repository URL below and install **Dyn** | User `LSP-Dyn.sublime-settings`: `{"command": ["/path/to/dyn", "lsp"]}` |

VS Code provides TextMate highlighting plus LSP semantic tokens. Zed, Helix and
Neovim use Tree-sitter. Sublime includes a syntax definition. Completion, hover,
navigation, references, rename, formatting and diagnostics come from the same
server; an editor displays only the protocol features it implements.

For Zed, Helix and Neovim, download this repository's source archive or clone
`https://github.com/17robots/dyn-editors.git`, then follow the table. Zed's dev
extension installer builds the grammar and extension for you.

For Sublime, run **Package Control: Add Repository** and enter:

```text
https://raw.githubusercontent.com/17robots/dyn-editors/main/sublime/packages.json
```

Then **Package Control: Install Package → Dyn**. Install **LSP** separately first;
it is an editor package, not a Python library dependency. Restart after installing
LSP if Dyn was already loaded. For manual installation, download
`Dyn.sublime-package` and place it in Sublime's `Installed Packages` directory.

Neovim example (replace the checkout path):

```lua
vim.opt.runtimepath:prepend('/path/to/dyn-editors/neovim')
require('dyn').setup()
```

For Neovim highlighting, run:

```sh
python scripts/install-parser.py --runtime /path/to/nvim-runtime
```

Add that runtime directory to Neovim's runtimepath too. This fetches the pinned
grammar and compiles `parser.c` **and** `scanner.c`; no language-server plugin or
nvim-treesitter dependency is needed. LSP still works without a parser.

## Mason

Mason installs the SDK, not the Neovim configuration. Configure the public registry:

```lua
require('mason').setup({
  registries = {
    'github:17robots/dyn-editors@v0.1.0',
    'github:mason-org/mason-registry',
  },
})
```

Run `:MasonUpdate`, then `:MasonInstall dyn`. Use `require('dyn').setup()` as above.
The package preserves the SDK layout and exposes its executable through Mason.
Unsupported operating systems/architectures have no package target. The registry
is pinned to this editor release. For local registry development, use
`file:/absolute/path/to/dyn-editors/mason` and install Mike Farah’s `yq`.

## Debugging

Build with `dyn build path/to/project --debug --output build/app` (use `app.exe`
on Windows). Create `build/` first. Linux stores DWARF in the executable. The local
compiler changes accompanying this repository add Windows `app.exe.pdb`, macOS
`app.dSYM`, and fix LLDB local-variable visibility. **Preview.6 does not include
those fixes.** Keep sidecars beside their executable. Optimized builds can omit
variables even with `--release --debug-info`.

Install LLDB and its DAP adapter separately. Use the examples in `shared/debug/`:

- VS Code: install the [LLVM LLDB DAP extension](https://lldb.llvm.org/use/lldbdap.html),
  copy `vscode-launch.json` to `.vscode/launch.json` and set the program path.
- Zed: copy `zed-debug.json` to `.zed/debug.json`; its built-in CodeLLDB adapter is used.
- Helix: the language configuration includes an `lldb-dap` launch template.
- Neovim: install `nvim-dap`, then call `require('dyn').setup_debugger()`.
- Sublime: install **Debugger**, install its LLDB adapter, and merge
  `sublime-project.json` into the project settings.

Adjust executable paths in examples for Windows. These are explicit launch
configurations; they do not guess your project's build command. LLDB uses C-style
expression evaluation for Dyn's debug types, not a full Dyn expression parser.

Optional LLDB summaries: run `command script import /absolute/path/to/shared/debug/dyn_lldb.py`
in LLDB's console, or include that command in the adapter's `initCommands`.
Byte-string previews are bounded; slices show length and address. Structs and enum
storage use the debugger's normal member display.

## Maintain and verify

`shared/release.json` is the source of truth for SDK version, checksums and grammar
revision. Generated files carry a comment. Update them locally with:

```sh
python scripts/update-release.py 0.1.0-preview.6
python scripts/sync.py --check
python tests/lsp.py
python scripts/package.py
```

The update command verifies downloads against GitHub's published SHA-256 digest
before changing pins. An optional `--grammar-revision <full-commit>` updates grammar
pins; review query compatibility after changing it. Packaging produces local
artifacts in ignored `dist/`, never publishes. CI builds packages and exercises
the server on Linux, macOS and Windows. Check the [CI runs](https://github.com/17robots/dyn-editors/actions) for native
platform results. Marketplace publication remains a separate step; see [publishing instructions](PUBLISHING.md).

Additional checks:

```sh
python scripts/install-parser.py --runtime build/nvim-runtime
DYN_EDITORS="$PWD" nvim --headless -u NONE -l tests/neovim.lua
node tests/run-vscode.cjs  # Linux needs a display or xvfb-run
DYN=/path/to/new/dyn LLDB_DAP=lldb-dap python tests/debugger.py
```

`tests/mason.lua` expects Mason in `build/deps/mason.nvim` and `yq` on PATH; it
installs into `build/mason`, leaving normal editor settings alone. Packaging also
requires Mike Farah’s `yq` for the publishable Mason registry JSON. See the workflow
for repeatable CI commands. Zed and Sublime have also loaded the local integration and connected to Dyn.
Broader GUI checks and VS Code forks still need manual testing. This repository does not claim every
editor or platform has been interactively tested.

Editor integrations in this repository are licensed under [MIT](LICENSE),
copyright Matthew Dray. Dependencies retain their own licenses. The Dyn compiler
and SDK remain covered by their separate preview license; the Mason package
describes that compiler license, not the license of this repository.
