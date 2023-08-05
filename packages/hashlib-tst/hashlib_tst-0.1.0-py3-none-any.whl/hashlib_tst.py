from hashlib import md5, sha256

class MD5:
    def __init__(self, data = "Hello, world!"):
        self.data = data
    def encrypt(self):
        self.data = md5(self.data.encode()).hexdigest()
        return "MD5 Crypted: "+self.data
    def decrypt(self, data):
        if md5(data.encode()).hexdigest() == self.data:
            return "MD5 Decrypted: "+data
            del self.data
        else:
            return "Error"

class SHA256:
    def __init__(self, data = "this is confidential message!"):
        self.data = data
    def encrypt(self):
        self.data = sha256(self.data.encode()).hexdigest()
        return "SHA256 Crypted: "+self.data
    def decrypt(self, data):
        if sha256(data.encode()).hexdigest() == self.data:
            return "SHA256 Decrypted: "+data
            del self.data
        else:
            return "Error"

if __name__ == "__main__":
    crypt = MD5()
    print(crypt.encrypt()) # Encrypt
    print(crypt.decrypt("Hello, world!")) # Decrypt data argument

    crypt = SHA256()
    print(crypt.encrypt()) # Encrypt
    print(crypt.decrypt("this is confidential message!")) # Decrypt data argument
