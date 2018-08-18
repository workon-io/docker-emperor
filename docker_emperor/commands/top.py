import os


def run(root, *args, **kwargs):

    cmd = root.bash(
        root.project.compose.bin,
        'top',
        *args,
        compose=root.compose,
        is_system=True
    )