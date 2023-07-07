import Pyro5.server
import Pyro5.socketutil

Pyro5.config.SERVERTYPE = "thread"

# adapters
from adapters.users.user_login_login_adapter import UserLoginAdapter

adress = Pyro5.socketutil.get_ip_address(None,workaround127=True)

Pyro5.server.serve({
        UserLoginAdapter:"adapters.user_login_login_adapter"
    },use_ns=True)

'''
import Pyro5.server
import Pyro5.socketutil

Pyro5.config.SERVERTYPE = "thread"

# adapters
from adapters.users.user_login_login_adapter import UserLoginAdapter

class  RMIServer:
    def __init__(self):
        Pyro5.config.SERVERTYPE = "thread"

        self.adapters = {
            UserLoginAdapter: "adapters.user_login_login_adapter"
        }

    def serve(self):
        Pyro5.server.serve(self.adapters, use_ns=True)
'''