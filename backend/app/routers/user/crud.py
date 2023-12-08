#!/usr/bin/python3
"""Module that defines CRUD functions"""

import sys
import jwt
import sqlalchemy
from app import utils
from sqlalchemy import text
from .database import get_db
from . import models, schemas
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import Depends, HTTPException
from ..auth.models import ResetPasswordCodes, RevokedToken
from app.exceptions import (
        ExpectationFailure, NotFoundError, UnAcceptableError, UnAuthorised)


async def is_token_blacklisted(token: str, db: Session):
    """Function to check if token is blacklisted"""

    res = db.query(RevokedToken).filter(RevokedToken.jti == token).first()
    if res is None:
        return False
    return True


async def read_users(db: Session = Depends(get_db),
                     skip: int = 0, limit: int = 100,
                     search: str = None, value: str = None):
    """Function that returns all users"""

    try:
        base = db.query(models.User)
        if search and value:
            try:
                base = base.filter(
                    models.User.__table__.c[search].like("%" + value + "%"))
            except KeyError:
                return base.offset(skip).limit(limit).all()
        return base.offset(skip).limit(limit).all()
    except Exception:
        print("{}: {}".format(sys.exc_info()[0], sys.exc_info()[1]))
        raise HTTPException(status_code=500)


async def read_users_auth(token: str, db: Session):
    """Function that returns all users with access token"""

    try:
        if await is_token_blacklisted(token, db):
            raise UnAuthorised('token blacklisted')
        token_data = utils.decode_token(data=token)
        if token_data:
            return await read_users(db)
        else:
            return UnAuthorised('Not qualified')
    except UnAuthorised:
        raise HTTPException(status_code=401, detail="{}".format(
            sys.exc_info()[1]), headers={"WWW-Authenticate": "Bearer"})
    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException(
                status_code=401,
                detail="Access token expired",
                headers={"WWW-Authenticate": "Bearer"})
    except jwt.exceptions.DecodeError:
        raise HTTPException(
                status_code=500,
                detail="Decode error. Not enough arguments",
                headers={"WWW-Authenticate": "Bearer"})


async def read_user_by_id(id: int, db: Session = Depends(get_db)):
    """Function that returns a user based on id"""

    return db.query(models.User).filter(models.User.id == id).first()


async def read_user_by_id_auth(id: int, token: str, db: Session):
    """Function that returns a user based on id and access token"""

    try:
        if await is_token_blacklisted(token, db):
            raise UnAuthorised('token blacklisted')
        token_data = utils.decode_token(data=token)
        if token_data:
            return await read_user_by_id(id, db)
        else:
            return UnAuthorised('Not qualified')
    except UnAuthorised:
        raise HTTPException(status_code=401, detail="{}".format(
            sys.exc_info()[1]), headers={"WWW-Authenticate": "Bearer"})
    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException(
                status_code=401,
                detail="Access token expired",
                headers={"WWW-Authenticate": "Bearer"})
    except jwt.exceptions.DecodeError:
        raise HTTPException(
                status_code=500,
                detail="Decode error. Not enough arguments",
                headers={"WWW-Authenticate": "Bearer"})


async def read_user_by_email(email: str, db: Session = Depends(get_db)):
    """Function that returns a user based on email"""

    return db.query(models.User).filter(models.User.email == email).first()


async def read_user_by_email_auth(email: str, token: str, db: Session):
    """Function that returns a user based on email and access token"""

    try:
        if await is_token_blacklisted(token, db):
            raise UnAuthorised('token blacklisted')
        token_data = utils.decode_token(data=token)
        if token_data:
            return await read_user_by_email(email, db)
        else:
            return UnAuthorised('Not qualified')
    except UnAuthorised:
        raise HTTPException(status_code=401, detail="{}".format(
            sys.exc_info()[1]), headers={"WWW-Authenticate": "Bearer"})
    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException(
                status_code=401,
                detail="Access token expired",
                headers={"WWW-Authenticate": "Bearer"})
    except jwt.exceptions.DecodeError:
        raise HTTPException(
                status_code=500,
                detail="Decode error. Not enough arguments",
                headers={"WWW-Authenticate": "Bearer"})


async def create_user(payload: schemas.UserCreate,
                      db: Session = Depends(get_db)):
    """Function to create a user"""

    try:
        if not db.query(models.UserType).filter(
                models.UserType.id == payload.user_type_id).first():
            raise NotFoundError('User type not found')
        new_user = models.User(
                **payload.dict(exclude={'password'}),
                password=models.User.generate_hash(payload.password))
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except NotFoundError:
        raise HTTPException(
            status_code=404, detail='{}'.format(sys.exc_info()[1]))
    except IntegrityError:
        db.rollback()
        print('{}'.format(sys.exc_info()[1]))
        raise HTTPException(status_code=409)
    except Exception:
        db.rollback()
        print('{}'.format(sys.exc_info()[1]))
        raise HTTPException(status_code=500)


