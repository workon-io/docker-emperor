import os


def run(root, *args, **kwargs):

    cmd = root.bash(
        root.project.compose.bin,
        'ps',
        *args,
        mounting=root.mounting,
        is_system=True
    )