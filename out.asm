extern printf
extern scanf
extern malloc
extern free
section .text
	global main
main:
	push ebp
	mov ebp, esp
	sub esp, 4
	mov eax, None
	mov dword [ebp-4], eax
	mov eax, 0
	mov esp, ebp
	pop ebp
	ret
section	.data
