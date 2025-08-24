.source HLang.java
.class public HLang
.super java/lang/Object

.method public static main([Ljava/lang/String;)V
.var 0 is args [Ljava/lang/String; from Label0 to Label1
Label0:
.var 1 is total I from Label0 to Label1
	iconst_0
	istore_1
.var 2 is arr [I from Label0 to Label1
	iconst_5
	newarray int
	dup
	iconst_0
	iconst_1
iastore
	dup
	iconst_1
	iconst_2
iastore
	dup
	iconst_2
	iconst_3
iastore
	dup
	iconst_3
	iconst_4
iastore
	dup
	iconst_4
	iconst_5
iastore
	astore_2
.var 3 is __idx I from Label2 to Label3
.var 4 is x I from Label2 to Label3
.var 5 is __array [I from Label2 to Label3
	iconst_0
	istore_3
	aload_2
	astore 5
Label2:
Label4:
	iload_3
	aload 5
arraylength
if_icmpge Label5
	aload 5
	iload_3
	iaload
	istore 4
	iload_1
	iload 4
	iadd
	istore_1
Label6:
	iload_3
	iconst_1
	iadd
	istore_3
	goto Label4
Label5:
Label3:
	getstatic java/lang/System/out Ljava/io/PrintStream;
new java/lang/StringBuilder
dup
	ldc ""
	invokespecial java/lang/StringBuilder/<init>(Ljava/lang/String;)V
	iload_1
	invokevirtual java/lang/StringBuilder/append(I)Ljava/lang/StringBuilder;
	invokevirtual java/lang/StringBuilder/toString()Ljava/lang/String;
	invokevirtual java/io/PrintStream/println(Ljava/lang/String;)V
	return
Label1:
.limit stack 21
.limit locals 6
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
