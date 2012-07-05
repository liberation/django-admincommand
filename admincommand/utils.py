def generate_instance_name(name):
    out = name[0].lower()
    for char in name[1:]:
        if char.isupper():
            out += '_%s' % char.lower()
        else:
            out += char
    return out


def generate_human_name(name):
    out = name[0]
    for char in name[1:]:
        if char.isupper():
            out += ' %s' % char.lower()
        else:
            out += char
    return out
    
