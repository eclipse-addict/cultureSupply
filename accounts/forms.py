from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth import get_user_model


class CustomedUserCreateForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):

        model = get_user_model()
        # fields = UserCreationForm.Meta.fields 
        fields = UserCreationForm.Meta.fields 

class CustomedUserUpdateForm(UserChangeForm):
    
    class Meta(UserChangeForm.Meta):
        model = get_user_model()
        fields = UserChangeForm.Meta.fields + ('email', 
                                               'first_name', 
                                               'last_name',
                                               )