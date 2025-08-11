.source HLang.java
.class public HLang
.super java/lang/Object

.method public static main([Ljava/lang/String;)V
.var 0 is args [Ljava/lang/String; from Label0 to Label1
Label0:
.var 1 is i I from Label0 to Label1
	iconst_1
	istore_1
.var 2 is sum I from Label0 to Label1
	iconst_0
	istore_2
Label4:
	iload_1
	iconst_5
	if_icmpgt Label5
	iconst_1
	goto Label6
Label5:
	iconst_0
Label6:
	ifle Label3
	iload_2
	iload_1
	iadd
	istore_2
	iload_1
	iconst_1
	iadd
	istore_1
Label2:
	goto Label4
Label3:
	getstatic java/lang/System/out Ljava/io/PrintStream;
	iload_2
	invokevirtual java/io/PrintStream/println(I)V
	return
Label1:
.limit stack 8
.limit locals 3
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
