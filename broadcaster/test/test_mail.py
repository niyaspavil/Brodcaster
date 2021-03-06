import random
import string
import smtplib_mocker
from .compose_mail_mocker import compose_mail
from ..plugins import mail
from .engine_mocker import Engine
from ..plugin import PluginError

msg=''.join(random.choice(string.lowercase) for x in range(10))
mail.smtplib = smtplib_mocker
engine=Engine("mail")
tmp_plug=mail.mail(engine, msg)	
tmp_plug.engine.mock_input="consumer999"


def test_init():
    """test for mail plugin initialisation"""

    assert tmp_plug.state=="waiting"
    assert tmp_plug.msg==msg

def test_status():
    """test for status method"""
    
    assert tmp_plug.status()=="waiting"

def test_get_user_details():
    """test for get_consumer_details method"""
  
    assert tmp_plug.get_user_details()==['consumer999','consumer999']
    assert tmp_plug.get_user_details()==['consumer999','consumer999']

def test_pre_authenicate():
    """test for pre_authenticate method"""
    assert tmp_plug.pre_authenticate()==True

def test_post():
    """test for post method"""
    assert tmp_plug.post()==True

def test_SMTPAuthenticationError():
    tmp_plug.engine=Engine("mail")
    tmp_plug.engine.mock_input="consumer9999"

    try:
        tmp_plug.post()
    except PluginError:
        pass
def test_SMTPRecipientsRefused():
    tmp_plug.engine=Engine("mail")
    tmp_plug.engine.mock_input="consumer999"
    tmp_plug.compose_mail=compose_mail
    tmp_plug.To_mail = ['consumer99']
    try:
        tmp_plug.post()
    except PluginError:
        pass

def test_SMTPDataError():
    tmp_plug.engine=Engine("mail")
    tmp_plug.engine.mock_input="consumer999"
    tmp_plug.compose_mail=compose_mail
    tmp_plug.To_mail = ['consumer9']
    try:
        tmp_plug.post()
    except PluginError:
        pass

def test_SMTPConnectionError():
    tmp_plug.engine=Engine("mail")
    tmp_plug.engine.mock_input="consumer999"
    tmp_plug.compose_mail=compose_mail
    tmp_plug.To_mail = ['consumer99999']
    try:
        tmp_plug.post()
    except PluginError:
        pass
