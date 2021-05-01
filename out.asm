extern printf
extern scanf
extern malloc
section .text
	global main
main:
	push ebp
	mov ebp, esp
	sub esp, 184
	mov eax, 5
	imul eax, 8
	push eax
	call malloc
	add esp, 4
	mov [ebp-8], eax
	mov dword [ebp-12], 0
	mov dword [ebp-12], 0
__l0:
	mov eax, dword [ebp-12]
	cmp eax, 5
	jl __l8
	mov eax, 0
	jmp __l9
__l8:
	mov eax, 1
__l9:
	mov dword [ebp-16], eax
	cmp eax, 0
	je __l1
	jmp __l2
__l3:
	mov eax, dword [ebp-12]
	mov dword [ebp-20], eax
	mov dword [ebp-12], eax
	inc eax
	mov dword [ebp-12], eax
	jmp __l0
__l2:
	mov eax, dword [ebp-12]
	mov ebx, eax
	imul ebx, 8
	mov dword [ebp-32], eax
	mov ecx, dword [ebp-8]
	mov dword [ebp-40], ecx
	add ecx, ebx
	mov dword [ebp-36], ebx
	mov ebx, [ecx] 
	mov dword [ebp-52], ebx
	mov ebx, ecx
	add ebx, 0
	mov dword [ebp-56], ecx
	mov edx, [ebx] 
	mov dword [ebp-64], edx
	mov edx, eax
	imul edx, eax
	mov [ebx], edx
	mov esi, eax
	imul esi, 8
	mov dword [ebp-72], eax
	mov edi, dword [ebp-8]
	mov dword [ebp-80], edi
	add edi, esi
	mov dword [ebp-76], esi
	mov esi, [edi] 
	mov dword [ebp-92], esi
	mov esi, edi
	add esi, 4
	mov dword [ebp-96], edi
	mov dword [ebp-12], eax
	mov eax, [esi] 
	mov dword [ebp-104], eax
	mov eax, dword [ebp-12]
	add eax, 3
	mov [esi], eax
	mov dword [ebp-108], eax
	mov dword [ebp-60], ebx
	mov dword [ebp-44], ecx
	mov dword [ebp-68], edx
	mov dword [ebp-100], esi
	mov dword [ebp-84], edi
	jmp __l3
__l1:
	mov dword [ebp-12], 0
__l4:
	mov eax, dword [ebp-12]
	cmp eax, 5
	jl __l10
	mov eax, 0
	jmp __l11
__l10:
	mov eax, 1
__l11:
	mov dword [ebp-24], eax
	cmp eax, 0
	je __l5
	jmp __l6
__l7:
	mov eax, dword [ebp-12]
	mov dword [ebp-28], eax
	mov dword [ebp-12], eax
	inc eax
	mov dword [ebp-12], eax
	jmp __l4
__l6:
	mov eax, dword [ebp-12]
	mov ebx, eax
	imul ebx, 8
	mov dword [ebp-112], eax
	mov ecx, dword [ebp-8]
	mov dword [ebp-120], ecx
	add ecx, ebx
	mov dword [ebp-116], ebx
	mov ebx, [ecx] 
	mov dword [ebp-132], ebx
	mov ebx, ecx
	add ebx, 0
	mov dword [ebp-136], ecx
	mov edx, [ebx] 
	mov dword [ebp-144], edx
	mov edx, eax
	imul edx, 8
	mov dword [ebp-148], eax
	mov esi, dword [ebp-8]
	mov dword [ebp-156], esi
	add esi, edx
	mov dword [ebp-152], edx
	mov edx, [esi] 
	mov dword [ebp-168], edx
	mov edx, esi
	add edx, 4
	mov dword [ebp-172], esi
	mov edi, [edx] 
	mov dword [ebp-180], edi
	push dword [ebp-180]
	push dword [ebp-144]
	push __t_22
	mov dword [ebp-12], eax
	mov dword [ebp-140], ebx
	mov dword [ebp-124], ecx
	mov dword [ebp-176], edx
	mov dword [ebp-160], esi
	call printf
	mov dword [ebp-184], eax
	add esp, 12
	jmp __l7
__l5:
	mov eax, 0
	mov esp, ebp
	pop ebp
	ret
section	.data
	__t_22:	db	`%d %d \n`, 0
