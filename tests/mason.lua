local root = assert(vim.env.DYN_EDITORS)
vim.opt.runtimepath:prepend(root .. '/build/deps/mason.nvim')
require('mason').setup({
  install_root_dir = root .. '/build/mason',
  registries = { 'file:' .. root .. '/mason' },
})
local registry = require('mason-registry')
local done, failure = false, nil
registry.refresh(function(success)
  if not success then failure = 'registry refresh failed'; done = true; return end
  local package = registry.get_package('dyn')
  if package:is_installed() then done = true; return end
  package:install():once('closed', function()
    if not package:is_installed() then failure = 'Dyn SDK install failed; inspect build/mason log' end
    done = true
  end)
end)
assert(vim.wait(180000, function() return done end, 100), 'Mason timed out')
assert(not failure, failure)
local output = vim.fn.system({ root .. '/build/mason/bin/dyn', 'version' })
assert(vim.v.shell_error == 0, output)
print('PASS Mason SDK install: ' .. output)
vim.cmd.qa()
