extern printf
section .text
	global main
even:
	push ebp
	mov ebp, esp
	sub esp, 8
	push dword [ebp+8]
	push __t_0
	call printf
	mov dword [ebp-4], eax
	add esp, 8
	mov eax, dword [ebp+8]
	cmp eax, 0
	je __l2
	mov eax, 0
	jmp __l3
__l2:
	mov eax, 1
__l3:
	mov dword [ebp-8], eax
	cmp eax, 0
	je __l0
	mov eax, 0
	mov esp, ebp
	pop ebp
	ret
__l0:
	mov eax, 1
	mov esp, ebp
	pop ebp
	ret
main:
	push ebp
	mov ebp, esp
	sub esp, 12
	push 10
	call even
	mov dword [ebp-4], eax
	add esp, 4
	mov eax, dword [ebp-4]
	push eax
	push __t_4
	mov dword [ebp-4], eax
	mov dword [ebp-8], eax
	call printf
	mov dword [ebp-12], eax
	add esp, 8
	mov eax, 1
	mov esp, ebp
	pop ebp
	ret
section	.data
	__t_0:	db	`%d\n`, 0
	__t_4:	db	`%d\n`, 0
