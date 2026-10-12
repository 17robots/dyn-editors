vim.opt.runtimepath:prepend(vim.fn.getcwd() .. '/build/nvim-runtime')
vim.treesitter.language.add('dyn')
for _, glob in ipairs({ 'helix/runtime/queries/dyn/*.scm', 'zed/languages/dyn/*.scm', 'neovim/queries/dyn/*.scm' }) do
  for _, file in ipairs(vim.fn.glob(glob, false, true)) do
    vim.treesitter.query.parse('dyn', table.concat(vim.fn.readfile(file), '\n'))
    print('PASS ' .. file)
  end
end
local source = [[
const Count: usize = 4
fn sample($T: type) usize {
  backing: [Count * 2]u8
  return #sizeof(T) + #alignof(T)
}
]]
local parser = vim.treesitter.get_string_parser(source, 'dyn')
local root = parser:parse()[1]:root()
assert(not root:has_error(), 'builtin/constant-array fixture must parse')
for _, file in ipairs({ 'helix/runtime/queries/dyn/highlights.scm', 'zed/languages/dyn/highlights.scm', 'neovim/queries/dyn/highlights.scm' }) do
  local query = vim.treesitter.query.parse('dyn', table.concat(vim.fn.readfile(file), '\n'))
  local captured = {}
  for id, node in query:iter_captures(root, source, 0, -1) do
    captured[vim.treesitter.get_node_text(node, source)] = query.captures[id]
  end
  assert(captured['usize'] == 'type.builtin', file .. ': primitive highlight')
  assert(captured['$T'] == 'type', file .. ': type parameter highlight')
  for _, name in ipairs({ '#sizeof', '#alignof' }) do
    assert(captured[name] == 'function.builtin', file .. ': ' .. name .. ' highlight')
  end
  print('PASS builtin captures: ' .. file)
end
vim.cmd.qa()
