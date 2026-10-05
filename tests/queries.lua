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
fn sample(output: Allocator) #AllocResult([]u64) {
  backing: [Count * 2]u8
  _ = #alloc_or_panic(u8, output)
  return #alloc_slice(u64, output, 4)
}
]]
local parser = vim.treesitter.get_string_parser(source, 'dyn')
local root = parser:parse()[1]:root()
assert(not root:has_error(), 'allocator/constant-array fixture must parse')
for _, file in ipairs({ 'helix/runtime/queries/dyn/highlights.scm', 'zed/languages/dyn/highlights.scm', 'neovim/queries/dyn/highlights.scm' }) do
  local query = vim.treesitter.query.parse('dyn', table.concat(vim.fn.readfile(file), '\n'))
  local captured = {}
  for id, node in query:iter_captures(root, source, 0, -1) do
    captured[vim.treesitter.get_node_text(node, source)] = query.captures[id]
  end
  assert(captured['Allocator'] == 'type.builtin', file .. ': Allocator highlight')
  for _, name in ipairs({ '#AllocResult', '#alloc_or_panic', '#alloc_slice' }) do
    assert(captured[name] == 'function.builtin', file .. ': ' .. name .. ' highlight')
  end
  print('PASS allocator captures: ' .. file)
end
vim.cmd.qa()
