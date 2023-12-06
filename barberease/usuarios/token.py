from datetime import datetime


from django.utils.crypto import constant_time_compare, salted_hmac
from django.utils.http import base36_to_int, int_to_base36
from django.conf import settings
class PasswordResetTokenGenerator:
    hash = "Going_Merry.Nica.Zoro.Sanji.Brook.Jimbe.Franky.Nico_Robin.Chopper.Usopp.Nami"
    secret_key = None
    algorithm = None

    def __init__(self, algorithm='sha256'):
        self.secret_key = settings.SECRET_KEY
        self.algorithm = algorithm

    def check_token(self,user, token):

        try:
            ts_b36, _ = token.split("-")
        except ValueError:
            return False

        try:
            ts = base36_to_int(ts_b36)
        except ValueError:
            return False

        if self.secret_key:
            if constant_time_compare(
                self._make_token_with_timestamp(user, ts,  self.secret_key),
                token,
            ) == False:
                return False
        else:
            return False
        # 5 minutos para redefinir a senha
        if (int((datetime.now() - datetime(2001, 1, 1)).total_seconds()) - ts) > 300:
            return False
        return True

    def make_token(self ,user):
        timestamp = int((datetime.now() - datetime(2001, 1, 1)).total_seconds())
        return self._make_token_with_timestamp(user ,  timestamp, self.secret_key)

    def _make_token_with_timestamp(self,user,timestamp, secret):
        ts_b36 = int_to_base36(timestamp)
        hash_string = salted_hmac(self.hash, self._make_hash_value( user, timestamp), secret=secret, algorithm=self.algorithm).hexdigest()[::2]
        return "%s-%s" % (ts_b36, hash_string)

    def _make_hash_value(self, user, timestamp):
        login_timestamp = (
            ""
            if user.last_login is None
            else user.last_login.replace(microsecond=0, tzinfo=None)
        )
        return f"{user.id}{user.password}{login_timestamp}{timestamp}{user.email}"

token_generator_password = PasswordResetTokenGenerator()