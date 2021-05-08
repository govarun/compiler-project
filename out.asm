extern printf
extern scanf
extern malloc
extern free
section .text
	global main
main:
	push ebp
	mov ebp, esp
	sub esp, 416
	mov eax, 4
	imul eax, 4
	push eax
	call malloc
	add esp, 4
	mov [ebp-4], eax
	mov eax, 4
	imul eax, 4
	push eax
	call malloc
	add esp, 4
	mov [ebp-8], eax
	mov eax, 4
	imul eax, 4
	push eax
	call malloc
	add esp, 4
	mov [ebp-12], eax
	mov dword [ebp-16], 0
__l0:
	mov eax, dword [ebp-16]
	cmp eax, 2
	jl __l44
	mov eax, 0
	jmp __l45
__l44:
	mov eax, 1
__l45:
	mov dword [ebp-28], eax
	cmp eax, 0
	je __l1
	jmp __l2
__l3:
	mov eax, dword [ebp-16]
	mov dword [ebp-32], eax
	mov dword [ebp-16], eax
	inc eax
	mov dword [ebp-16], eax
	jmp __l0
__l2:
	mov dword [ebp-20], 0
__l4:
	mov eax, dword [ebp-20]
	cmp eax, 2
	jl __l46
	mov eax, 0
	jmp __l47
__l46:
	mov eax, 1
__l47:
	mov dword [ebp-76], eax
	cmp eax, 0
	je __l5
	jmp __l6
__l7:
	mov eax, dword [ebp-20]
	mov dword [ebp-80], eax
	mov dword [ebp-20], eax
	inc eax
	mov dword [ebp-20], eax
	jmp __l4
__l6:
	mov eax, dword [ebp-16]
	mov ebx, eax
	imul ebx, 2
	mov dword [ebp-84], eax
	mov dword [ebp-92], ebx
	add ebx, dword [ebp-20]
	mov dword [ebp-88], ebx
	imul ebx, 4
	mov ecx, dword [ebp-4]
	mov dword [ebp-100], ecx
	add ecx, ebx
	mov dword [ebp-96], ebx
	mov ebx, [ecx] 
	mov dword [ebp-108], ebx
	mov ebx, eax
	add ebx, dword [ebp-20]
	mov dword [ebp-112], ebx
	add ebx, 1
	mov [ecx], ebx
	mov edx, eax
	imul edx, 2
	mov dword [ebp-120], eax
	mov dword [ebp-128], edx
	add edx, dword [ebp-20]
	mov dword [ebp-124], edx
	imul edx, 4
	mov esi, dword [ebp-8]
	mov dword [ebp-136], esi
	add esi, edx
	mov dword [ebp-132], edx
	mov edx, [esi] 
	mov dword [ebp-144], edx
	mov edx, eax
	sub edx, dword [ebp-20]
	mov dword [ebp-148], edx
	add edx, 1
	mov [esi], edx
	mov edi, eax
	imul edi, 2
	mov dword [ebp-156], eax
	mov dword [ebp-164], edi
	add edi, dword [ebp-20]
	mov dword [ebp-160], edi
	imul edi, 4
	mov dword [ebp-16], eax
	mov eax, dword [ebp-12]
	mov dword [ebp-172], eax
	add eax, edi
	mov dword [ebp-168], edi
	mov edi, [eax] 
	mov dword [ebp-180], edi
	mov dword [eax], 0
	mov dword [ebp-176], eax
	mov dword [ebp-116], ebx
	mov dword [ebp-104], ecx
	mov dword [ebp-152], edx
	mov dword [ebp-140], esi
	jmp __l7
__l5:
	jmp __l3
__l1:
	mov dword [ebp-16], 0
__l8:
	mov eax, dword [ebp-16]
	cmp eax, 2
	jl __l48
	mov eax, 0
	jmp __l49
__l48:
	mov eax, 1
__l49:
	mov dword [ebp-36], eax
	cmp eax, 0
	je __l9
	jmp __l10
__l11:
	mov eax, dword [ebp-16]
	mov dword [ebp-40], eax
	mov dword [ebp-16], eax
	inc eax
	mov dword [ebp-16], eax
	jmp __l8
__l10:
	mov dword [ebp-20], 0
__l12:
	mov eax, dword [ebp-20]
	cmp eax, 2
	jl __l50
	mov eax, 0
	jmp __l51
__l50:
	mov eax, 1
__l51:
	mov dword [ebp-184], eax
	cmp eax, 0
	je __l13
	jmp __l14
