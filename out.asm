extern printf
extern scanf
extern malloc
extern free
section .text
	global main
main:
	push ebp
	mov ebp, esp
	sub esp, 16
	mov dword [ebp-8], 4
	mov eax, dword [ebp-8]
	push eax
	push __t_1
	mov dword [ebp-12], eax
	mov dword [ebp-8], eax
	call printf
	mov dword [ebp-16], eax
	add esp, 8
	mov eax, 0
	mov esp, ebp
	pop ebp
	ret
section	.data
	__t_1:	db	`%d`, 0
