import os
import time
import pyotp
from functools import wraps

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305, AESCCM
# from cryptography.hazmat.primitives.ciphers.aead import AESCCM

import logging

salt_save_location = "salt.bin"

class TimeRecord():
    def measure(func):
        @wraps(func)
        def _time_it(*args, **kwargs):
            start = time.time()
            try:
                return func(*args, **kwargs)
            finally:
                end_ = time.time()
                time_ = (end_ - start)*1000
                print("Total execution for {:30s} time: {} ms".format(func.__name__, time_))
                # logger.info("Total execution for {:30s} time: {} ms".format(func.__name__, time_))
        return _time_it
    
class TOTP():
    def __init__(self, init_key) -> None:
        '''
        Init the class
        Param: 
            init_key : secret key or hardware key to generate otp value
              init_key should be same between 2 device
        '''
        self.init_key = init_key
        self.otp = pyotp.HOTP(self.init_key)
    
    @TimeRecord.measure
    def get_otp(self, counter) -> bytes:
        '''
        Get the otp code at a counter
        '''
        otp_key = self.otp.at(int(counter)).encode()
        return otp_key

    @TimeRecord.measure
    def verify_otp(self, otp_key, counter) -> bool:
        otp_key = otp_key.decode("utf-8")
        return self.otp.verify(otp_key, counter)