async def create_user_auth(payload: schemas.UserCreate,
                           token: str,
                           db: Session = Depends(get_db)):
    """Function that creates a user using access token"""

    try:
        if await is_token_blacklisted(token, db):
            raise UnAuthorised('token blacklisted')
        token_data = utils.decode_token(data=token)
        if token_data:
            return await create_user(payload, db)
        else:
            return UnAuthorised('Not qualified')
    except UnAuthorised:
        raise HTTPException(status_code=401, detail="{}".format(
            sys.exc_info()[1]), headers={"WWW-Authenticate": "Bearer"})
    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException(
                status_code=401,
                detail="access token expired",
                headers={"WWW-Authenticate": "Bearer"})
    except jwt.exceptions.DecodeError:
        raise HTTPException(
                status_code=500,
                detail="decode error not enough arguments",
                headers={"WWW-Authenticate": "Bearer"})


async def verify_password(id, payload: schemas.ResetPassword, db: Session):
    """Function to verify a user's password"""

    try:
        user = await read_user_by_id(id, db)
        if not user:
            raise NotFoundError("user with id: {} was not found".format(id))
        return models.User.verify_hash(payload.password, user.password)
    except NotFoundError:
        raise HTTPException(
            status_code=404, detail='{}'.format(sys.exc_info()[1]))
    except Exception:
        raise HTTPException(
            status_code=500, detail='{}'.format(sys.exc_info()[1]))


async def verify_password_auth(id,
                               payload: schemas.ResetPassword,
                               token: str, db: Session = Depends(get_db)):
    """Function to verify a user's password with access token"""

    try:
        if await is_token_blacklisted(token, db):
            raise UnAuthorised('token blacklisted')
        token_data = utils.decode_token(data=token)
        if token_data:
            return await verify_password(id, payload, db)
        else:
            return UnAuthorised('Not qualified')
    except UnAuthorised:
        raise HTTPException(status_code=401, detail="{}".format(
            sys.exc_info()[1]), headers={"WWW-Authenticate": "Bearer"})
    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException(
                status_code=401,
                detail="Access token expired",
                headers={"WWW-Authenticate": "Bearer"})
    except jwt.exceptions.DecodeError:
        raise HTTPException(
                status_code=500,
                detail="Decode error. Not enough arguments",
                headers={"WWW-Authenticate": "Bearer"})


async def read_hash_code(code: str, db: Session):
    """Function to verify password reset code"""

    res = db.execute(
        text("""
        SELECT
            id, code, user_id, user_email, status,
            to_char(date_created, 'YYYY-MM-DD HH24:MI:SS') AS date_created,
            to_char(date_modified, 'YYYY-MM-DD HH24:MI:SS') AS date_modified
        FROM public.reset_password_codes
        WHERE code=:code
        """),
        {'code': code}
    )
    res = res.fetchall()

    result_list = []
    for row in res:
        row_dict = {
            "id": row[0],
            "code": row[1],
            "user_id": row[2],
            "user_email": row[3],
            "status": row[4],
            "date_created": row[5],
            "date_modified": row[6]
        }
        result_list.append(row_dict)

    return result_list


async def read_hash_table(db: Session):
    """Function to read all password reset codes"""

    res = db.execute(
        text("""
        SELECT
            id, code, user_id, user_email, status,
            to_char(date_created, 'YYYY-MM-DD HH24:MI:SS') AS date_created,
            to_char(date_modified, 'YYYY-MM-DD HH24:MI:SS') AS date_modified
        FROM public.reset_password_codes;
        """)
    )
    res = res.fetchall()

    result_list = []
    for row in res:
        row_dict = {
            "id": row[0],
            "code": row[1],
            "user_id": row[2],
            "user_email": row[3],
            "status": row[4],
            "date_created": row[5],
            "date_modified": row[6]
        }
        result_list.append(row_dict)

    return result_list