__l15:
	mov eax, dword [ebp-20]
	mov dword [ebp-20], eax
	mov dword [ebp-188], eax
	inc eax
	mov dword [ebp-20], eax
	jmp __l12
__l14:
	mov dword [ebp-24], 0
__l16:
	mov eax, dword [ebp-24]
	cmp eax, 2
	jl __l52
	mov eax, 0
	jmp __l53
__l52:
	mov eax, 1
__l53:
	mov dword [ebp-192], eax
	cmp eax, 0
	je __l17
	jmp __l18
__l19:
	mov eax, dword [ebp-24]
	mov dword [ebp-196], eax
	mov dword [ebp-24], eax
	inc eax
	mov dword [ebp-24], eax
	jmp __l16
__l18:
	mov eax, dword [ebp-16]
	mov ebx, eax
	imul ebx, 2
	mov dword [ebp-200], eax
	mov dword [ebp-208], ebx
	add ebx, dword [ebp-20]
	mov dword [ebp-204], ebx
	imul ebx, 4
	mov ecx, dword [ebp-12]
	mov dword [ebp-216], ecx
	add ecx, ebx
	mov dword [ebp-212], ebx
	mov ebx, [ecx] 
	mov dword [ebp-224], ebx
	mov ebx, eax
	imul ebx, 2
	mov dword [ebp-228], eax
	mov dword [ebp-236], ebx
	add ebx, dword [ebp-24]
	mov dword [ebp-232], ebx
	imul ebx, 4
	mov edx, dword [ebp-4]
	mov dword [ebp-244], edx
	add edx, ebx
	mov dword [ebp-240], ebx
	mov ebx, [edx] 
	mov dword [ebp-252], ebx
	mov ebx, dword [ebp-24]
	mov esi, ebx
	imul esi, 2
	mov dword [ebp-256], ebx
	mov dword [ebp-264], esi
	add esi, dword [ebp-20]
	mov dword [ebp-260], esi
	imul esi, 4
	mov edi, dword [ebp-8]
	mov dword [ebp-272], edi
	add edi, esi
	mov dword [ebp-268], esi
	mov esi, [edi] 
	mov dword [ebp-280], esi
	mov esi, dword [ebp-252]
	imul esi, dword [ebp-280]
	mov dword [ebp-16], eax
	mov eax, dword [ebp-224]
	add eax, esi
	mov dword [ebp-284], esi
	mov dword [ebp-224], eax
	mov dword [ebp-24], ebx
	mov dword [ebp-220], ecx
	mov dword [ebp-248], edx
	mov dword [ebp-276], edi
	jmp __l19
__l17:
	jmp __l15
__l13:
	jmp __l11
__l9:
	mov dword [ebp-16], 0
__l20:
	mov eax, dword [ebp-16]
	cmp eax, 2
	jl __l54
	mov eax, 0
	jmp __l55
__l54:
	mov eax, 1
__l55:
	mov dword [ebp-44], eax
	cmp eax, 0
	je __l21
	jmp __l22
__l23:
	mov eax, dword [ebp-16]
	mov dword [ebp-48], eax
	mov dword [ebp-16], eax
	inc eax
	mov dword [ebp-16], eax
	jmp __l20
__l22:
	mov dword [ebp-20], 0
__l24:
	mov eax, dword [ebp-20]
	cmp eax, 2
	jl __l56
	mov eax, 0
	jmp __l57
__l56:
	mov eax, 1
__l57:
	mov dword [ebp-288], eax
	cmp eax, 0
	je __l25
	jmp __l26
__l27:
	mov eax, dword [ebp-20]
	mov dword [ebp-20], eax
	mov dword [ebp-292], eax
	inc eax
	mov dword [ebp-20], eax
	jmp __l24
__l26:
	mov eax, dword [ebp-16]
	mov ebx, eax
	imul ebx, 2
	mov dword [ebp-300], eax
	mov dword [ebp-308], ebx
	add ebx, dword [ebp-20]
	mov dword [ebp-304], ebx
	imul ebx, 4
	mov ecx, dword [ebp-4]
	mov dword [ebp-316], ecx
	add ecx, ebx
	mov dword [ebp-312], ebx
	mov ebx, [ecx] 
	mov dword [ebp-324], ebx
	push dword [ebp-324]
	push __t_61
	mov dword [ebp-16], eax
	mov dword [ebp-320], ecx
	call printf
	mov dword [ebp-328], eax
	add esp, 8
	jmp __l27
__l25:
	push __t_70
	call printf
	mov dword [ebp-296], eax
	add esp, 4
	jmp __l23
