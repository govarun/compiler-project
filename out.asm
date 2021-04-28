extern printf
section .text
	global main
even:
	push ebp
	mov ebp, esp
	sub esp, 20
	mov eax, dword [ebp-4]
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
	mov eax, dword [ebp-4]
	sub eax, 1
	push eax
	mov dword [ebp-12], eax
	call odd
	mov dword [ebp-16], eax
	add esp, 4
	mov eax, 1
	add eax, dword [ebp-16]
	mov dword [ebp-20], eax
	mov esp, ebp
	pop ebp
	ret
odd:
	push ebp
	mov ebp, esp
	sub esp, 16
	mov eax, dword [ebp-4]
	sub eax, 1
	push eax
	mov dword [ebp-8], eax
	call even
	mov dword [ebp-12], eax
	add esp, 4
	mov eax, 1
	add eax, dword [ebp-12]
	mov dword [ebp-16], eax
	mov esp, ebp
	pop ebp
	ret
main:
	push ebp
	mov ebp, esp
	sub esp, 12
	push 4
	call even
	mov dword [ebp-4], eax
	add esp, 4
	mov eax, dword [ebp-4]
	push eax
	push __t_8
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
	__t_8:	db	`%d\n`, 0
