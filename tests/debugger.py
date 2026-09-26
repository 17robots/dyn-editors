#!/usr/bin/env python3
"""Verify source breakpoints, arguments, locals and stepping through LLDB DAP."""
import argparse
import json
import os
from pathlib import Path
import queue
import subprocess
import tempfile
import threading
import time

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--dyn', default=os.environ.get('DYN','dyn'))
parser.add_argument('--adapter', default=os.environ.get('LLDB_DAP','lldb-dap'))
args = parser.parse_args()
source = '''fn add(left: i32, right: i32) i32 {
    sum := left + right
    text := "hello"
    return sum
}
fn main() {
    result := add(20, 22)
    if result != 42 { #panic("wrong result") }
}
'''
with tempfile.TemporaryDirectory(prefix='dyn debug ') as directory:
    root = Path(directory).resolve()
    (root/'main.dyn').write_text(source)
    output = root/('program.exe' if os.name == 'nt' else 'program')
    subprocess.run([args.dyn,'build',str(root),'--debug','--no-cache','--output',str(output)],check=True)
    process = subprocess.Popen([args.adapter],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    messages = queue.Queue()
    def read():
        try:
            while True:
                header = {}
                while True:
                    line = process.stdout.readline()
                    if not line: return
                    if line == b'\r\n': break
                    key, value = line.decode().split(':',1)
                    header[key.lower()] = value.strip()
                messages.put(json.loads(process.stdout.read(int(header['content-length']))))
        finally:
            messages.put({'event':'eof'})
    threading.Thread(target=read,daemon=True).start()
    pending = []
    sequence = 0
    def wait(predicate):
        deadline = time.monotonic()+20
        while time.monotonic()<deadline:
            for i, item in enumerate(pending):
                if predicate(item): return pending.pop(i)
            item = messages.get(timeout=max(0.01,deadline-time.monotonic()))
            if item.get('event')=='eof': raise RuntimeError('DAP exited: '+process.stderr.read().decode())
            pending.append(item)
        raise TimeoutError(pending)
    def send(command, arguments):
        global sequence
        sequence += 1
        body = json.dumps({'seq':sequence,'type':'request','command':command,'arguments':arguments}).encode()
        process.stdin.write(b'Content-Length: %d\r\n\r\n'%len(body)+body)
        process.stdin.flush()
        return sequence
    def response(ident):
        result = wait(lambda item:item.get('type')=='response' and item.get('request_seq')==ident)
        assert result['success'],result
        return result.get('body',{})
    def request(command, arguments): return response(send(command,arguments))
    try:
        request('initialize',{'adapterID':'lldb','linesStartAt1':True,'columnsStartAt1':True,'pathFormat':'path'})
        launch = send('launch',{'program':str(output),'cwd':str(root),'disableASLR':False,'stopOnEntry':False,
            'initCommands':['command script import "' + (Path(__file__).resolve().parents[1]/'shared/debug/dyn_lldb.py').as_posix() + '"']})
        wait(lambda item:item.get('event')=='initialized')
        bp = request('setBreakpoints',{'source':{'path':str(root/'main.dyn')},'breakpoints':[{'line':4}]})
        assert bp['breakpoints'][0]['verified'],bp
        request('configurationDone',{})
        response(launch)
        stopped = wait(lambda item:item.get('event')=='stopped')
        thread = stopped['body']['threadId']
        stack = request('stackTrace',{'threadId':thread})['stackFrames']
        assert len(stack)>=2,stack
        assert stack[0]['line']==4,stack
        scopes = request('scopes',{'frameId':stack[0]['id']})['scopes']
        values = {}
        for scope in scopes:
            for variable in request('variables',{'variablesReference':scope['variablesReference']})['variables']:
                values[variable['name']] = variable['value']
        for name, value in [('left','20'),('right','22'),('sum','42')]:
            assert values.get(name)==value,values
        assert 'hello' in values.get('text',''),values
        request('next',{'threadId':thread})
        wait(lambda item:item.get('event')=='stopped')
        request('disconnect',{'terminateDebuggee':True})
        print('PASS LLDB DAP: breakpoint, stack, arguments, locals, string summary, stepping')
    finally:
        process.kill()
        process.wait(timeout=10)
