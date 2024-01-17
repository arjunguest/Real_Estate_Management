from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, BaseUserManager

from django.utils import timezone

# Create your models here.
ROLE_CHOICES = (
    ("tenant", "Tenant"),
    ("vendor", "Vendor"),
    ("admin", "Admin"),
)

class AiUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(email, password)
        user.is_admin = True
        user.role = "admin"
        user.is_staff = True
        user.save(using=self._db)
        return user

class AiUser(AbstractBaseUser):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100,unique=True)
    password = models.CharField(max_length=100)
    role = models.CharField(max_length = 20, choices = ROLE_CHOICES, default = 'tenant')
    date_joined = models.DateTimeField(default=timezone.now)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    
    objects = AiUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin
    class Meta:
        verbose_name = "Ai User"
        verbose_name_plural = "Ai Users"

class Property(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    post_image = models.ImageField(upload_to='post_images/',blank=True)
    location = models.CharField(max_length=255)
    features = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Property"
        verbose_name_plural = "Property"

class Unit(models.Model):
    properties = models.ForeignKey(Property, on_delete=models.CASCADE)
    rent_cost = models.DecimalField(max_digits=10, decimal_places=2)
    type_choices = [
        ('1BHK', '1BHK'),
        ('2BHK', '2BHK'),
        ('3BHK', '3BHK'),
        ('4BHK', '4BHK'),
    ]
    unit_type = models.CharField(max_length=4, choices=type_choices)

    def __str__(self):
        return f"{self.properties.name} - {self.unit_type}"
    
    class Meta:
        verbose_name = "Unit"
        verbose_name_plural = "Unit"

class Tenant(models.Model):
    user = models.OneToOneField(AiUser, on_delete=models.CASCADE)
    address = models.TextField()
    document_proofs = models.TextField()

    def __str__(self):
        return self.user.name
    
    class Meta:
        verbose_name = "Tenant"
        verbose_name_plural = "Tenant"

class Lease(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    agreement_end_date = models.DateField()
    monthly_rent_date = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.tenant.user.name} - {self.unit.properties.name}"
    
    class Meta:
        verbose_name = "Lease"
        verbose_name_plural = "Lease"
