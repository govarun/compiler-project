extern printf
extern scanf
extern malloc
section .text
	global main
main:
	push ebp
	mov ebp, esp
	sub esp, 84
	lea eax, [ebp-16]
	mov dword [ebp-20], eax
	add eax, 8
	mov ebx, [eax] 
	mov dword [ebp-28], ebx
	mov ebx, dword [ebp-32]
	imul ebx, 4
	mov ecx, eax
	add ecx, ebx
	mov dword [ebp-40], eax
	mov dword [ebp-36], ebx
	mov ebx, [ecx] 
	mov dword [ebp-48], ebx
	mov dword [ecx], 5
	lea ebx, [ebp-16]
	mov dword [ebp-52], ebx
	add ebx, 8
	mov edx, [ebx] 
	mov dword [ebp-60], edx
	mov edx, dword [ebp-64]
	imul edx, 4
	mov esi, ebx
	add esi, edx
	mov dword [ebp-72], ebx
	mov dword [ebp-68], edx
	mov edx, [esi] 
	mov dword [ebp-80], edx
	push dword [ebp-80]
	push __t_8
	mov dword [ebp-24], eax
	mov dword [ebp-56], ebx
	mov dword [ebp-44], ecx
	mov dword [ebp-76], esi
	call printf
	mov dword [ebp-84], eax
	add esp, 8
	mov eax, 0
	mov esp, ebp
	pop ebp
	ret
section	.data
	__t_8:	db	`%d `, 0
