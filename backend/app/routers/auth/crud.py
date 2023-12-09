#!/usr/bin/python3
"""Module that defines CRUD functions"""

import sys
import jwt
from app import utils
from sqlalchemy import text
from . import models, schemas
from app.config import settings
from fastapi import HTTPException
from .database import SessionLocal
from sqlalchemy.orm import Session
from app.schedulers import scheduler
from ..user.crud import read_user_by_id
from app.routers.user.models import User
from datetime import datetime, timedelta
from app.services.email import Mail, send_in_background
from app.exceptions import (ExpectationFailure, NotFoundError,
                            UnAcceptableError, UnAuthorised)
from app.static.email_templates.reset_password import reset_password_template

ATD = settings.ACCESS_TOKEN_DURATION_IN_MINUTES
RTD = settings.REFRESH_TOKEN_DURATION_IN_MINUTES
RPC = models.ResetPasswordCodes.generate_code()
RPS = settings.RESET_PASSWORD_SESSION_DURATION_IN_MINUTES


async def authenticate(payload: schemas.Auth, db: Session):
    """Function to login/authenticate a user"""

    try:
        user = db.query(User).filter(User.email == payload.email).first()
        if not user:
            raise NotFoundError('User not found')

        query = text("SELECT user_type_id FROM \
                public.user WHERE email = :email")
        user_type = db.execute(query, {'email': payload.email}).scalar()
        if user_type is not None and user_type < 3:
            if User.verify_hash(payload.password, user.password):
                access_token = utils.create_token(data={'email': payload.email,
                                                        'id': user.id})
                refresh_token = utils.create_token(data={'email':
                                                         payload.email,
                                                         'id': user.id})
                return {"access_token": access_token,
                        "refresh_token": refresh_token,
                        "user": user}
            else:
                raise UnAuthorised('Invalid password')
        else:
            raise UnAuthorised('This user is not allowed to log in')
    except UnAuthorised:
        raise HTTPException(status_code=401, detail="Unauthorized")
    except NotFoundError:
        raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        print("Unhandled exception:", repr(e))
        raise HTTPException(status_code=500,
                            detail="An internal server error occurred")


async def revoke_token(payload: schemas.Token, db: Session):
    """Function that defines revoked access tokens"""

    try:
        db.add_all([models.RevokedToken(jti=token) for token in list(
            {v for (k, v) in payload.dict().items()}) if token is not None])
        db.commit()
        db.close()
        return True
    except Exception:
        db.rollback()
        db.close()
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=500)


async def refresh_token(payload: schemas.Token, db: Session):
    """Function to refresh access tokens"""

    try:
        if not payload.refresh_token:
            raise UnAcceptableError('refresh token needed')
        if await is_token_blacklisted(payload.refresh_token, db):
            raise UnAuthorised('refresh token blacklisted')
        if await revoke_token(payload, db):
            data = utils.decode_token(data=payload.refresh_token)
            access_token = utils.create_token(data={'email':
                                                    data.get('email'),
                                                    'id': data.get('id')},
                                              expires_delta=timedelta(
                                                  minutes=ATD))
            refresh_token = utils.create_token(data={'email':
                                                     data.get('email'),
                                                     'id': data.get('id')},
                                               expires_delta=timedelta(
                                                   minutes=RTD))
            return {'access_token': access_token,
                    'refresh_token': refresh_token}
        else:
            raise ExpectationFailure()
    except UnAcceptableError:
        raise HTTPException(status_code=422,
                            detail="{}".format(sys.exc_info()[1]))
    except UnAuthorised:
        raise HTTPException(status_code=401,
                            detail="{}".format(sys.exc_info()[1]))
    except ExpectationFailure:
        raise HTTPException(status_code=417,
                            detail="{}".format(sys.exc_info()[1]))
    except jwt.exceptions.DecodeError:
        raise HTTPException(status_code=500,
                            detail="{}".format(sys.exc_info()[1]))
    except Exception as e:
        print("Unhandled exception:", repr(e))
        raise HTTPException(status_code=500)


async def is_token_blacklisted(token: str, db: Session):
    """Function to check if token is blacklisted"""

    res = db.query(models.RevokedToken).filter(models.RevokedToken.jti ==
                                               token).first()
    if res is None:
        return False
    return True


