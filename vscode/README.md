# Dyn for VS Code

Requires the complete Dyn SDK on PATH. Open a folder containing `.dyn` files.
Completion, hover, navigation, rename, formatting and diagnostics use `dyn lsp`.
Set `dyn.server.path` to an absolute executable path if your editor cannot find
mise's shims. Use **Dyn: Restart Language Server** after changing SDK versions.

Local preview. Install the generated VSIX through **Extensions: Install from VSIX**.
For debugging, install LLVM's LLDB DAP extension and configure an executable built
with `dyn build --debug`. The accompanying compiler changes fix LLDB locals and
add macOS dSYM and Windows PDB output; preview.5 does not contain these fixes.

Compiler: https://github.com/17robots/dyn
