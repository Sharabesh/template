from BaseHandler import BaseHandler, EndpointType
import sys
sys.path.extend("../database")
import json
from database.image_uploader import upload_file
from auth.user_validation import set_user_image, register_user, validate_user

class LogoutHandler(BaseHandler):

    endpoint_type = EndpointType.GET

    params = {}

    async def process(self):
        if await self.end_session():
            return {"success": 1}

        return {"success": 0}


class ImageUploadHandler(BaseHandler):

    endpoint_type = EndpointType.POST

    params = {}

    async def process(self):
        user_profile_image = self.request.files["profile_image"][0]["body"]
        with open("data/tmp.jpeg", "wb+") as file:
            file.write(user_profile_image)
        # Upload to the hosting server retrieving the response and saving this to DB
        secure_url = await upload_file()
        # # Save relevant data to DB
        current_user = await self.get_user()
        if not current_user:
            return
        await set_user_image(current_user.uid, secure_url)
        return {"success": 1}


class LoginHandler(BaseHandler):

    endpoint_type = EndpointType.GET

    params = {
        "email": {
            "type": str,
            "required": True
        },
        "password": {
            "type": str,
            "required": True
        }
    }


    async def process(self, email, password):
        """
        Login should complete the following operations
        1. Evaluate whether the user exists in the database
        2. If Pass:
            3. Create cryptographic key and add to sessions_db
            4. set_secure_cookie(cryptographic_key)
            4. Redirect user to main page
        5. Else:
            6. Render Error Message on login page ("Invalid Credentials")
        """
        uid = await validate_user(email, password)
        if uid:
            # Log User in
            await self.set_user(uid)
            return {"success": 1}
        else:
            return {"success": 0}


class UserInfoHandler(BaseHandler):

    endpoint_type = EndpointType.GET

    # No parameters passed in request
    params = {}


    async def process(self):
        user = await self.get_user()
        if user:
            return  {
                        "success": 1,
                        "username": user.username,
                        "email": user.email_address,
                        "profile_image": user.profile_image,
                        "phone": user.phone,
                    }
        else:
            return {"success": 0}


class UserSignupHandler(BaseHandler):

    endpoint_type = EndpointType.GET

    params = {
        "email": {
            "type": str,
            "required": True
        },
        "username": {
            "type": str,
            "required": True
        },
        "password": {
            "type": str,
            "required": True
        },
        "phone": {
            "type": str,
            "required": True
        }
    }


    async def process(self, email, username, password, phone):
        success = await register_user(
            username=username, password=password, email=email, phone=phone
        )
        if success:
            return {"success": 1}
        else:
            return {"success": 0}




