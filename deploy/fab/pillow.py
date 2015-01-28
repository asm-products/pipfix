from cuisine import package_ensure, mode_sudo

def pillow_ensure():
    with mode_sudo():
        package_ensure('libjpeg62 libjpeg62-dev zlib1g-dev')

