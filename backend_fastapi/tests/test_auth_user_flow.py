from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import models
import schemas
from app.services import auth_service, user_service


def create_test_db_session():
    engine = create_engine('sqlite:///:memory:', connect_args={'check_same_thread': False})
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    models.Base.metadata.create_all(bind=engine)
    return TestingSessionLocal()


def test_register_and_login_success():
    db = create_test_db_session()
    try:
        register_req = schemas.RegisterRequest(account='u1', password='pass123', nickname='测试A')
        ok, payload = auth_service.register(db, register_req)
        assert ok is True
        assert payload['user_id'] > 0

        login_req = schemas.LoginRequest(account='u1', password='pass123')
        ok, payload = auth_service.login(db, login_req)
        assert ok is True
        assert payload['nickname'] == '测试A'
        assert payload['is_guest'] is False
    finally:
        db.close()


def test_register_duplicate_account_fails():
    db = create_test_db_session()
    try:
        req = schemas.RegisterRequest(account='dup', password='p', nickname='A')
        ok, _ = auth_service.register(db, req)
        assert ok is True

        ok, payload = auth_service.register(db, req)
        assert ok is False
        assert payload['code'] == 400
    finally:
        db.close()


def test_login_wrong_password_fails():
    db = create_test_db_session()
    try:
        req = schemas.RegisterRequest(account='u2', password='pass123', nickname='测试B')
        ok, _ = auth_service.register(db, req)
        assert ok is True

        login_req = schemas.LoginRequest(account='u2', password='wrong')
        ok, payload = auth_service.login(db, login_req)
        assert ok is False
        assert payload['code'] == 400
    finally:
        db.close()


def test_update_nickname_success_and_validate_length():
    db = create_test_db_session()
    try:
        req = schemas.RegisterRequest(account='u3', password='pass123', nickname='旧昵称')
        ok, register_payload = auth_service.register(db, req)
        assert ok is True

        ok, payload = user_service.update_nickname(db, register_payload['user_id'], '新昵称')
        assert ok is True
        assert payload['nickname'] == '新昵称'

        ok, payload = user_service.update_nickname(db, register_payload['user_id'], 'x' * 21)
        assert ok is False
        assert payload['code'] == 400
    finally:
        db.close()
