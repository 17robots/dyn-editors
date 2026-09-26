local M = {}
function M.setup(opts)
  opts = opts or {}
  vim.filetype.add({ extension = { dyn = 'dyn' } })
  vim.lsp.config('dyn', { cmd = opts.cmd or { 'dyn', 'lsp' } })
  vim.lsp.enable('dyn')
  local group = vim.api.nvim_create_augroup('DynEditor', { clear = true })
  vim.api.nvim_create_autocmd('FileType', {
    group = group, pattern = 'dyn', callback = function(args)
      vim.bo[args.buf].commentstring = '// %s'
      vim.bo[args.buf].shiftwidth = 4
      vim.bo[args.buf].expandtab = true
      if pcall(vim.treesitter.language.add, 'dyn') then
        vim.treesitter.start(args.buf, 'dyn')
      end
    end,
  })
end
function M.setup_debugger(opts)
  opts = opts or {}
  local dap = require('dap')
  dap.adapters.dyn = { type = 'executable', command = opts.adapter or 'lldb-dap', name = 'lldb' }
  dap.configurations.dyn = {{
    name = 'Debug Dyn', type = 'dyn', request = 'launch',
    program = function() return vim.fn.input('Executable: ', vim.fn.getcwd() .. '/', 'file') end,
    cwd = '${workspaceFolder}', stopOnEntry = false,
  }}
end
return M
