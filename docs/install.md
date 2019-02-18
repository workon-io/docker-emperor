You can run Docker Emperor on macOS, Windows, and 64-bit Linux.

## Prerequisites

Docker Emperor relies on Docker Engine and Docker Compose for any meaningful work, so make sure you
have Docker Engine and Docker Compose installed either locally or remote, depending on your setup.

- On Linux systems, first install the
[Docker](https://docs.docker.com/install/index.md#server)
- Then install
[Docker Compose](https://docs.docker.com/compose/install/)
- To run Compose as a non-root user, see [Manage Docker as a non-root user](/install/linux/linux-postinstall.md).
- Then recommended install
[Docker Machine](https://docs.docker.com/machine/install-machine/)


## Install Docker Emperor

~~Follow the instructions below to install Compose on Mac, Windows, Windows Server
2016, or Linux systems, or find out about alternatives like using the `pip`
Python package manager or installing Docker Emperor as a container.~~  (not yet available)

### Alternative install options
-   [Install using pip](/docker/docker-emperor/install/#install-using-pip)
-   [Install as a container](/docker/docker-emperor/install/#install-as-a-container) (not yet available)

#### INSTALL USING PIP

Docker Emperor can be installed from  [pypi](https://pypi.python.org/pypi/docker-emperor)  using  `pip`. If you install using  `pip`, we recommend that you use a  [virtualenv](https://virtualenv.pypa.io/en/latest/)  because many operating systems have python system packages that conflict with docker-emperor dependencies. See the  [virtualenv tutorial](http://docs.python-guide.org/en/latest/dev/virtualenvs/)  to get started.

```
pip install docker-emperor
```

#### ~~INSTALL AS A CONTAINER~~  (not yet available)
