use zed_extension_api::{self as zed, Result, settings::LspSettings};
struct Dyn;
impl zed::Extension for Dyn {
    fn new() -> Self {
        Self
    }
    fn language_server_command(
        &mut self,
        id: &zed::LanguageServerId,
        worktree: &zed::Worktree,
    ) -> Result<zed::Command> {
        let binary = LspSettings::for_worktree(id.as_ref(), worktree)?.binary;
        let path = binary.as_ref().and_then(|b| b.path.clone())
            .or_else(|| worktree.which("dyn"))
            .ok_or_else(|| "Dyn SDK not found. Install Dyn, then add its bin directory to PATH or set lsp.dyn.binary.path.".to_string())?;
        Ok(zed::Command {
            command: path,
            args: binary
                .as_ref()
                .and_then(|b| b.arguments.clone())
                .unwrap_or_else(|| vec!["lsp".into()]),
            env: binary
                .and_then(|b| b.env)
                .unwrap_or_default()
                .into_iter()
                .collect(),
        })
    }
}
zed::register_extension!(Dyn);
