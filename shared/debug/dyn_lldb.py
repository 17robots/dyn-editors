"""Bounded Dyn string/slice summaries for LLDB and LLDB-based DAP adapters."""
import json
import lldb

MAX_STRING_BYTES = 256

def string_summary(value, _internal):
    data = value.GetChildMemberWithName('data')
    length = value.GetChildMemberWithName('len')
    if not data.IsValid() or not length.IsValid():
        return '<unavailable>'
    size = length.GetValueAsUnsigned()
    if size == 0:
        return '""'
    error = lldb.SBError()
    raw = value.GetProcess().ReadMemory(data.GetValueAsUnsigned(), min(size, MAX_STRING_BYTES), error)
    if error.Fail():
        return f'<unreadable string, len={size}>'
    text = bytes(raw).decode('utf-8', errors='replace')
    return json.dumps(text, ensure_ascii=False) + ('…' if size > MAX_STRING_BYTES else '')

def slice_summary(value, _internal):
    length = value.GetChildMemberWithName('len')
    data = value.GetChildMemberWithName('data')
    if not data.IsValid() or not length.IsValid():
        return '<unavailable>'
    summary = f'len={length.GetValueAsUnsigned()}, data=0x{data.GetValueAsUnsigned():x}'
    if data.GetType().GetPointeeType().GetName() in ('u8', 'unsigned char'):
        summary += ', bytes=' + string_summary(value, _internal)
    return summary

def __lldb_init_module(debugger, _internal):
    debugger.HandleCommand('type summary add -w Dyn -F dyn_lldb.string_summary "[]const u8"')
    debugger.HandleCommand('type summary add -w Dyn -F dyn_lldb.slice_summary slice')
    debugger.HandleCommand('type category enable Dyn')
