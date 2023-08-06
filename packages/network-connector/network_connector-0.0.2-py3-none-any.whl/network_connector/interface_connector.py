# pylint: disable=unused-argument

from abc import ABC, abstractmethod


class InterfaceNetworkConnector(ABC):
    def __init__(
        self,
        remote_ssh_ip_address: str,
        remote_ssh_port: int,
        remote_username: str,
        *args,
        verbose: bool = True,
        **kwargs
    ) -> None:
        """
        Abstract interface for remote network connection.

        :param remote_ssh_ip_address: (str) IP address of the ssh connection (ex. 1.1.1.1.1).
        :param remote_ssh_port: (int) SSH port to use.
        :param remote_username: (str) Remote machine username (ex. username).
        :param args: Supplemental child class arguments.
        :param args: verbose: bool = True,
        :param kwargs: Supplemental child class named arguments
        """
        self.remote_ssh_host = remote_ssh_ip_address
        self.remote_username = remote_username
        self.remote_ssh_port = remote_ssh_port
        self.verbose = verbose

        self.ssh_local_bind_port = None

    @abstractmethod
    def _start_connector(self) -> None:
        pass
