
from token import *
from jack_lexer import *



#statement functions
def compile_return_statement(lexer):
    tree="<returnStatement>\n"
    tree+=compile_expected_token(lexer,Token_Type.RETURN)
    lexer.peek_ahead(1)
    if lexer.cur_token.token_type != Token_Type.SEMICOLON:
        tree+=compile_expression(lexer)
    tree+=compile_expected_token(lexer,Token_Type.SEMICOLON)
    tree+="</returnStatement>\n"
    return tree

def compile_do_statement(lexer):
    tree="<doStatement>\n"
    tree+=compile_expected_token(lexer,Token_Type.DO)
    tree+=compile_subroutine_call(lexer)
    tree+=compile_expected_token(lexer,Token_Type.SEMICOLON)
    tree+="</doStatement>\n"
    return tree

def get_xml_name(token):
    if token.name == "<":
        return "&lt;"
    elif token.name == ">":
        return "&gt;"
    elif token.name == "&":
        return "&amp;"
    else:
        return token.name

def compile_while_statement(lexer):
    tree="<whileStatement>\n"
    tree+=compile_expected_token(lexer,Token_Type.WHILE)
    tree+=compile_expected_token(lexer,Token_Type.LEFT_PAREN)
    tree+=compile_expression(lexer)
    tree+=compile_expected_token(lexer,Token_Type.RIGHT_PAREN)
    tree+=compile_expected_token(lexer,Token_Type.LEFT_CURLY)
    tree+=compile_multiple_statements(lexer)
    tree+=compile_expected_token(lexer,Token_Type.RIGHT_CURLY)
    tree+="</whileStatement>\n"
    return tree

def compile_if_statement(lexer):
    tree="<ifStatement>\n"
    tree+=compile_expected_token(lexer,Token_Type.IF)
    tree+=compile_expected_token(lexer,Token_Type.LEFT_PAREN)
    tree+=compile_expression(lexer)
    tree+=compile_expected_token(lexer,Token_Type.RIGHT_PAREN)
    tree+=compile_expected_token(lexer,Token_Type.LEFT_CURLY)
    tree+=compile_multiple_statements(lexer)
    tree+=compile_expected_token(lexer,Token_Type.RIGHT_CURLY)
    lexer.peek_ahead(1)
    if lexer.cur_token.token_type == Token_Type.ELSE:
        tree+=compile_expected_token(lexer,Token_Type.ELSE)
        tree+=compile_expected_token(lexer,Token_Type.LEFT_CURLY)
        tree+=compile_multiple_statements(lexer)
        tree+=compile_expected_token(lexer,Token_Type.RIGHT_CURLY)
    tree+="</ifStatement>\n"
    return tree

def compile_let_statement(lexer):
    tree="<letStatement>\n"
    tree+=compile_expected_token(lexer,Token_Type.LET)
    tree+=compile_identifier(lexer)
    lexer.peek_ahead(1)
    if lexer.cur_token.token_type == Token_Type.LEFT_BRACKET:
        tree+=compile_expected_token(lexer,Token_Type.LEFT_BRACKET)
        tree+=compile_expression(lexer) 
        tree+=compile_expected_token(lexer,Token_Type.RIGHT_BRACKET)
        tree+=compile_expected_token(lexer,Token_Type.EQUALS)
    else:
        tree+=compile_expected_token(lexer,Token_Type.EQUALS)
    tree+=compile_expression(lexer) 
    tree+=compile_expected_token(lexer,Token_Type.SEMICOLON)
    tree+="</letStatement>\n"
    return tree


statement_maps = {
Token_Type.LET: compile_let_statement,
Token_Type.IF:compile_if_statement,
Token_Type.WHILE:compile_while_statement,
 Token_Type.DO:compile_do_statement ,
Token_Type.RETURN:compile_return_statement}

def compile_class(lexer): 
    tree="<class>\n"
    tree+= compile_expected_token(lexer,Token_Type.CLASS)
    tree+=compile_identifier(lexer)
    tree+=compile_expected_token(lexer,Token_Type.LEFT_CURLY)
    #for var decs
    while True:
        lexer.peek_ahead(1)
        if lexer.cur_token.token_type == Token_Type.STATIC or lexer.cur_token.token_type == Token_Type.FIELD:
            tree+=compile_class_var_dec(lexer)
        else:
            break
    #for function defs
    while True:
        lexer.peek_ahead(1)
        if lexer.cur_token.token_type == Token_Type.FUNCTION or lexer.cur_token.token_type == Token_Type.METHOD or lexer.cur_token.token_type == Token_Type.CONSTRUCTOR:
            tree+=compile_subroutine_dec(lexer)
        else:
            break
    tree+=compile_expected_token(lexer,Token_Type.RIGHT_CURLY)
    tree+="</class>\n"
    return tree

def compile_next_token(lexer):
    lexer.lex_next_token()
    s = token_class_to_str(lexer.cur_token.token_class)
    name = get_xml_name(lexer.cur_token)
    tree = f"<{s}> {name} </{s}>\n"
    return tree

