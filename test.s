	.file	"test.c"
	.text
	.globl	eps
	.data
	.align 4
	.type	eps, @object
	.size	eps, 4
eps:
	.long	1008981770
	.section	.rodata
.LC1:
	.string	"eps = %f, mult = %f, x = %d\n"
	.text
	.globl	main
	.type	main, @function
main:
.LFB0:
	.cfi_startproc
	endbr64
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
	subq	$16, %rsp
	movss	eps(%rip), %xmm1
	movss	.LC0(%rip), %xmm0
	mulss	%xmm1, %xmm0
	cvttss2sil	%xmm0, %eax
	movl	%eax, -4(%rbp)
	movss	eps(%rip), %xmm1
	movss	.LC0(%rip), %xmm0
	mulss	%xmm1, %xmm0
	cvtss2sd	%xmm0, %xmm1
	movss	eps(%rip), %xmm0
	cvtss2sd	%xmm0, %xmm0
	movl	-4(%rbp), %eax
	movl	%eax, %esi
	leaq	.LC1(%rip), %rdi
	movl	$2, %eax
	call	printf@PLT
	movl	$0, %eax
	leave
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE0:
	.size	main, .-main
	.section	.rodata
	.align 4
.LC0:
	.long	1125515264
	.ident	"GCC: (Ubuntu 9.3.0-17ubuntu1~20.04) 9.3.0"
	.section	.note.GNU-stack,"",@progbits
	.section	.note.gnu.property,"a"
	.align 8
	.long	 1f - 0f
	.long	 4f - 1f
	.long	 5
0:
	.string	 "GNU"
1:
	.align 8
	.long	 0xc0000002
	.long	 3f - 2f
2:
	.long	 0x3
3:
	.align 8
4:
