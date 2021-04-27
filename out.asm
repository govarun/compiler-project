extern printf
section .text
	global main
f:
	push dword ebp
	mov ebp, esp
	sub esp, 0
	mov eax, [ebp+8]
	mov esp, ebp
	pop ebp
	ret
main:
	push ebp
	mov ebp, esp
	sub esp, 8
	mov dword [ebp-8], 5
	push dword [ebp-8]
	call f
	mov dword [__t_0], eax
	add esp, 4
	mov [ebp-4], eax
	mov eax, dword [__t_0]
	push eax
	push __t_1
	mov eax, [ebp-4]
	call printf
	mov dword [__t_2], eax
	add esp, 8
	mov eax, 0
	mov esp, ebp
	pop ebp
	ret
section	.data
	__t_0	dd	0
	__t_2	dd	0
	getInt:	db	"%d"	
	__t_1:	db	"%d", 0
