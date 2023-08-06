# 棋盘密码 Pro
import random


class PolybiusSquire:
    key = [
        ['A', 'B', 'C', 'D', 'E', '0', '1', '2', '3', '4'],
        ['F', 'G', 'H', 'I', 'K', '5', '6', '7', '8', '9'],
        ['L', 'M', 'N', 'O', 'P', '*', '/', '+', '-', '='],
        ['Q', 'R', 'S', 'T', 'U', '!', '@', '#', '$', '%'],
        ['V', 'W', 'X', 'Y', 'Z', '^', '&', '_', '[', ']'],
        ['a', 'b', 'c', 'd', 'e', '.', ',', ':', ';', '`'],
        ['f', 'g', 'h', 'i', 'k', '~', '|', '<', '>', ' '],
        ['l', 'm', 'n', 'o', 'p', '(', ')', '{', '}', '\\'],
        ['q', 'r', 's', 't', 'u', 'J', 'j', '\'', '\"', '《'],
        ['v', 'w', 'x', 'y', 'z', '⌈', '⌋', '⌊', '⌉', '》']
    ]

    @classmethod
    def encode(cls, message):
        key = cls.key
        code_list = []

        for char in message:
            i, j = 0, 0
            while i < len(key) and char not in key[i]:
                i += 1
            if i < len(key):
                j = key[i].index(char)
                code_list.append(str(i) + str(j))
            else:
                # print('Incorrect input!')
                return False

        ciphertext = ''.join(code_list)
        return ciphertext

    @classmethod
    def decode(cls, ciphertext):
        key = cls.key
        original_list = []

        try:
            splited = [ciphertext[i:i + 2] for i in range(0, len(ciphertext), 2)]
        except:
            # print('Incorrect input!')
            return False

        for i in splited:
            i = int(i)
            original_list.append(key[i // 10][i % 10])

        plaintext = ''.join(original_list)
        return plaintext


class Double:
    @classmethod
    def encode(cls, num):
        result = ''
        for i in num:
            result += i + f'{random.randint(0,5)}'
        return result

    @classmethod
    def decode(cls, num):
        result = ''
        try:
            splited = [num[i:i + 2] for i in range(0, len(num), 2)]
        except:
            # print('Incorrect input!')
            return False

        for i in splited:
            result += i[:1]
        return result


class Plugin:
    @classmethod
    def encode(cls, num):
        s = 0
        for i in num:
            s += int(i)
        # print(s)
        if len(str(s)) % 2 == 0:
            result = f'{random.randint(0,9)}' + num + str(s) + '1'
        else:
            result = f'{random.randint(0,9)}' + num + str(s) + f'{random.randint(0,9)}0'
        return result

    @classmethod
    def decode(cls, num):
        check = num[-1:]
        num = num[1:-1]
        if check == '1':
            result = cls.checking(num)
        else:
            num = num[:-1]
            result = cls.checking(num)
        return result

    @staticmethod
    def checking(string):
        for i in range(1, 6):
            s = 0
            fh = string[:-i]
            sh = string[-i:]
            for k in fh:
                s += int(k)
            if s == int(sh):
                return fh


class Core:
    error = '❌The format or content of the input is incorrect!'

    @classmethod
    def encode(cls, string):
        poe = PolybiusSquire.encode(string)
        if not poe:
            print(cls.error)
        else:
            doe = Double.encode(poe)
            ple = Plugin.encode(doe)
            pod = PolybiusSquire.decode(ple)
            return pod

    @classmethod
    def decode(cls, string):
        try:
            poe = PolybiusSquire.encode(string)
            pld = Plugin.decode(poe)
            dod = Double.decode(pld)
            pod = PolybiusSquire.decode(dod)
            return pod
        except:
            print(cls.error)
