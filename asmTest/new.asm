extern printf
section .text
        global main
f:
        push ebp
        mov ebp, esp
        sub esp, 0
        mov eax, [ebp+8]
        add eax, [ebp+8]
        mov dword [__t_0], eax
        mov eax, dword [__t_0]
        mov esp, ebp
        pop ebp
        ret
main:
        push ebp
        mov ebp, esp
        sub esp, 4
        push 5
        call f
        mov dword [__t_1], eax
        add esp, 4
        mov [ebp-4], eax
        mov eax, dword [__t_1]
        push eax
        push __t_2
        mov eax, [ebp-4]
        call printf
        mov dword [__t_3], eax
        add esp, 8
        mov eax, 0
        mov esp, ebp
        pop ebp
        ret
section .data
        __t_0   dd      0
        __t_1   dd      0
        __t_3   dd      0
        getInt: db      "%d"
        __t_2:  db      "%d", 0