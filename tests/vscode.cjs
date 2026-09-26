const assert = require('node:assert/strict');
const vscode = require('vscode');
exports.run = async function() {
  const root = process.env.DYN_EDITORS;
  const document = await vscode.workspace.openTextDocument(vscode.Uri.file(root + '/shared/fixtures/main.dyn'));
  await vscode.window.showTextDocument(document);
  assert.equal(document.languageId, 'dyn');
  await vscode.extensions.getExtension('17robots.dyn').activate();
  let hover;
  for (let attempt = 0; attempt < 100; attempt++) {
    hover = await vscode.commands.executeCommand('vscode.executeHoverProvider', document.uri, new vscode.Position(6, 15));
    if (hover?.length) break;
    await new Promise(resolve => setTimeout(resolve, 100));
  }
  assert.ok(hover?.length, 'Dyn hover never arrived');
  const definitions = await vscode.commands.executeCommand('vscode.executeDefinitionProvider', document.uri, new vscode.Position(6, 15));
  assert.ok(definitions.length, 'No definition');
  const edits = await vscode.commands.executeCommand('vscode.executeDocumentRenameProvider', document.uri, new vscode.Position(6, 15), 'sum_values');
  assert.ok(edits.size, 'No rename edits');
  await vscode.commands.executeCommand('dyn.restart');
  console.log('PASS VS Code activation, hover, definition, rename and restart');
};
