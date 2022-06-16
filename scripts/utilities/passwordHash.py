from os import environ
from cryptography.fernet import Fernet
import uuid

class PasswordHash:

    cipherSuite = Fernet(environ.get('SECRET_KEY').encode('utf-8'))

    @staticmethod
    def encrypt(rawPassword):
        return PasswordHash.cipherSuite.encrypt(rawPassword.encode('utf-8')).decode('utf-8')

    @staticmethod
    def decrypt(cipheredPassword):
        return bytes(PasswordHash.cipherSuite.decrypt(cipheredPassword.encode('utf-8'))).decode('utf-8')

    @staticmethod
    def generateRandomPassword(charCount=6):
        randomPassword = str(uuid.uuid4()) # Convert UUID format to a Python string.
        randomPassword = randomPassword.replace('-', '') # Remove the hyphens (-) on the generated UUID.
        return randomPassword[0:charCount] # Return the first 6 characters of the random string.
