OPT_HARDWARE_CODE= open("shared_key/otp_hardware_code.txt", "r").readline()
SECRET_KEY= open('shared_key/key_message_encryptor.bin', "rb").readline()
SALT= open('shared_key/salt.bin', "rb").readline()
USER_PIN = "12345678"