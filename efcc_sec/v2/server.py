from flask import Flask
from flask import request
import time
import logging
from Enc import ENC_ECC, TOTP
from Skeleton import SkeletonECC, invert_transform
import config

app = Flask(__name__)

# Logger
logger = logging.getLogger("Simple_server")
logger.setLevel(logging.DEBUG)
log_file_name = str(time.ctime().replace(" ", "_")) + "_LOG.log"
fh = logging.FileHandler("LOG_FILE/" + log_file_name)
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
fh.setFormatter(formatter)
logger.addHandler(fh)

# Class init
ecc = ENC_ECC(
    salt=config.SALT,
    key=config.SECRET_KEY,
    user_pincode=config.USER_PIN,
    otp_hw_code=config.OPT_HARDWARE_CODE,
)


@app.route("/listener", methods=["POST"])
def listener():
    start_time = time.time()
    _payload = request.get_data()
    decrypt_msg = ecc.decrypt_message(payload=_payload)
    data = invert_transform(decrypt_msg)
    # print(data)
    end_data = time.time()
    logger.info("Download data {} Second (+Decrypt)".format(end_data - start_time))
    return "Success"


@app.route("/listener_wot", methods=["POST"])
def listener_without_time():
    start_time = time.time()
    data = request.get_data()
    logger.info("Example data".format(data[0:10]))
    end_data = time.time()
    logger.info("Download data {} Second (+Decrypt)".format(end_data - start_time))
    return "Success"


@app.route("/")
def hello_world():
    return "Hello World"


if __name__ == "__main__":
    app.run(
        port=4210, host="0.0.0.0", ssl_context="adhoc"
    )  # ssl_context="adhoc" for securing the data transmision
