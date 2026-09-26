vim.opt.runtimepath:prepend(vim.fn.getcwd() .. '/build/nvim-runtime')
vim.treesitter.language.add('dyn')
for _, glob in ipairs({ 'helix/runtime/queries/dyn/*.scm', 'zed/languages/dyn/*.scm' }) do
  for _, file in ipairs(vim.fn.glob(glob, false, true)) do
    vim.treesitter.query.parse('dyn', table.concat(vim.fn.readfile(file), '\n'))
    print('PASS ' .. file)
  end
end
vim.cmd.qa()