async def reset_password(id, payload: schemas.ResetPassword, db: Session):
    """Function to reset user password with code"""

    try:
        if not payload.code:
            raise UnAcceptableError('code required')
        if not await read_user_by_id(id, db):
            raise NotFoundError('user not found')
        if not await verify_code(id, payload.code, db):
            raise ExpectationFailure('could not verify reset code')
        db.query(models.User).filter(models.User.id == id).update(
                {'password': models.User.generate_hash(payload.password)})
        db.commit()
        return True
    except UnAcceptableError:
        raise HTTPException(
            status_code=422, detail='{}'.format(sys.exc_info()[1]))
    except NotFoundError:
        raise HTTPException(
            status_code=404, detail='{}'.format(sys.exc_info()[1]))
    except ExpectationFailure:
        raise HTTPException(
            status_code=417, detail='{}'.format(sys.exc_info()[1]))
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="{}: {}".format(
            sys.exc_info()[0], sys.exc_info()[1]))


async def reset_password_auth(id, payload: schemas.ResetPassword,
                              token: str, db: Session = Depends(get_db)):
    """Function to reset user password with code and access token"""

    try:
        if await is_token_blacklisted(token, db):
            raise UnAuthorised('token blacklisted')
        token_data = utils.decode_token(data=token)
        if token_data:
            return await reset_password(id, payload, db)
        else:
            return UnAuthorised('Not qualified')
    except UnAuthorised:
        raise HTTPException(
                status_code=401,
                detail="{}".format(sys.exc_info()[1]),
                headers={"WWW-Authenticate": "Bearer"})
    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException(
                status_code=401,
                detail="access token expired",
                headers={"WWW-Authenticate": "Bearer"})
    except jwt.exceptions.DecodeError:
        raise HTTPException(
                status_code=500,
                detail="Decode error. Not enough arguments",
                headers={"WWW-Authenticate": "Bearer"})


async def reset_password_(email, payload: schemas.ResetPassword, db: Session):
    """Function to reset user password using email"""

    try:
        if not payload.code:
            raise UnAcceptableError('Code required')
        if not await read_user_by_email(email, db):
            raise NotFoundError('User not found')
        if not await verify_code_(email, payload.code, db):
            raise ExpectationFailure('could not verify reset code')
        db.query(models.User).filter(models.User.email == email).update(
                {'password': models.User.generate_hash(payload.password)})
        db.commit()
        return True
    except UnAcceptableError:
        raise HTTPException(
            status_code=422, detail='{}'.format(sys.exc_info()[1]))
    except NotFoundError:
        raise HTTPException(
            status_code=404, detail='{}'.format(sys.exc_info()[1]))
    except ExpectationFailure:
        raise HTTPException(
            status_code=417, detail='{}'.format(sys.exc_info()[1]))
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="{}: {}".format(
            sys.exc_info()[0], sys.exc_info()[1]))


async def reset_password_auth_(email, payload: schemas.ResetPassword,
                               token: str, db: Session = Depends(get_db)):
    """Function to reset password using email and access token"""

    try:
        if await is_token_blacklisted(token, db):
            raise UnAuthorised('token blacklisted')
        token_data = utils.decode_token(data=token)
        if token_data:
            return await reset_password_(email, payload, db)
        else:
            return UnAuthorised('Not qualified')
    except UnAuthorised:
        raise HTTPException(
                status_code=401,
                detail="{}".format(sys.exc_info()[1]),
                headers={"WWW-Authenticate": "Bearer"})
    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException(
                status_code=401,
                detail="access token expired",
                headers={"WWW-Authenticate": "Bearer"})
    except jwt.exceptions.DecodeError:
        raise HTTPException(
                status_code=500,
                detail="decode error not enough arguments",
                headers={"WWW-Authenticate": "Bearer"})


async def change_password(email: str, password: str, db: Session):
    """Function to change user password directly"""

    db.execute("""UPDATE public.users SET email=:email,
               password=:password WHERE email=:email;""",
               {'email': email,
                'password': models.User.generate_hash(password)})
    db.commit()


async def verify_code(id, code, db: Session):
    """Function to verify password reset code"""

    return db.query(ResetPasswordCodes).filter(sqlalchemy.and_(
        ResetPasswordCodes.user_id == id,
        ResetPasswordCodes.code == code)).first()


async def verify_code_auth(id, code, token: str,
                           db: Session = Depends(get_db)):
    """Function to verify reset code with token"""

    try:
        if await is_token_blacklisted(token, db):
            raise UnAuthorised('token blacklisted')
        token_data = utils.decode_token(data=token)
        if token_data:
            return await verify_code(id, code, db)
        else:
            return UnAuthorised('Not qualified')
    except UnAuthorised:
        raise HTTPException(status_code=401, detail="{}".format(
            sys.exc_info()[1]), headers={"WWW-Authenticate": "Bearer"})
    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException(
                status_code=401,
                detail="Access token expired",
                headers={"WWW-Authenticate": "Bearer"})
    except jwt.exceptions.DecodeError:
        raise HTTPException(
                status_code=500,
                detail="Decode error. Not enough arguments",
                headers={"WWW-Authenticate": "Bearer"})


