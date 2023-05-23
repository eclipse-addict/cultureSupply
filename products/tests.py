from django.test import TestCase
from products.models import kicks

# Create your tests here.


class KickTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        kicks.objects.get(brnad='nike')
        
    
    
    # def test_name_label(self):

    #     first_member =Member.objects.get(name='byeonguk').first_name

    #     self.assertEquals(first_name, 'first name')


    # def test_age_bigger_19(self):

    #     age = Member.objects.get(name='byeonguk').age

    #     check_age = age > 19

    #     self.assertTrue(check_age)