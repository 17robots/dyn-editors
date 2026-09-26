const path = require('node:path');
const { runTests } = require('../vscode/node_modules/@vscode/test-electron');
const root = path.resolve(__dirname, '..');
runTests({
  version: '1.105.1',
  cachePath: path.join(root, 'build/vscode-test'),
  extensionDevelopmentPath: path.join(root, 'vscode'),
  extensionTestsPath: path.join(__dirname, 'vscode.cjs'),
  extensionTestsEnv: { DYN_EDITORS: root },
  launchArgs: [path.join(root, 'shared/fixtures'), '--no-sandbox', '--disable-gpu', '--skip-welcome', '--disable-workspace-trust'],
}).catch(error => { console.error(error); process.exit(1); });
