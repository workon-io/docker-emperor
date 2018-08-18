import os


def run(root, *args, **kwargs):

    cmd = root.bash(
        root.project.compose.bin,
        'ps',
        *args,
        compose=root.compose,
        is_system=True
    )