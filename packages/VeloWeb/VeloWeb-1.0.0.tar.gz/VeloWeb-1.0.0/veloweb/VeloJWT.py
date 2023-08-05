import os
import platform
import datetime
import jwt
import uuid
import json
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import serialization 

class TokenExpiredError(Exception):
    pass

class InvalidTokenError(Exception):
    pass

class VeloJwtExtended:
    def __init__(self, private_key=None, public_key=None, encryption_key=None):
        self.private_key = private_key
        self.public_key = public_key
        self.encryption_key = encryption_key
        self.algorithm = 'RS256'
        self.blacklist_file = self.get_blacklist_file()

    def get_system_directory(self):
        system = platform.system()
        if system == 'Windows':
            return os.path.join(os.environ['APPDATA'], 'GoRouteJWT')
        elif system == 'Linux':
            return os.path.join(os.path.expanduser('~'), '.GoRouteJWT')
        elif system == 'Darwin':
            return os.path.join(os.path.expanduser('~'), 'Library', 'Application Support', 'GoRouteJWT')
        else:
            raise Exception('Unsupported platform')

    def generate_key_pair(self):
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        public_key = private_key.public_key()
        private_key_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        public_key_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        return private_key_pem, public_key_pem

    def get_or_generate_keys(self):
        system_directory = self.get_system_directory()
        private_key_file = os.path.join(system_directory, 'private_key.pem')
        public_key_file = os.path.join(system_directory, 'public_key.pem')
        if os.path.exists(private_key_file) and os.path.exists(public_key_file):
            with open(private_key_file, 'rb') as f:
                private_key = serialization.load_pem_private_key(
                    f.read(),
                    password=None,
                    backend=default_backend()
                )
                private_key_pem = private_key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.PKCS8,
                    encryption_algorithm=serialization.NoEncryption()
                )
            with open(public_key_file, 'rb') as f:
                public_key_pem = f.read()
            return private_key_pem, public_key_pem
        else:
            private_key_pem, public_key_pem = self.generate_key_pair()
            os.makedirs(system_directory, exist_ok=True)
            with open(private_key_file, 'wb') as f:
                f.write(private_key_pem)
            with open(public_key_file, 'wb') as f:
                f.write(public_key_pem)
            return private_key_pem, public_key_pem

    def get_blacklist_file(self):
        system_directory = self.get_system_directory()
        blacklist_file = os.path.join(system_directory, 'token_blacklist.json')
        return blacklist_file

    def create_access_token(self, payload, expires_delta=None):
        if not self.private_key or not self.public_key or not self.encryption_key:
            self.private_key, self.public_key = self.get_or_generate_keys()
            self.encryption_key = Fernet.generate_key()

        if expires_delta:
            expires = datetime.datetime.utcnow() + expires_delta
        else:
            expires = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)

        payload['exp'] = expires
        access_token = jwt.encode(payload, self.private_key, algorithm=self.algorithm).decode('utf-8')
        encrypted_access_token = self.encrypt_token(access_token)
        return encrypted_access_token

    def decode_access_token(self, encrypted_access_token):
        if not self.public_key or not self.encryption_key:
            raise Exception('Public key and encryption key are required for token decoding')

        access_token = self.decrypt_token(encrypted_access_token)
        try:
            payload = jwt.decode(access_token, self.public_key, algorithms=[self.algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            raise TokenExpiredError('Token has expired')
        except jwt.InvalidTokenError:
            raise InvalidTokenError('Invalid token')

    def create_refresh_token(self, payload):
        refresh_token = jwt.encode(payload, self.private_key, algorithm=self.algorithm).decode('utf-8')
        encrypted_refresh_token = self.encrypt_token(refresh_token)
        return encrypted_refresh_token

    def decode_refresh_token(self, encrypted_refresh_token):
        refresh_token = self.decrypt_token(encrypted_refresh_token)
        try:
            payload = jwt.decode(refresh_token, self.public_key, algorithms=[self.algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            raise TokenExpiredError('Refresh token has expired')
        except jwt.InvalidTokenError:
            raise InvalidTokenError('Invalid refresh token')

    def revoke_refresh_token(self, encrypted_refresh_token):
        refresh_token = self.decrypt_token(encrypted_refresh_token)
        try:
            payload = jwt.decode(refresh_token, self.public_key, algorithms=[self.algorithm])
            if 'token_id' not in payload:
                raise InvalidTokenError('Invalid refresh token')

            token_id = payload['token_id']
            self.blacklist_token(token_id)
            return True
        except jwt.InvalidTokenError:
            return False

    def revoke_all_refresh_tokens(self, user_id):
        tokens_to_revoke = []
        with open(self.blacklist_file, 'r') as f:
            blacklist = json.load(f)
            for token_id, token_data in blacklist.items():
                if token_id.startswith(user_id):
                    tokens_to_revoke.append(token_id)

        with open(self.blacklist_file, 'w') as f:
            blacklist = json.load(f)
            for token_id in tokens_to_revoke:
                del blacklist[token_id]
            json.dump(blacklist, f)

    def generate_token_id(self):
        return str(uuid.uuid4())

    def encrypt_token(self, token):
        f = Fernet(self.encryption_key)
        encrypted_token = f.encrypt(token.encode('utf-8'))
        return encrypted_token

    def decrypt_token(self, encrypted_token):
        f = Fernet(self.encryption_key)
        decrypted_token = f.decrypt(encrypted_token.encode('utf-8'))
        return decrypted_token.decode('utf-8')

    def blacklist_token(self, token_id):
        with open(self.blacklist_file, 'r') as f:
            blacklist = json.load(f)
        blacklist[token_id] = datetime.datetime.utcnow().isoformat()
        with open(self.blacklist_file, 'w') as f:
            json.dump(blacklist, f)

    def is_token_blacklisted(self, token_id):
        with open(self.blacklist_file, 'r') as f:
            blacklist = json.load(f)
        return token_id in blacklist