async def verify_code_(email, code, db: Session):
    """Function to verify password reset code by email"""

    return db.query(ResetPasswordCodes).filter(sqlalchemy.and_(
        ResetPasswordCodes.user_email == email,
        ResetPasswordCodes.code == code)).first()


async def verify_code_auth_(email, code, token: str,
                            db: Session = Depends(get_db)):
    """Function to verify reset code with token"""

    try:
        if await is_token_blacklisted(token, db):
            raise UnAuthorised('token blacklisted')
        token_data = utils.decode_token(data=token)
        if token_data:
            return await verify_code_(email, code, db)
        else:
            return UnAuthorised('Not qualified')
    except UnAuthorised:
        raise HTTPException(status_code=401, detail="{}".format(
            sys.exc_info()[1]), headers={"WWW-Authenticate": "Bearer"})
    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException(
                status_code=401,
                detail="Access token expired",
                headers={"WWW-Authenticate": "Bearer"})
    except jwt.exceptions.DecodeError:
        raise HTTPException(
                status_code=500,
                detail="Decode error. Not enough arguments",
                headers={"WWW-Authenticate": "Bearer"})


async def update_user(id: int, payload: schemas.UserUpdate,
                      db: Session = Depends(get_db)):
    """Function to update user with id"""

    try:
        if not await read_user_by_id(id, db):
            raise NotFoundError('user not found')
        res = db.query(models.UserInfo).filter(
                models.UserInfo.user_id == id).update(
                        payload.dict(exclude_unset=True))
        db.commit()
        if bool(res):
            return await read_user_by_id(id, db)
    except NotFoundError:
        raise HTTPException(
            status_code=404, detail='{}'.format(sys.exc_info()[1]))
    except IntegrityError:
        db.rollback()
        print("{}: {}".format(sys.exc_info()[0], sys.exc_info()[1]))
        raise HTTPException(
            status_code=409, detail="unique constraint failed on index")
    except Exception:
        db.rollback()
        print("{}: {}".format(sys.exc_info()[0], sys.exc_info()[1]))
        raise HTTPException(status_code=500, detail="{}: {}".format(
            sys.exc_info()[0], sys.exc_info()[1]))


async def update_user_auth(id: int, payload: schemas.UserUpdate,
                           token: str, db: Session = Depends(get_db)):
    """Function to update user by id and token"""

    try:
        if await is_token_blacklisted(token, db):
            raise UnAuthorised('token blacklisted')
        token_data = utils.decode_token(data=token)
        if token_data:
            return await update_user(id, payload, db)
        else:
            return UnAuthorised('Not qualified')
    except UnAuthorised:
        raise HTTPException(
                status_code=401,
                detail=str(sys.exc_info()[1]),
                headers={"WWW-Authenticate": "Bearer"})
    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException(
                status_code=401,
                detail="access token expired",
                headers={"WWW-Authenticate": "Bearer"})
    except jwt.exceptions.DecodeError:
        raise HTTPException(
                status_code=500,
                detail="decode error not enough arguments",
                headers={"WWW-Authenticate": "Bearer"})


async def delete_user(id: int, db):
    """Function to delete a user by id"""

    try:
        user = await read_user_by_id(id, db)
        if user:
            db.delete(user)
        db.commit()
        return True
    except Exception:
        db.rollback()
        print("{}: {}".format(sys.exc_info()[0], sys.exc_info()[1]))
        raise HTTPException(status_code=500)


async def delete_user_auth(id: int, token: str,
                           db: Session = Depends(get_db)):
    """Function to delete a user based on id with token"""

    try:
        if await is_token_blacklisted(token, db):
            raise UnAuthorised('token blacklisted')
        token_data = utils.decode_token(data=token)
        if token_data:
            return await delete_user(id, db)
        else:
            return UnAuthorised('Not qualified')
    except UnAuthorised:
        raise HTTPException(
                status_code=401,
                detail="{}".format(sys.exc_info()[1]),
                headers={"WWW-Authenticate": "Bearer"})
    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException(
                status_code=401,
                detail="Access token expired",
                headers={"WWW-Authenticate": "Bearer"})
    except jwt.exceptions.DecodeError:
        raise HTTPException(
                status_code=500,
                detail="Decode error. Not enough arguments",
                headers={"WWW-Authenticate": "Bearer"})
