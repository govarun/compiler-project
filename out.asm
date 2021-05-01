extern printf
extern scanf
extern malloc
section .text
	global main
main:
	push ebp
	mov ebp, esp
	sub esp, 24
	lea eax, [ebp-4]
	mov dword [ebp-12], eax
	add eax, 0
	mov ebx, [eax] 
	mov dword [ebp-20], ebx
