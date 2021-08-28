import requests
from Enc import ENC_ECC, TOTP
from Skeleton import SkeletonECC
import config
import json

counter = 0
# Class init
ecc  = ENC_ECC(salt=config.SALT ,
          key=config.SECRET_KEY ,
          user_pincode=config.USER_PIN,
          otp_hw_code=config.OPT_HARDWARE_CODE)
otp = ecc.get_otp(counter=counter)

with open('./kinec_set1_4_1_0.json') as json_files:
    data = json.load(json_files)

skeleton_obj  = SkeletonECC(skeleton_data=data['data'])

bytes_convert = skeleton_obj.multi_skeleton(portion=0.1) # 1 frame
# bytes_convert = skeleton_obj.multi_skeleton(portion=0.25) # 1/4
# bytes_convert = skeleton_obj.multi_skeleton(portion=0.5) # 1/2
# bytes_convert = skeleton_obj.multi_skeleton(portion=1) # 1 action

enc_msg, iv = ecc.encrypt_message(bytes_convert)
hmac_key  = ecc.hmac_key_generation()
payload = ecc.message_transformer(
            enc_msg = enc_msg,
            iv=iv,
            hmac=hmac_key,
            otp=otp)

ret = requests.post("https://0.0.0.0:4211/listener", data=payload, verify=False)