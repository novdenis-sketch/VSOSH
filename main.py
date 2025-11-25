import random

OPERATIONS = [
    ('+', '-'),
    ('-', '+'),
    ('*', '//'),
    ('//', '*'),
    ('^', '^')
]
xor_function = ['char* decrypt_string(char* data, int key) {\n',
     'for (int i = 0; data[i]; i++) {\n',
    'data[i] = data[i] ^ key;\n',
     '}\n',
     'return data;\n',
'}\n']


def obfuscate_numbers(lines):
    global new_lines
    for line in lines:
        x = ''
        new_line = ""
        i = 0
        while i < len(line):
            if line[i] == '#':
                new_line += line[i:]
                break
            if i < len(line) - 1 and line[i:i + 2] == "0x":
                new_line += "0x"
                i += 2
                while i < len(line) and line[i] in "0123456789abcdefABCDEF":
                    new_line += line[i]
                    i += 1
                continue
            if line[i] == '"':
                new_line += line[i]
                i += 1
                while i < len(line) and line[i] != '"':
                    new_line += line[i]
                    i += 1
                if i < len(line):
                    new_line += line[i]
                    i += 1
                continue
            if line[i] == "'":
                new_line += line[i]
                i += 1
                while i < len(line) and line[i] != "'":
                    new_line += line[i]
                    i += 1
                if i < len(line):
                    new_line += line[i]
                    i += 1
                continue
            if line[i] == '.':
                new_line += line[i]
                i += 1
                continue
            if line[i] in "0123456789":
                start = i
                while i < len(line) and line[i] in "0123456789":
                    i += 1
                number_str = line[start:i]
                is_part_of_variable = False
                if start > 0:
                    prev_char = line[start - 1]
                    if prev_char.isalpha() or prev_char == '_' or prev_char.isdigit():
                        is_part_of_variable = True
                if i < len(line):
                    next_char = line[i]
                    if next_char.isalpha() or next_char == '_' or next_char.isdigit():
                        is_part_of_variable = True
                if is_part_of_variable:
                    new_line += number_str
                    continue
                operation1, operation2 = random.choice(OPERATIONS)
                num = random.randint(1, 1000)
                ist = int(number_str)
                ets = eval(f"{ist} {operation1} {num}")
                if operation2 == "//":
                    operation2 = "/"
                new_line += f"({ets} {operation2} {num})"
            else:
                new_line += line[i]
                i += 1
        new_lines.append(new_line)

def encrypt_string(s, key):
    encrypted_bytes = []
    xxs=-1
    for i in range(len(s)):
        char = s[i]
        if i!=len(s)-1 and ord(s[i])==92 and ord(s[i+1])==110:
            xxs = i+1
            encrypted_bytes.append(str(10 ^ key))
        if i!=xxs and i!=xxs-1:
            encrypted_bytes.append(str(ord(char) ^ key))
    encrypted_bytes.append('0')
    return encrypted_bytes
def obfuscate_string(lines):
    global new_lines
    new_lines=xor_function+new_lines
    st=False
    start=0
    end=0
    x=0
    for line in lines:
        new_line=""
        for i in range(len(line)):
            if line[i] == '"' and st==False:
                st=True
                start = i+1
            elif line[i] == '"' and st==True:
                st=False
                end = i
                word = line[start:end]
                key = random.randint(1, 255)
                encrypted_word = encrypt_string(word, key)
                ew = ", ".join(encrypted_word)
                new_line += " decrypt_string((char[]){"+ew+"},"+str(key)+")"
            elif not(st):
                new_line += line[i]
        new_lines[x+len(xor_function)]=new_line
        x+=1


def add_anti_debug(code):
    anti_debug_code = [
        '#include <sys/ptrace.h>\n',
        '#include <stdlib.h>\n',
        '#include <time.h>\n',
        'void anti_debug_check() {\n',
        'if (ptrace(PTRACE_TRACEME, 0, 1, 0) == -1) {\n',
        'exit(1);\n',
        '}\n',
        'clock_t start = clock();\n',
        'for (volatile int i = 0; i < 10000; i++) {}\n',
        'clock_t end = clock();\n',
        'if (((double)(end - start)) / CLOCKS_PER_SEC > 0.01) {\n',
        'exit(1);\n',
        '}\n',
        '}\n',
    ]

    lines = code
    new_lines = anti_debug_code + lines

    for i, line in enumerate(new_lines):
        if 'int main(' in line and '{' in line:
            for j in range(i + 1, len(new_lines)):
                if new_lines[j]:
                    new_lines.insert(j, 'anti_debug_check();\n')
                    break
            break

    return ''.join(new_lines)

def add_more_garbage(lines):
    garbage_snippets = [
        'for (volatile int g_{} = 0; g_{} < {}; g_{}++) {{ volatile int tmp = g_{} * {}; }}',
        'if (0) {{ int unused_{} = {}; }}',
        'do {{ double fake_{} = {} / 3.14; }} while (0);',
        'volatile int dummy_{} = {};',
        'while (0) {{ char fake_str_{}[] = "junk"; }}',
        'switch(0) {{ case 0: break; default: break; }}',
        '{{ volatile int block_{} = {} * {}; }}'
    ]
    new_lines = []

    for line in lines:
        new_lines.append(line)
        if random.random() < 0.15 and line.strip() and not line.strip().startswith('#'):
            garbage = random.choice(garbage_snippets)
            garbage_id = random.randint(1000, 9999)
            garbage_num = random.randint(1, 100)
            garbage_line = garbage.format(garbage_id, garbage_id, garbage_num,
                                          garbage_id, garbage_id, garbage_num)
            new_lines.append(garbage_line+"\n")

    return new_lines

    return '\n'.join(new_lines)
file_name = input("Введите название файла:")
Filename_extension = file_name.split(".")
if Filename_extension[-1] == "c":
    try:
        file = open(file_name)
    except:
        print("Файл не найден")
        exit(0)
else:
    print("Не тот тип файла")
    exit(0)
new_lines = []
lines = file.readlines()
obfuscate_numbers(lines)
obfuscate_string(lines)

new_lines=add_more_garbage(new_lines)
new_lines =add_anti_debug(new_lines)
with open("obfuscate.c", 'w') as file:
    file.writelines(new_lines)

print("Файл успешно обработан!")
