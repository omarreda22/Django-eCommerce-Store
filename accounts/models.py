from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class AccountManger(BaseUserManager):
    def create_user(self, first_name, last_name, username, email, password=None):
        if not email :
            raise ValueError('User must have an email address')
        if not username :
            raise ValueError('User must have an username')

        user = self.model(
            # normalize_email => if as write captel char it turn for samll char
            email = self.normalize_email(email),
            first_name = first_name,
            last_name = last_name,
            username = username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, first_name, last_name, username, email, password):
        user = self.create_user(
            email = self.normalize_email(email),
            first_name = first_name,
            last_name = last_name,
            username = username,
            password = password,
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        
        user.save(using=self._db)
        return user

class Account(AbstractBaseUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    Phone_number = models.CharField(max_length=50)

    # Required
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)
    
    
    date_joined_for_format = models.DateTimeField(auto_now_add=True)
    last_login_for_format  = models.DateTimeField(auto_now_add=True)
    def date_joined(self):
        return self.date_joined_for_format.strftime('%B %d %Y')
    def last_login(self):
        return self.last_login_for_format.strftime('%B %d %Y')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects = AccountManger()

    def __str__(self):
        return self.email
    
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    # he has all the permission to do all the changes
    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True


class UserProfile(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE)
    address = models.TextField(blank=True, max_length=500)
    profile_picture = models.ImageField(blank=True, upload_to='userprofile',default='static/user_image_default.png')
    city = models.CharField(blank=True, max_length=20)
    state = models.CharField(blank=True, max_length=20)
    country = models.CharField(blank=True, max_length=20)

    def __str__(self):
        return self.user.first_name
