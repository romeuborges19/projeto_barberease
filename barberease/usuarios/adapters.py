from allauth.account.adapter import DefaultAccountAdapter

class CustomAccountAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form, commit=False):
        user = super().save_user(request, user, form, commit)
        print(user) 
        print(user.email)
        print("hsgdsugfi")
        user.username = user.email
        user.save()
        return user
