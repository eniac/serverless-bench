import json
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os

# Key and IV should ideally be securely generated and stored.
# For the example, we'll use static values for demo purposes.
key = bytes.fromhex(
    "00112233445566778899aabbccddeeff00112233445566778899aabbccddeeff"
)  # 32 bytes key
iv = bytes.fromhex("00112233445566778899aabbccddeeff")  # 16 bytes IV


def encrypt(data):
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted_data = encryptor.update(data.encode()) + encryptor.finalize()
    return encrypted_data


def decrypt(encrypted_data):
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()
    return decrypted_data.decode("utf-8", errors="replace")


def handler(event, context):
    try:
        if event["action"] == "encrypt":
            plaintext = event["message"]
            encrypted_message = encrypt(plaintext)
            return {
                "statusCode": 200,
                "body": json.dumps({"encrypted": encrypted_message.hex()}),
            }

        elif event["action"] == "decrypt":
            encrypted_message = bytes.fromhex(event["message"])
            decrypted_message = decrypt(encrypted_message)
            return {
                "statusCode": 200,
                "body": json.dumps({"decrypted": decrypted_message}),
            }
        else:
            return {
                "statusCode": 400,
                "body": 'Invalid action. Use "encrypt" or "decrypt".',
            }
    except Exception as e:
        return {"statusCode": 500, "body": f"Error: {str(e)}"}
