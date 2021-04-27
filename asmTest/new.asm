extern printf
section .text
        global main
main:
        push ebp
        mov ebp, esp
        sub esp, 8
        mov dword [ebp-4], 1000000000
        mov eax, dword [ebp-4]
        sub eax, 1
        mov [ebp-8], eax
        call printf
        mov dword [__t_2], eax
        add esp, 0
        mov eax, 1
        mov esp, ebp
        pop ebp
        ret
section .data
        __t_0   dd      0
        __t_2   dd      0
        __t_1:  db      "%d %d", 0