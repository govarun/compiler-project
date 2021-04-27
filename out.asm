extern printf
section .text
	global main
main:
	push ebp
	mov ebp, esp
	sub esp, 8
	mov dword [ebp-4], 1
	mov eax, dword [ebp-4]
	add eax, 10
	push eax
	push dword [ebp-4]
	push dword [ebp-4]
	push __t_1
	mov [ebp-8], eax
	call printf
	mov dword [__t_2], eax
	add esp, 16
	push __t_3
	call printf
	mov dword [__t_4], eax
	add esp, 4
	mov eax, 1
	mov esp, ebp
	pop ebp
	ret
section	.data
	__t_0	dd	0
	__t_2	dd	0
	__t_4	dd	0
	__t_1:	db	`%d %d %d\n`, 0
	__t_3:	db	`1`, 0
