from fastapi import HTTPException

user_doesnt_exist = HTTPException(status_code=404, detail='User does\'t exists')
same_password = HTTPException(status_code=403, detail='New password must be different from current password')
bad_code = HTTPException(status_code=401, detail='Invalid confirmation code')
bad_token = HTTPException(status_code=401, detail="Could not validate refresh token")
not_entered_code = HTTPException(status_code=403, detail='Confirmation code was not entered')
user_not_in_changes = HTTPException(status_code=403, detail='User didn\'t reset password')
credentials_exception = HTTPException(status_code=401, detail="Could not validate credentials",
                                      headers={"WWW-Authenticate": "Bearer"})
