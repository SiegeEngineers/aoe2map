from django.contrib.auth.models import User

from mapsapp.models import Vote
from mapsapp.tests.aoe2maptest import AbstractAoe2mapTest
from mapsapp.helpers import count_voters


class VotesTest(AbstractAoe2mapTest):

    def test_count_voters_two_users_two_rms(self):
        first_user = User.objects.create_user(username='firstuser', password='password')
        second_user = User.objects.create_user(username='seconduser', password='password')

        rms1 = self.create_sample_map()
        rms2 = self.create_sample_map(newer_version=rms1)

        Vote(rms=rms1, user=first_user).save()
        Vote(rms=rms2, user=second_user).save()

        self.assertEquals(2, count_voters(rms1))
        self.assertEquals(2, count_voters(rms2))

    def test_count_voters_one_user_two_rms(self):
        user = User.objects.create_user(username='user', password='password')

        rms1 = self.create_sample_map()
        rms2 = self.create_sample_map(newer_version=rms1)

        Vote(rms=rms1, user=user).save()
        Vote(rms=rms2, user=user).save()

        self.assertEquals(1, count_voters(rms1))
        self.assertEquals(1, count_voters(rms2))
