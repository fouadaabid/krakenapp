from core.config import settings
from sshtunnel import SSHTunnelForwarder
import pymongo
import sshtunnel
from typing import Dict, Any


class MongoDB():

    def __init__(self):
        self.ssh_tunnel_host = settings.PUBLIC_ADDRESS
        self.ssh_tunnel_port = settings.SSH_TUNNEL_PORT
        self.ssh_tunnel_user = settings.USER
        self.ssh_tunnel_pkey = f'./{settings.KEY_FOLDER}/{settings.KEY_FILE}'
        self.localhost = settings.LOCALHOST
        self.db_host = settings.PRIVATE_ADDRESS
        self.db_port = settings.DB_PORT
        self.server = self.ssh_server()
        self.user: Dict[str, Any] = dict()

    def ssh_server(self) -> sshtunnel.SSHTunnelForwarder:
        """_summary_

        Returns:
            sshtunnel.SSHTunnelForwarder: _description_
        """
        return SSHTunnelForwarder(
            (self.ssh_tunnel_host, self.ssh_tunnel_port),
            ssh_username=self.ssh_tunnel_user,
            ssh_pkey=self.ssh_tunnel_pkey,
            remote_bind_address=(self.db_host, self.db_port),
            local_bind_address=(self.localhost, self.db_port)
        )

    def db_find_user(
        self,
        db_name: str,
        db_col: str,
        db_admin: str,
        db_pass: str,
        username: str,
    ) -> None:
        """_summary_

        Args:
            db_name (str): _description_
            db_col (str): _description_
            db_admin (str): _description_
            db_pass (str): _description_

        Returns:
            _type_: _description_
        """
        with self.server as s:
            s.start()

            db_uri = f'mongodb://{db_admin}:{db_pass}@{self.localhost}:{self.db_port}'
            client = pymongo.MongoClient(db_uri, serverSelectionTimeoutMS=3000)

            db = client[db_name]        
            # mydict = { "userid": 2, "username": "Susana", "password": "password456" }
            # x = db[db_col].insert_one(mydict)
            mydoc = db[db_col].find({'username': username})

            for i, doc in enumerate(mydoc):
                if i>0:
                    raise ValueError(f"Duplicated User '{doc['username']}' in the DataBase Collection")
                self.user = doc
            
        return None
            