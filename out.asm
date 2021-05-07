extern printf
extern scanf
extern malloc
section .text
	global main
main:
	push ebp
	mov ebp, esp
	sub esp, 72
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
	mov ecx, 8
	imul ecx, 13
	mov [ebx], ecx
	lea edx, [ebp-8]
	mov esi, edx
	add esi, 0
	mov edi, [esi] 
	mov dword [ebp-60], edi
	mov edi, edx
	add edi, 4
	mov dword [ebp-16], edx
	mov dword [ebp-24], eax
	mov eax, [edi] 
	mov dword [ebp-68], eax
	push dword [ebp-68]
	push dword [ebp-60]
	push __t_8
	mov dword [ebp-36], ebx
	mov dword [ebp-44], ecx
	mov dword [ebp-52], edx
	mov dword [ebp-56], esi
	mov dword [ebp-64], edi
	call printf
	mov dword [ebp-72], eax
	add esp, 12
	mov eax, 0
	mov esp, ebp
	pop ebp
	ret
section	.data
	__t_8:	db	`%d , %d\n`, 0
