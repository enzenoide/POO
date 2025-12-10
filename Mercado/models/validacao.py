import re 

def validar_telefone(numero):
    regex = r'^\(?\d{2}\)?[\s\.\-]?\d{4,5}[\s\.\-]?\d{4}$'
    return bool(re.match(regex,numero))
def validar_email(email):
    regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(regex,email))