#encoding=utf-8
from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser

class UserManager(BaseUserManager):
    def create_user(self,email,surname,name,password=None):
        if not email:
            raise ValueError('Users must have an email address')
        user=self.model(surname=surname,name=name,
                email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,email,surname,name,password):
        user=self.create_user(email,surname,name,password)
        user.is_admin=True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    name=models.CharField(u'名字',max_length=20,null=True)
    surname=models.CharField(u'姓',max_length=20,null=True)
    email=models.EmailField(u'Email Address',unique=True)
    is_active=models.BooleanField(default=False)
    is_admin=models.BooleanField(default=False)
    addTime=models.DateTimeField(auto_now_add=True)
    avatar=models.ImageField(upload_to='avatar',verbose_name=u"Avatar",default='')
    follower=models.ManyToManyField('self',symmetrical=False,through='UserFollow',related_name="ufollow")

    objects=UserManager()

    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['name','surname']

    class Meta:
        verbose_name=u'用户'
    
    def __unicode__(self):
        return self.get_full_name()

    def get_short_name(self):
        return self.name

    def get_full_name(self):
        return '%s%s' %(self.surname,self.name)

    def has_perm(self,perm,obj=None):
        return True

    def has_module_perms(self,add_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
    def get_full_name(self):
        return self.surname+self.name

    def get_absolute_url(self):
        return reverse("user_detail",args=[self.id])
    #@property
    #def is_active(self):
        #return self.is_active

class UserFollow(models.Model):
    ufollow=models.ForeignKey(User,related_name="from_user")
    tuser=models.ForeignKey(User,related_name="to_user")
    addtime=models.DateTimeField(auto_now_add=True)
     

class Register_Temp(models.Model):
    email=models.EmailField()
    activecode=models.CharField(max_length=36,primary_key=True)
    addTime=models.DateTimeField(auto_now_add=True)