__l21:
	push __t_72
	call printf
	mov dword [ebp-52], eax
	add esp, 4
	mov dword [ebp-16], 0
__l28:
	mov eax, dword [ebp-16]
	cmp eax, 2
	jl __l58
	mov eax, 0
	jmp __l59
__l58:
	mov eax, 1
__l59:
	mov dword [ebp-56], eax
	cmp eax, 0
	je __l29
	jmp __l30
__l31:
	mov eax, dword [ebp-16]
	mov dword [ebp-60], eax
	mov dword [ebp-16], eax
	inc eax
	mov dword [ebp-16], eax
	jmp __l28
__l30:
	mov dword [ebp-20], 0
__l32:
	mov eax, dword [ebp-20]
	cmp eax, 2
	jl __l60
	mov eax, 0
	jmp __l61
__l60:
	mov eax, 1
__l61:
	mov dword [ebp-332], eax
	cmp eax, 0
	je __l33
	jmp __l34
__l35:
	mov eax, dword [ebp-20]
	mov dword [ebp-20], eax
	mov dword [ebp-336], eax
	inc eax
	mov dword [ebp-20], eax
	jmp __l32
__l34:
	mov eax, dword [ebp-16]
	mov ebx, eax
	imul ebx, 2
	mov dword [ebp-344], eax
	mov dword [ebp-352], ebx
	add ebx, dword [ebp-20]
	mov dword [ebp-348], ebx
	imul ebx, 4
	mov ecx, dword [ebp-8]
	mov dword [ebp-360], ecx
	add ecx, ebx
	mov dword [ebp-356], ebx
	mov ebx, [ecx] 
	mov dword [ebp-368], ebx
	push dword [ebp-368]
	push __t_78
	mov dword [ebp-16], eax
	mov dword [ebp-364], ecx
	call printf
	mov dword [ebp-372], eax
	add esp, 8
	jmp __l35
__l33:
	push __t_87
	call printf
	mov dword [ebp-340], eax
	add esp, 4
	jmp __l31
__l29:
	push __t_89
	call printf
	mov dword [ebp-64], eax
	add esp, 4
	mov dword [ebp-16], 0
__l36:
	mov eax, dword [ebp-16]
	cmp eax, 2
	jl __l62
	mov eax, 0
	jmp __l63
__l62:
	mov eax, 1
__l63:
	mov dword [ebp-68], eax
	cmp eax, 0
	je __l37
	jmp __l38
__l39:
	mov eax, dword [ebp-16]
	mov dword [ebp-16], eax
	mov dword [ebp-72], eax
	inc eax
	mov dword [ebp-16], eax
	jmp __l36
__l38:
	mov dword [ebp-20], 0
__l40:
	mov eax, dword [ebp-20]
	cmp eax, 2
	jl __l64
	mov eax, 0
	jmp __l65
__l64:
	mov eax, 1
__l65:
	mov dword [ebp-376], eax
	cmp eax, 0
	je __l41
	jmp __l42
__l43:
	mov eax, dword [ebp-20]
	mov dword [ebp-20], eax
	mov dword [ebp-380], eax
	inc eax
	mov dword [ebp-20], eax
	jmp __l40
__l42:
	mov eax, dword [ebp-16]
	mov ebx, eax
	imul ebx, 2
	mov dword [ebp-388], eax
	mov dword [ebp-396], ebx
	add ebx, dword [ebp-20]
	mov dword [ebp-392], ebx
	imul ebx, 4
	mov ecx, dword [ebp-12]
	mov dword [ebp-404], ecx
	add ecx, ebx
	mov dword [ebp-400], ebx
	mov ebx, [ecx] 
	mov dword [ebp-412], ebx
	push dword [ebp-412]
	push __t_95
	mov dword [ebp-16], eax
	mov dword [ebp-408], ecx
	call printf
	mov dword [ebp-416], eax
	add esp, 8
	jmp __l43
__l41:
	push __t_104
	call printf
	mov dword [ebp-384], eax
	add esp, 4
	jmp __l39
__l37:
	mov eax, 0
	mov esp, ebp
	pop ebp
	ret
section	.data
	__t_61:	db	`%d `, 0
	__t_70:	db	`\n`, 0
	__t_72:	db	`\n`, 0
	__t_78:	db	`%d `, 0
	__t_87:	db	`\n`, 0
	__t_89:	db	`\n`, 0
	__t_95:	db	`%d `, 0
	__t_104:	db	`\n`, 0
