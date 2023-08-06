"Module for generating public/private SSH key pairs"
import os
import shutil
from Crypto.PublicKey import RSA


PRIVATE_KEY_NAME: str = "key"
PUBLIC_KEY_NAME: str = f"{PRIVATE_KEY_NAME}-cert.pub"
KEY_SIZE_BITS = 2048


def generate_private_public_key() -> tuple[bytes, bytes]:
    "Generates a private and public RSA key"
    key = RSA.generate(KEY_SIZE_BITS)
    private_key = key.export_key()
    public_key = key.public_key().export_key(format="OpenSSH")
    return private_key, public_key


def generate_private_public_key_in_file(
    public_key_dir: str,
    private_key_dir: str | None = None,
    public_key_name: str = PUBLIC_KEY_NAME,
    private_key_name: str = PRIVATE_KEY_NAME,
) -> tuple[bytes, bytes]:
    "Creates a private key and public key at the given paths"
    # If private key was not given a separate dir, use the same one as for public key
    if private_key_dir is None:
        private_key_dir = public_key_dir
    private_key, public_key = generate_private_public_key()
    user_path = os.path.expanduser("~")
    user_path_components = user_path.split("/")
    user = user_path_components[len(user_path_components) - 1]

    if not os.path.isdir(private_key_dir):
        os.makedirs(private_key_dir)
    if not os.path.isdir(public_key_dir):
        os.makedirs(public_key_dir)

    private_key_path = f"{private_key_dir}/{private_key_name}"
    public_key_path = f"{public_key_dir}/{public_key_name}"

    with open(private_key_path, "wb") as private_out:
        private_out.write(private_key)

    shutil.chown(private_key_path, user=user, group=-1)
    os.chmod(private_key_path, 0o600)

    with open(public_key_path, "wb") as public_out:
        public_out.write(public_key)
    return private_key, public_key