async def request_password_reset(payload: schemas.UserBase,
                                 db: Session, background_tasks):
    """Function to request reset password code with id"""

    try:
        user = db.query(models.User).filter(models.User.email ==
                                            payload.email).first()
        if not user:
            raise NotFoundError('user not found')
        while True:
            new_code = models.ResetPasswordCodes(user_id=user.id, code=RPC)
            code = db.query(models.ResetPasswordCodes).filter(
                    models.ResetPasswordCodes.user_id == user.id).first()
            if code:
                db.delete(code)
                db.flush()
            break
        db.add(new_code)
        db.commit()
        db.refresh(new_code)
        scheduler.add_job(delete_password_reset_code,
                          trigger='date',
                          kwargs={'id': new_code.id},
                          id='ID{}'.format(new_code.id),
                          replace_existing=True,
                          run_date=datetime.utcnow()+timedelta(minutes=RPS))
        await send_in_background(background_tasks,
                                 Mail(email=['{}'.format(payload.email)],
                                      content={'code': new_code.code}),
                                 reset_password_template)
        return True
    except NotFoundError:
        raise HTTPException(status_code=404,
                            detail="{}".format(sys.exc_info()[1]))
    except ExpectationFailure:
        raise HTTPException(status_code=404,
                            detail="{}".format(sys.exc_info()[1]))
    except Exception:
        db.rollback()
        print("{}".format(sys.exc_info()[1]))
        raise HTTPException(status_code=500)


async def request_password_reset_(payload: schemas.UserBase,
                                  db: Session, background_tasks):
    """Function to request password reset code with email"""

    try:
        user = db.query(User).filter(User.email == payload.email).first()
        if not user:
            raise NotFoundError('User not found')
        while True:
            new_code = models.ResetPasswordCodes(user_email=user.email,
                                                 code=RPC)
            code = db.query(models.ResetPasswordCodes).filter(
                    models.ResetPasswordCodes.user_email ==
                    user.email).first()
            if code:
                db.delete(code)
                db.flush()
            break
        db.add(new_code)
        db.commit()
        db.refresh(new_code)
        scheduler.add_job(delete_password_reset_code,
                          trigger='date',
                          kwargs={'id': new_code.id},
                          id='ID{}'.format(new_code.id),
                          replace_existing=True,
                          run_date=datetime.utcnow()+timedelta(minutes=RPS))
        await send_in_background(background_tasks,
                                 Mail(email=['{}'.format(payload.email)],
                                      content={'code': new_code.code}),
                                 reset_password_template)
        return True
    except NotFoundError:
        raise HTTPException(
            status_code=404, detail="{}".format(sys.exc_info()[1]))
    except ExpectationFailure:
        raise HTTPException(
            status_code=404, detail="{}".format(sys.exc_info()[1]))
    except Exception:
        db.rollback()
        print("{}".format(sys.exc_info()[1]))
        raise HTTPException(status_code=500)


async def get_current_user(token: str, db: Session):
    """Function to retrieve current user logged in"""

    try:
        if await is_token_blacklisted(token, db):
            raise UnAuthorised('Access token blacklisted')
        token_data = utils.decode_token(data=token)
        if token_data:
            return await read_user_by_id(token_data['id'], db)
    except UnAuthorised:
        raise HTTPException(status_code=401, detail="{}".format(
            sys.exc_info()[1]), headers={"WWW-Authenticate": "Bearer"})
    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException(status_code=401,
                            detail="Access token expired",
                            headers={"WWW-Authenticate": "Bearer"})
    except jwt.exceptions.DecodeError:
        raise HTTPException(status_code=500,
                            detail="Decode error not enough arguments",
                            headers={"WWW-Authenticate": "Bearer"})


def delete_password_reset_code(id: int, db: Session = SessionLocal()):
    """Function to delete password reset code"""

    try:
        code = db.query(models.ResetPasswordCodes).filter(
                models.ResetPasswordCodes.id == id).first()
        if code:
            db.delete(code)
        db.commit()
        return True
    except Exception:
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=500)
