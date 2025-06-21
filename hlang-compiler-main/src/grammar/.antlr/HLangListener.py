# Generated from d:/StudyingStuffs/ThirdYear/PPL/Assignment/hlang-compiler-main/src/grammar/HLang.g4 by ANTLR 4.13.1
from antlr4 import *
if "." in __name__:
    from .HLangParser import HLangParser
else:
    from HLangParser import HLangParser

# This class defines a complete listener for a parse tree produced by HLangParser.
class HLangListener(ParseTreeListener):

    # Enter a parse tree produced by HLangParser#program.
    def enterProgram(self, ctx:HLangParser.ProgramContext):
        pass

    # Exit a parse tree produced by HLangParser#program.
    def exitProgram(self, ctx:HLangParser.ProgramContext):
        pass



del HLangParser