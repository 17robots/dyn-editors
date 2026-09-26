local root = assert(vim.env.DYN_EDITORS)
vim.opt.runtimepath:prepend(root .. '/neovim')
vim.opt.runtimepath:prepend(root .. '/build/nvim-runtime')
vim.cmd('filetype on')
require('dyn').setup()
vim.cmd.edit(root .. '/shared/fixtures/main.dyn')
assert(vim.bo.filetype == 'dyn', 'filetype detection failed')
assert(vim.wait(10000, function()
  local clients = vim.lsp.get_clients({ bufnr = 0, name = 'dyn' })
  return #clients == 1 and clients[1].initialized
end, 50), 'Dyn LSP did not attach')
local client = vim.lsp.get_clients({ bufnr = 0, name = 'dyn' })[1]
local result = client:request_sync('textDocument/hover', {
  textDocument = { uri = vim.uri_from_bufnr(0) }, position = { line = 6, character = 15 },
}, 5000, 0)
assert(result and not result.err and result.result, vim.inspect(result))
local parser = vim.treesitter.get_parser(0, 'dyn')
assert(not parser:parse()[1]:root():has_error(), 'Tree-sitter parse failed')
for _, query in ipairs({ 'highlights', 'locals', 'indents', 'folds' }) do
  assert(vim.treesitter.query.get('dyn', query), query .. ' failed to compile')
end
client:stop()
print('PASS Neovim filetype, LSP hover, Tree-sitter parser and queries')
vim.cmd.qa()