def compile_class_var_dec(lexer):
    tree="<classVarDec>\n"
    tree+=compile_next_token(lexer) 
    if lexer.cur_token.token_type != Token_Type.FIELD and lexer.cur_token.token_type != Token_Type.STATIC:
        lexer.error_log+=f"syntax error: field or static expected, not {lexer.cur_token.name}\n" 
        lexer.error_log+=f"{lexer.cur_file}: line {lexer.cur_line}:{lexer.line_pos}\n"
    tree+=compile_type(lexer)
    while True:
        tree+=compile_identifier(lexer)
        tree+=compile_next_token(lexer)
        if lexer.cur_token.token_type == Token_Type.SEMICOLON:
           break
        elif lexer.cur_token.token_type == Token_Type.COMMA:
           pass
        else:
            lexer.error_log+=f"syntax error: semicolon expected to end declaration, not {lexer.cur_token.name}\n"
            lexer.error_log+=f"{lexer.cur_file}: line {lexer.cur_line}:{lexer.line_pos}\n"
    tree+="</classVarDec>\n"
    return tree

def compile_subroutine_dec(lexer): 
    tree="<subroutineDec>\n"
    tree+=compile_next_token(lexer)
    if not(lexer.cur_token.token_type == Token_Type.FUNCTION or lexer.cur_token.token_type == Token_Type.METHOD or lexer.cur_token.token_type == Token_Type.CONSTRUCTOR):
        lexer.error_log+=f"syntax error: keywords function, method, or constructor expected, not {lexer.cur_token.name}\n"
        lexer.error_log+=f"{lexer.cur_file}: line {lexer.cur_line}:{lexer.line_pos}\n"
    lexer.peek_ahead(1)
    if lexer.cur_token.token_type == Token_Type.VOID:
         tree+=compile_next_token(lexer)
    else:
        tree+=compile_type(lexer) 
    tree+=compile_identifier(lexer)
    tree+=compile_expected_token(lexer,Token_Type.LEFT_PAREN)
    tree+=compile_parameter_list(lexer) 
    tree+=compile_expected_token(lexer,Token_Type.RIGHT_PAREN)
    tree+=compile_subroutine_body(lexer) 
    tree+="</subroutineDec>\n"
    return tree

def compile_subroutine_body(lexer): 
    tree="<subroutineBody>\n"
    tree+=compile_expected_token(lexer,Token_Type.LEFT_CURLY)
    while True:
        lexer.peek_ahead(1)
        if lexer.cur_token.token_type == Token_Type.VAR:
            tree+=compile_var_dec(lexer)
        else:
            break
    tree+=compile_multiple_statements(lexer)
    tree+=compile_expected_token(lexer,Token_Type.RIGHT_CURLY) 
    tree+="</subroutineBody>\n"
    return tree

def compile_parameter_list(lexer): 
    tree="<parameterList>\n"
    lexer.peek_ahead(1)
    if lexer.cur_token.token_type != Token_Type.RIGHT_PAREN:
        tree+=compile_type(lexer)
        tree+=compile_identifier(lexer)
        lexer.peek_ahead(1)
        while lexer.cur_token.token_type == Token_Type.COMMA:
            tree+=compile_expected_token(lexer,Token_Type.COMMA) 
            tree+=compile_type(lexer)
            tree+=compile_identifier(lexer)
            lexer.peek_ahead(1) 
    tree+="</parameterList>\n"
    return tree

def compile_var_dec(lexer): 
    tree="<varDec>\n"
    tree+=compile_expected_token(lexer,Token_Type.VAR)
    tree+=compile_type(lexer)
    while True:
        tree+=compile_identifier(lexer)
        tree+=compile_next_token(lexer)
        if lexer.cur_token.token_type == Token_Type.COMMA:
            pass
        elif lexer.cur_token.token_type == Token_Type.SEMICOLON:
            break
        else:
            lexer.error_log+=f"syntax error: semicolon is expected to end variable declarations, not {lexer.cur_token.name}\n"
            lexer.error_log+=f"{lexer.cur_file}: line {lexer.cur_line}:{lexer.line_pos}\n"
    tree+="</varDec>\n"
    return tree

def compile_type(lexer): 
    tree = compile_next_token(lexer)
    if not(lexer.cur_token.token_type == Token_Type.INT or lexer.cur_token.token_type == Token_Type.CHAR or lexer.cur_token.token_type == Token_Type.BOOL or lexer.cur_token.token_type == Token_Type.IDENTIFIER):
        lexer.error_log+=f"invalid type on line {lexer.cur_line}:{lexer.line_pos}\n"
    return tree


def compile_multiple_statements(lexer):
    tree="<statements>\n"
    while True:
        lexer.peek_ahead(1)
        if lexer.cur_token.token_type == Token_Type.RIGHT_CURLY:
            break
        tree+=compile_statement(lexer)
    tree+="</statements>\n"
    return tree


def compile_statement(lexer):
    tree = None
    lexer.peek_ahead(1)
    if not(lexer.cur_token.token_type in statement_maps):
        tree = compile_next_token(lexer) #idk
        lexer.error_log+=f"syntax error: invalid statement, expecting do, let, if, while, or return keywords, not {lexer.cur_token.name}\n"
        lexer.error_log+=f"{lexer.cur_file}: line {lexer.cur_line}:{lexer.line_pos}\n"
        return tree

    tree = statement_maps[lexer.cur_token.token_type](lexer)
    return tree


