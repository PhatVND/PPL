.source HLang.java
.class public HLang
.super java/lang/Object

.method public static main([Ljava/lang/String;)V
.var 0 is args [Ljava/lang/String; from Label0 to Label1
Label0:
	getstatic java/lang/System/out Ljava/io/PrintStream;
	iconst_3
	iconst_4
	invokestatic HLang/add(II)I
	invokevirtual java/io/PrintStream/println(I)V
	return
Label1:
.limit stack 3
.limit locals 1
.end method

.method public static add(II)I
.var 0 is a I from Label0 to Label1
.var 1 is b I from Label0 to Label1
Label0:
	iload_0
	iload_1
	iadd
	ireturn
Label1:
.limit stack 2
.limit locals 2
.end method

.method public <init>()V
.var 0 is this LHLang; from Label0 to Label1
Label0:
	aload_0
	invokespecial java/lang/Object/<init>()V
	return
Label1:
.limit stack 1
.limit locals 1
.end method
