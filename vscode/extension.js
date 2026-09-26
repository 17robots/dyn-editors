const vscode = require('vscode');
const { LanguageClient } = require('vscode-languageclient/node');
const clients = new Map();
const watchers = [];
let serial = Promise.resolve();
async function restart() {
  await Promise.all([...clients.values()].map(client => client.stop()));
  clients.clear();
  watchers.splice(0).forEach(watcher => watcher.dispose());
  if (!vscode.workspace.isTrusted) return;
  const folders = vscode.workspace.workspaceFolders || [undefined];
  for (const folder of folders) {
    const config = vscode.workspace.getConfiguration('dyn', folder?.uri);
    const server = { command: config.get('server.path', 'dyn'), args: config.get('server.args', ['lsp']) };
    const selector = folder
      ? [{ scheme: 'file', language: 'dyn', pattern: new vscode.RelativePattern(folder, '**/*.dyn') }]
      : [{ scheme: 'file', language: 'dyn' }];
    const watcher = vscode.workspace.createFileSystemWatcher(new vscode.RelativePattern(folder?.uri || vscode.Uri.file(process.cwd()), '**/*.dyn'));
    watchers.push(watcher);
    const client = new LanguageClient('dyn', 'Dyn', server, {
      documentSelector: selector, workspaceFolder: folder,
      synchronize: { fileEvents: watcher },
    });
    clients.set(folder?.uri.toString() || 'single-file', client);
    await client.start();
  }
}
function scheduleRestart() {
  serial = serial.then(restart).catch(error => vscode.window.showErrorMessage(`Dyn: ${error.message}`));
  return serial;
}
exports.activate = function(context) {
  context.subscriptions.push(
    vscode.commands.registerCommand('dyn.restart', scheduleRestart),
    vscode.workspace.onDidChangeWorkspaceFolders(scheduleRestart),
    vscode.workspace.onDidChangeConfiguration(event => { if (event.affectsConfiguration('dyn')) scheduleRestart(); }),
  );
  return scheduleRestart();
};
exports.deactivate = async function() {
  await serial;
  await Promise.all([...clients.values()].map(client => client.stop()));
  clients.clear();
  watchers.splice(0).forEach(watcher => watcher.dispose());
};
