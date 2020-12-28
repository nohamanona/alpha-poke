import os
import random
import subprocess
import json
import re
from typing import List, Optional
from logging import getLogger

from pathlib import Path
from typing import Union

ROOT_DIR = Path(__file__).resolve().parents[1]  # type: Path



proc = subprocess.Popen(['node', 'alpha_poke/js/simpipe'], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                         encoding='utf-8', cwd=str(ROOT_DIR))

def _writeChunk(commands: List[str]):
    # logger.debug("writeChunk " + json.dumps('\n'.join(commands)))
    print("writeChunk " + json.dumps('\n'.join(commands)))
    proc.stdin.write(json.dumps('\n'.join(commands)) + '\n')
    proc.stdin.flush()

def _readChunk() -> List[str]:
    line = proc.stdout.readline()
    # logger.debug("readChunk " + line)
    rawstr = json.loads(line)
    print("readChunk " + rawstr)
    # return rawstr.split('\n', 1)  # 最初の1要素(update, endなど)のみ分離

# spec = {'formatid': 'gen2customgame'}
spec = {'formatid': 'gen7randombattle'}
name = {"name":"Alice"}
name2 = {"name":"Bob"}
_writeChunk([
    f'>start {json.dumps(spec)}',
    # f'>player p1 {json.dumps(name)}',
    # f'>player p2 {json.dumps(name2)}',
    # f'>p1 move 1',
    # f'>p2 move 1',
])
_readChunk()
_writeChunk([
    f'>player p1 {json.dumps(name)}',
])
_readChunk()
_writeChunk([
    f'>player p2 {json.dumps(name2)}',
])
_readChunk()
_readChunk()
_readChunk()
_writeChunk([
    f'>p1 move 1',
])
# _readChunk()
_writeChunk([
    f'>p2 move 1',
])
_readChunk()
_readChunk()
_readChunk()
# a = input("choice p1")
# _writeChunk([
#     f'' + a
# ])
# _readChunk()
# a = input("choice p2")
# _writeChunk([
#     f'' + a
# ])
# _readChunk()
# a = input("choice p1")
# _writeChunk([
#     f'' + a
# ])
# _readChunk()
# a = input("choice p2")
# _writeChunk([
#     f'' + a
# ])
# _readChunk()