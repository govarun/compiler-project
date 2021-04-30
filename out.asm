extern printf
extern scanf
section .text
	global main
main:
	push ebp
	mov ebp, esp
	sub esp, 36
	mov dword [ebp-4], 10
	lea eax, [ebp-4]
	mov ebx, [eax] 
	mov dword [ebp-16], ebx
	mov dword [eax], 1314
	mov ebx, [eax] 
	mov dword [ebp-20], ebx
	push dword [ebp-20]
	push eax
	push __t_2
	mov dword [ebp-8], eax
	mov dword [ebp-12], eax
	call printf
	mov dword [ebp-24], eax
	add esp, 12
	mov eax, dword [ebp-12]
	add eax, 1
	mov ebx, [eax] 
	mov dword [ebp-32], ebx
	push dword [ebp-32]
	push eax
	push __t_6
	mov dword [ebp-28], eax
	mov dword [ebp-12], eax
	call printf
	mov dword [ebp-36], eax
	add esp, 12
	mov eax, 0
	mov esp, ebp
	pop ebp
	ret
section	.data
	__t_2:	db	`%x %d\n`, 0
	__t_6:	db	`%x %d\n`, 0
