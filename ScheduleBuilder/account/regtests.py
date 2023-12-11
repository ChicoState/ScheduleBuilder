import pytest
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
from django.urls import reverse
from django.test import Client
from unittest.mock import Mock, patch
import requests
from profile.models import *

@pytest.mark.django_db
def test_create_user():
    user = Account.objects.create_user(
        email='test@example.com',
        username='testuser',
        password='testpassword',
    )
    assert user.email == 'test@example.com'
    assert user.username == 'testuser'
    assert user.check_password('testpassword')
    assert not user.is_admin
    assert user.is_active
    assert not user.is_staff
    assert not user.is_superuser


@pytest.mark.django_db
def test_create_user2():
    user = Account.objects.create_user(
        email='monkeyswam@gmail.com',
        username='monkeyfan',
        password='monkey123',
    )
    assert user.email == 'monkeyswam@gmail.com'
    assert user.username == 'monkeyfan'
    assert user.check_password('monkey123')
    assert not user.is_admin
    assert user.is_active
    assert not user.is_staff
    assert not user.is_superuser


@pytest.mark.django_db
def test_create_superuser():
    admin_user = Account.objects.create_superuser(
        email='superimportantguy@gmail.com',
        username='bossman',
        password='moneymaker123',
    )
    assert admin_user.email == 'superimportantguy@gmail.com'
    assert admin_user.username == 'bossman'
    assert admin_user.check_password('moneymaker123')
    assert admin_user.is_admin
    assert admin_user.is_active
    assert admin_user.is_staff
    assert admin_user.is_superuser

@pytest.mark.django_db
def test_create_user_invalid_email_sad():
    with pytest.raises(ValidationError) as e:
        # Use validate_email to raise ValidationError for invalid email
        validate_email('invalidemail')
        # Create a user with the same invalid email to test the create_user method
        Account.objects.create_user(
            email='invalidemail',
            username='testuser',
            password='testpassword',
        )
    print(f"Exception message: {e}")

@pytest.mark.django_db
def test_create_user_invalid_email2_sad():
    with pytest.raises(ValidationError) as e:
        # Use validate_email to raise ValidationError for invalid email
        validate_email('@@@')
        # Create a user with the same invalid email to test the create_user method
        Account.objects.create_user(
            email='@@@',
            username='testuser',
            password='testpassword',
        )
    print(f"Exception message: {e}")

@pytest.mark.django_db
def test_create_user_no_email_sad():
    with pytest.raises(ValueError) as e:
        Account.objects.create_user(
            email='',  # Empty email should raise ValueError
            username='testuser3',
            password='testpassword',
        )
    print(f"Exception message: {e}")

@pytest.mark.django_db
def test_create_user_no_username_sad():
    with pytest.raises(ValueError) as e:
        Account.objects.create_user(
            email='test3@example.com',
            username='',  # Empty username should raise ValueError
            password='testpassword',
        )
    print(f"Exception message: {e}")