def compile_expression(lexer):
    tree="<expression>\n"
    tree+=compile_term(lexer) 
    while True:
        lexer.peek_ahead(1)
        if lexer.cur_token.token_class == Token_Class.OPERATOR:
            tree+=compile_next_token(lexer) #check for proper operator
            tree+=compile_term(lexer)
        else:
            break
    tree+="</expression>\n"
    return tree

def compile_term(lexer):
    tree="<term>\n"
    lexer.peek_ahead(1)
    if lexer.cur_token.token_type == Token_Type.INT_CONSTANT:
       tree+=compile_next_token(lexer)
    elif lexer.cur_token.token_type == Token_Type.STRING_CONSTANT: 
       tree+=compile_next_token(lexer)
    elif lexer.cur_token.token_type == Token_Type.TRUE: 
        tree+=compile_next_token(lexer)
    elif lexer.cur_token.token_type == Token_Type.FALSE: 
        tree+=compile_next_token(lexer)
    elif lexer.cur_token.token_type == Token_Type.NULL: 
        tree+=compile_next_token(lexer)
    elif lexer.cur_token.token_type == Token_Type.THIS: 
        tree+=compile_next_token(lexer)
    elif lexer.cur_token.token_type == Token_Type.LEFT_PAREN:
        tree+=compile_expected_token(lexer,Token_Type.LEFT_PAREN)
        tree+=compile_expression(lexer)
        tree+=compile_expected_token(lexer,Token_Type.RIGHT_PAREN)
    elif lexer.cur_token.token_type == Token_Type.MINUS or lexer.cur_token.token_type == Token_Type.TILDE:
        tree+=compile_next_token(lexer) # maybe make a function for it?
        tree+=compile_term(lexer)
    elif lexer.cur_token.token_type == Token_Type.IDENTIFIER:
        lexer.peek_ahead(2)
        if lexer.cur_token.token_type == Token_Type.LEFT_BRACKET:
            tree+=compile_identifier(lexer)
            tree+=compile_expected_token(lexer,Token_Type.LEFT_BRACKET)
            tree+=compile_expression(lexer)
            tree+=compile_expected_token(lexer,Token_Type.RIGHT_BRACKET)
        elif lexer.cur_token.token_type == Token_Type.LEFT_PAREN or lexer.cur_token.token_type == Token_Type.DOT:
            tree+=compile_subroutine_call(lexer) 
        else:
            tree+=compile_identifier(lexer)
    else:
        lexer.error_log+=f"syntax error: invalid term for expression, identifier, constant or expression expected, not {lexer.cur_token.name}\n"
        lexer.error_log+=f"{lexer.cur_file}: line {lexer.cur_line}:{lexer.line_pos}\n"
        tree+=compile_next_token(lexer) 
    tree+="</term>\n"
    return tree

def compile_subroutine_call(lexer):
    tree=compile_identifier(lexer)
    tree+=compile_next_token(lexer)
    if lexer.cur_token.token_type == Token_Type.DOT:
        tree+=compile_identifier(lexer)
        tree+=compile_expected_token(lexer,Token_Type.LEFT_PAREN)
    elif lexer.cur_token.token_type != Token_Type.LEFT_PAREN:
        lexer.error_log+=f"syntax error: ( is expected for subroutine call not {lexer.cur_token.name}\n"
        lexer.error_log+=f"{lexer.cur_file}: line {lexer.cur_line}:{lexer.line_pos}\n"
    tree+=compile_expression_list(lexer)
    tree+=compile_expected_token(lexer,Token_Type.RIGHT_PAREN)
    return tree

def compile_expression_list(lexer):
    tree="<expressionList>\n"
    lexer.peek_ahead(1)
    while lexer.cur_token.token_type != Token_Type.RIGHT_PAREN:
        tree+=compile_expression(lexer)
        lexer.peek_ahead(1)
        if lexer.cur_token.token_type == Token_Type.COMMA:
            tree+=compile_next_token(lexer)
    tree+="</expressionList>\n"
    return tree

def compile_expected_token(lexer,tt):
    lexer.peek_ahead(1)
    if lexer.cur_token.token_type != tt:
        lexer.error_log+=f"syntax error:  expected {tt} not {lexer.cur_token.name}\n"
        lexer.error_log+=f"{lexer.cur_file}: line {lexer.cur_line}:{lexer.line_pos}\n"
    return compile_next_token(lexer)

def compile_identifier(lexer):
    tree = compile_next_token(lexer)
    if lexer.cur_token.token_type != Token_Type.IDENTIFIER:
        lexer.error_log+=f"syntax error: identifier is expected not {lexer.cur_token.name}\n"
        lexer.error_log+=f"{lexer.cur_file}: line {lexer.cur_line}:{lexer.line_pos}\n"
    return tree


def dump_xml_to_file(xml,file_name):
    try:
        with open(file_name,"w") as file:
            file.write(xml)
    except:
        print("could not open file for writing")
        exit()