class ENC_ECC(TOTP):
    def __init__(self, user_pincode, key, otp_hw_code, 
                      salt=None, mode=0, iv_length=16) -> None:
        self.key = key
        self.user_pincode=user_pincode
        self.password = bytes(self.user_pincode, 'ascii')

        self.mode = mode
        self.no_hmac = [2, 3, 5]
        self.otp_length = 6
        self.hmac_length = 16
        self.iv_length = iv_length

        if salt == None:
            self.salt = self.generate_salt()
        else:
            if isinstance(salt, bytes):
                self.salt = salt
            else:
                self.salt = self.read_salt(file_path=salt)
        super().__init__(otp_hw_code)
    
    @TimeRecord.measure
    def save_salt(self):
        try:
            file = open(salt_save_location, "wb")
            file.write(self.salt)
            file.close()
            return salt_save_location
        except Exception as e:
            return e

    @TimeRecord.measure
    def generate_salt(self):
        '''
        Params:
            file_path: full path to save the file (inlcude file name)
            Salt code --> Save and copy to server
        Return:
            Path of the salt file
        '''
        return os.urandom(16)
    
    @TimeRecord.measure
    def read_salt(self, file_path="salt.bin"):
        '''
        Params:
            file_path: full path to save the file (inlcude file name)
        Return:
            Salt data
        '''
        try:
            with open(salt_save_location, mode='rb') as file: # b is important -> binary
                fileContent = file.read()
            return fileContent
        except Exception as e:
            return e

    @TimeRecord.measure
    def hmac_key_generation(self) -> bytes:
        '''
        Use Case:
            HMAC Authentication, call after data encryption
              before sending the message
            Example: Cypertext + HMAC_Keys
              Cypertext = encrypted data
              HMAC_Keys = (return value of this function)
        Params:
            salt: Salt data for generating token code - binary
            user_pincode: User Password to generate token code - String
        Return:
            HMAC keys (binary)
        '''
        length = self.hmac_length
        if self.mode in self.no_hmac:
            # No need HMAC
            return os.urandom(length)
        # Code Generation
        password = bytes(self.user_pincode, 'ascii')
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=length,
            salt=self.salt,
            iterations=100000,)
        key = kdf.derive(password)
        return key

    @TimeRecord.measure
    def decrypt_message(self, payload) -> str:
        '''
        Params:
            payload: Message from outside -- encrypted
            token_code: TOTP code
        Return:
            Original data (json)
        '''

        otp, message_encrypted, iv, hmac = self.message_invert_transformer(payload)
        counter = 0
        # Veify otp
        verify = self.verify_otp(otp, counter)
        if not verify:
            raise Exception("OTP verification failed")
        
        # Veify HMAC
        if self.mode not in self.no_hmac:
            if not self.verify_hmac(hmac_key=hmac):
                raise Exception("HMAC verification failed")
            
        # Message decrypt
        try:
            if self.mode == 0:
                print("Mode : {}".format("AES"))
                cipher_decryptor = Cipher(
                            algorithms.AES(self.key),
                            modes.CBC(iv)).decryptor()
                message = cipher_decryptor.update(
                            message_encrypted) + cipher_decryptor.finalize()
                return message
            elif self.mode == 1:
                print("Mode : {}".format("Camelia"))
                cipher_decryptor = Cipher(
                            algorithms.Camellia(self.key),
                            modes.CBC(iv)).decryptor()
                message = cipher_decryptor.update(
                            message_encrypted) + cipher_decryptor.finalize()
                return message
            elif self.mode == 2:
                print("Mode : {}".format("AES-GCM"))
                cipher_decryptor = Cipher(
                                algorithms.AES(self.key),
                                modes.GCM(iv, hmac),
                                ).decryptor()
                message = cipher_decryptor.update(
                        message_encrypted) + cipher_decryptor.finalize()
                return message
            elif self.mode == 3:
                print("Mode : {}".format("ChaCha20Poly1305"))
                cipher_decryptor = ChaCha20Poly1305(self.key)
                message = cipher_decryptor.decrypt(iv, message_encrypted, None)
                return message
            elif self.mode == 4:
                print("Mode : {}".format("ChaCha20"))
                cipher_decryptor = Cipher(
                    algorithms.ChaCha20(self.key, iv),
                    mode=None).decryptor()
                message = cipher_decryptor.update(message_encrypted)
                return message
            elif self.mode == 5:
                print("Mode : {}".format("AES-CCM"))
                cipher_decryptor = AESCCM(self.key)
                message = cipher_decryptor.decrypt(iv, message_encrypted, None)
                return message
            elif self.mode == 6:
                print("Mode : {}".format("TripleDES"))
                cipher_decryptor = Cipher(
                    algorithms.TripleDES(self.key),
                    modes.CBC(iv)).decryptor() # Decrypt
                enc_msg = cipher_decryptor.update(message_encrypted) + cipher_decryptor.finalize()
            return enc_msg
        except Exception as e:
            return Exception("Decrypt process failed")

    @TimeRecord.measure
    def verify_hmac(self, hmac_key):
        self.kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=self.hmac_length,
            salt=self.salt,
            iterations=100000,)
        if self.kdf.verify(self.password, hmac_key) == None:
            return True
        else:
            return False
    
    @TimeRecord.measure
    def encrypt_message(self, message) -> bytes:
        a,b = divmod(len(message), self.iv_length)
        
        # [Mode] which not required padding
        if self.mode not in self.no_hmac:
            if b != 0:
                message = message.rjust((a+1)*self.iv_length,"*")

        iv = os.urandom(self.iv_length) # Append before message
        bin_msg = message
        if not isinstance(message, bytes):
            bin_msg = message.encode('ascii')
        
        if   self.mode == 0:
            print("Mode : {}".format("AES-CBC"))
            cipher_enc = Cipher(
                algorithms.AES(self.key),
                modes.CBC(iv)).encryptor() # Encryption
            enc_msg = cipher_enc.update(bin_msg) + cipher_enc.finalize()
            return enc_msg, iv, self.hmac_key_generation()
        elif self.mode == 1:
            print("Mode : {}".format("Camelia"))
            cipher_enc = Cipher(
                algorithms.Camellia(self.key),
                modes.CBC(iv)).encryptor() # Encryption
            enc_msg = cipher_enc.update(bin_msg) + cipher_enc.finalize()
            return enc_msg, iv, self.hmac_key_generation()
        elif self.mode == 2:
            print("Mode : {}".format("AES-GCM"))
            cipher_enc = Cipher(
                algorithms.AES(self.key),
                modes.GCM(iv)).encryptor() # Encryption
            enc_msg = cipher_enc.update(bin_msg) + cipher_enc.finalize()
            return enc_msg, iv, cipher_enc.tag
        elif self.mode == 3:
            print("Mode : {}".format("ChaCha20Poly1305"))
            cipher_enc = ChaCha20Poly1305(self.key)# Encryption
            enc_msg = cipher_enc.encrypt(iv, bin_msg, None)
            return enc_msg, iv, self.hmac_key_generation()
        elif self.mode == 4:
            print("Mode : {}".format("ChaCha20"))
            cipher_enc = Cipher(
                algorithms.ChaCha20(self.key, iv),
                mode=None).encryptor() # Encryption
            enc_msg = cipher_enc.update(bin_msg)
            return enc_msg, iv, self.hmac_key_generation()
        elif self.mode == 5:
            print("Mode : {}".format("AES-CCM"))
            cipher_enc = AESCCM(self.key)
            enc_msg = cipher_enc.encrypt(iv, bin_msg, None)
            return enc_msg, iv, self.hmac_key_generation()
        elif self.mode == 6:
            print("Mode : {}".format("TripleDES"))
            cipher_enc = Cipher(
                algorithms.TripleDES(self.key),
                modes.CBC(iv)).encryptor() # Encryption
            enc_msg = cipher_enc.update(bin_msg) + cipher_enc.finalize()
            return enc_msg, iv, self.hmac_key_generation()

    @TimeRecord.measure
    def message_transformer(self, enc_msg, iv, hmac, otp):
        message_ = otp + iv + enc_msg + hmac
        return message_

    @TimeRecord.measure
    def message_invert_transformer(self, payload):
        otp = payload[0:self.otp_length]
        hmac = payload[-1*self.hmac_length:]
        iv = payload[self.otp_length:self.iv_length+self.otp_length]
        message_encrypted = payload[self.iv_length+self.otp_length:-1*self.hmac_length]
        return otp, message_encrypted, iv, hmac

