# pylint: disable=too-many-arguments

import logging
from typing import Union, Callable, Any

import paramiko
from sshtunnel import SSHTunnelForwarder, BaseSSHTunnelForwarderError

from . import InterfaceNetworkConnector

logging.basicConfig(
    level=logging.INFO,
    filename="./logging/logger.log",
    filemode="w",
    format="%(asctime)s %(levelname)s [%(name)s:%(lineno)d] %(message)s",
)
logger = logging.getLogger(__name__)


class SSHConnector(InterfaceNetworkConnector):
    def __init__(
        self,
        remote_ssh_ip_address: str,
        remote_ssh_port: int,
        remote_ssh_username: str,
        remote_bind_host: str,
        remote_bind_port: int,
        pkey_path: Union[str, None] = None,
        password: Union[str, int, None] = None,
        verbose: bool = True,
    ) -> None:
        """
        SSH tunnel for remote network connection.

        :param remote_ssh_ip_address: (str) IP address of the ssh connection (ex. 1.1.1.1.1).
        :param remote_ssh_port: (int) SSH port to use.
        :param remote_ssh_username: (str) Remote machine username (ex. username).
        :param remote_bind_host: (str) Remote server hostname (ex. localhost).
        :param remote_bind_port: (int) Remote port opened on the machine.
        :param pkey_path: (Union[str, None]) Path of the local pkey to use to connect to the remote host
            (i.e. usually format ``".pem"``). By default, set to None for no pkey use.
        :param password: (str, int, None) Connection password. By default, set to None for no password use.
        :param verbose: (bool) Print to console or not.
        """
        super().__init__(remote_ssh_ip_address, remote_ssh_port, remote_ssh_username, verbose)

        if pkey_path is not None:
            self.key = paramiko.RSAKey.from_private_key_file(pkey_path)

        self.password = password
        self.remote_bind_host = remote_bind_host
        self.remote_bind_port = remote_bind_port

        self.ssh_local_bind_port = self._start_connector()

    def _start_connector(self) -> int:
        """
        Start a connection through an SSH tunnel.

        :return: Local binded port (assigned at run time) used on the local user machine (i.e. "localhost:LOCAL_PORT").
        """
        try:
            ssh = self.__get_ssh()
            ssh.start()

            logger.info("Success - SSH connected")
        except BaseSSHTunnelForwarderError as error:
            message = f"Connexion problem with the SSH connexion: {error}."
            logger.critical(message)
            raise error

        return ssh.local_bind_port

    def _run_with(self, function: Callable, *args, **kwargs) -> Any:
        """
        Look-a-like decorator to run code with an SSH tunnel. Allow decoupling of the SSH tunnel with a class
        (i.e. run ssh tunnel outside a class).

        :param function: (Callable) Function to be run through the SSH tunnel.
        :param args: Function parameters.
        :param kwargs: Function named parameters.

        :return: Result of the function if any.
        """
        try:
            ssh = self.__get_ssh()
            with ssh:
                result = function(*args, **kwargs)

            logger.info("Success - SSH connected")
        except BaseSSHTunnelForwarderError as error:
            message = f"Connexion problem with the SSH connexion: {error}."
            logger.critical(message)
            raise error

        if self.verbose:
            message = f"Success - Function {function} called with SSH protocol."
            print(message)
            logger.info(message)

        return result

    def __get_ssh(self) -> SSHTunnelForwarder:
        """
        :return: SSH Tunnel instance used for the connection.
        """
        return SSHTunnelForwarder(
            (self.remote_ssh_host, self.remote_ssh_port),
            ssh_username=self.remote_username,
            ssh_pkey=self.key,
            ssh_password=self.password,
            remote_bind_address=(self.remote_bind_host, self.remote_bind_port),
        )
