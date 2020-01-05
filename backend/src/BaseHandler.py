import tornado.web
import tornado.websocket
import sys
import json

sys.path.extend("auth")
from enum import Enum, auto


class EndpointType(Enum):
    POST = auto()
    GET = auto()


from auth.user_validation import *


class BaseHandler(tornado.web.RequestHandler):
    """
    All endpoints will subclass this method. This contains the basic
    functionality needed for user authentication.
    """

    params = {}  # Override in base class for needed parameters
    endpoint_type = None  # Override for get or set method

    async def process(self, **kwargs):
        raise NotImplementedError("Must implement in subclass")

    async def process_endpoint(self):
        """
        Logic to handle all endpoint functionality. Get, post, put, etc endpoints
        will call into this function in order to map to respective function.
        This should also validate all parameters passed into endpoint to
        invalidate bad calls

        Currently supports "optional" and "type" fields
        """
        args = {}
        for param, options in self.params.items():
            try:
                argument = self.get_argument(param, "")
                if not argument and not options['required']:
                    continue
                if not argument:
                    raise SyntaxError(f"No argument passed for {param}")
                type_checked_param = options[type](argument)
                args[param] = type_checked_param
            except Exception as e:
                raise SyntaxError(
                    f"Invalid argument to {param} provided: ", str(e)
                )

        endpoint_result = await self.process(**args)
        return endpoint_result

    async def get(self):
        try:
            endpoint_result = await self.process_endpoint()
            self.write(json.dumps(endpoint_result))
        except Exception as e:
            print(e)
            self.write(json.dumps({"success": 0, "error": str(e)}))

    async def post(self):
        try:
            endpoint_result = await self.process_endpoint()
            self.write(json.dumps(endpoint_result))
        except Exception as e:
            print(e)
            self.write(json.dumps({"success": 0, "error": str(e)}))

    async def set_user(self, uid: Uid):
        user_token = await generate_session_id()
        set_user_token(uid, user_token)
        self.set_secure_cookie("SESSION_ID", user_token, httponly=True)

    async def get_user(self):
        session_id = self.get_secure_cookie("SESSION_ID")
        if not session_id:
            return None
        session_id = session_id.decode("utf-8")
        user = await get_user_from_session_id(session_id)
        return user

    async def end_session(self) -> bool:
        """Returns whether the session was successfully completed"""
        session_id = self.get_secure_cookie("SESSION_ID")
        if not session_id:
            print("INVALID SESSION_ID")
            return False
        session_id = session_id.decode("utf-8")
        user = await get_user_from_session_id(session_id)
        if user:
            clear_session_cookie(user.uid)
        self.clear_cookie("SESSION_ID")
        return True
