import os
import sys
import sysconfig


def register_package(path, pth_name=None):
    if pth_name is None:
        pth_name = os.path.split(path)[1] + ".pth"

    user_site_path = sysconfig.get_paths()['purelib']
    if not os.path.exists(user_site_path):
        os.makedirs(user_site_path)

    pth_file = os.path.join(user_site_path, pth_name)

    with open(pth_file, "w") as pth:
        pth.write(path)


if __name__ == "__main__":
    pth_name = "framework.pth"
    register_package(os.path.split(os.path.abspath(sys.argv[0]))[0], pth_name)
    install_cmd = "pip install -r {}"
    if os.getenv("ARTIFACTORY_INDEX_URL") is not None:
        url = os.getenv("ARTIFACTORY_INDEX_URL")
        install_cmd += f" --index-url={url}"

    os.system(install_cmd.format(
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "requirements.txt")
    ))
