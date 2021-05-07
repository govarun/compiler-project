extern printf
extern scanf
extern malloc
section .text
	global main
main:
	push ebp
	mov ebp, esp
	sub esp, 68
	lea eax, [ebp-8]
	mov dword [ebp-20], eax
	add eax, 0
	mov ebx, [eax] 
	mov dword [ebp-28], ebx
	mov dword [eax], 4
	lea ebx, [ebp-8]
	mov dword [ebp-32], ebx
	add ebx, 4
	mov ecx, [ebx] 
	mov dword [ebp-40], ecx
	mov dword [ebx], 12
	mov ecx, dword [ebp-8 + 0]
	mov dword [ebp-16 + 0], ecx
	mov ecx, dword [ebp-8 + 4]
	mov dword [ebp-16 + 4], ecx
	lea ecx, [ebp-16]
	mov dword [ebp-44], ecx
	add ecx, 0
	mov edx, [ecx] 
	mov dword [ebp-52], edx
	lea edx, [ebp-16]
	mov dword [ebp-56], edx
	add edx, 4
	mov esi, [edx] 
	mov dword [ebp-64], esi
	push dword [ebp-64]
	push dword [ebp-52]
	push __t_6
	mov dword [ebp-24], eax
	mov dword [ebp-36], ebx
	mov dword [ebp-48], ecx
	mov dword [ebp-60], edx
	call printf
	mov dword [ebp-68], eax
	add esp, 12
	mov eax, 0
	mov esp, ebp
	pop ebp
	ret
section	.data
	__t_6:	db	`%d , %d\n`, 0