if __name__ == "__main__":
    # Logger
    logger = logging.getLogger("Simple_server")
    logger.setLevel(logging.DEBUG)
    log_file_name = str(time.ctime().replace(" ", "_")) + "_LOG.log"
    fh = logging.FileHandler("LOG_FILE/" + log_file_name)
    fh.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    # Shared key 
    user_pincode     = "12345678" # 8 char --> User PIN
    key_message_encryptor = os.urandom(16) # Save on server and on client
    otp_hardware_code = pyotp.random_base32() # For init HOTP
    '''
    user_pincode, key_message_encryptor, and otp_hardware_code
     should be available in both device 
     In the future this two keys should be manage by "keys management"
    '''
    print("----- Client side ------")
    ## Client Side
    # Triple DES --> mode 6, iv 8, key 16
    counter = 0
    ecc  = ENC_ECC(salt="salt.bin",
          key=key_message_encryptor,
          user_pincode=user_pincode,
          otp_hw_code=otp_hardware_code,
          mode=2,
          iv_length=16)
    otp = ecc.get_otp(counter=counter)
    
    message     = "a secret message"
    enc_msg, iv, hmac_key = ecc.encrypt_message(message)
    payload     = ecc.message_transformer(
                    enc_msg = enc_msg,
                    iv=iv,
                    hmac=hmac_key,
                    otp=otp)
    
    # print("----- Server side ------")
    # # Server side
    # payload = payload
    # ecc  = ENC_ECC(salt="salt.bin",
    #       key=key_message_encryptor,
    #       user_pincode=user_pincode,
    #       otp_hw_code=otp_hardware_code,
    #       mode=6, iv_length=8)

    # decrypt_msg = ecc.decrypt_message(
    #               payload=payload)
    # print(decrypt_msg)

