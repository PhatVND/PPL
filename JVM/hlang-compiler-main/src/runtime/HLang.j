.source HLang.java
.class public HLang
.super java/lang/Object

.method public static main([Ljava/lang/String;)V
.var 0 is args [Ljava/lang/String; from Label0 to Label1
Label0:
	invokestatic HLang/hello()V
	return
Label1:
.limit stack 0
.limit locals 1
.end method

.method public static hello()V
Label0:
	getstatic java/lang/System/out Ljava/io/PrintStream;
	ldc "Hi"
	invokevirtual java/io/PrintStream/println(Ljava/lang/String;)V
	return
Label1:
.limit stack 2
.limit locals 0
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
