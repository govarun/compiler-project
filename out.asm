extern printf
section .text
	global main
main:
	push ebp
	mov ebp, esp
	sub esp, 4
	mov dword [ebp-4], 2
	mov eax, dword [ebp-4]
	imul eax, dword [ebp-4]
	push eax
	push __t_0
	mov [__t_1], eax
	call printf
	mov dword [__t_2], eax
	add esp, 8
	mov eax, 0
	mov esp, ebp
	pop ebp
	ret
section	.data
	__t_1	dd	0
	__t_2	dd	0
	getInt:	db	"%d"	
	__t_0:	db	"%d", 0
