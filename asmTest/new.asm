extern printf
section .text
        global main
main:
        push ebp
        mov ebp, esp
        sub esp, 0
        push 1
        push __t_0
        call printf
        mov dword [__t_1], eax
        add esp, 8
        mov eax, 0
        mov esp, ebp
        pop ebp
        ret
section .data
        __t_1   dd      0
        getInt: db      "%d"
        __t_0:  db      "%d", 0