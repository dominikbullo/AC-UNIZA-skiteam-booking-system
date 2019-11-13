from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    # USER_TYPE_CHOICES = (
    #     (1, 'child'),
    #     (2, 'parent'),
    #     (3, 'coach'),
    #     (4, 'admin'),
    # )
    #
    # user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES, default=1)
    pass


#
# class FamilyName(models.Model):
#     id = models.AutoField(primary_key=True)
#
#
# class FamilyMember(models.Model):
#     family_name = models.ForeignKey(FamilyName)
#     first_name = models.CharField(max_length=50)
#     parents = models.ManyToManyField('self', null=True, blank=True, related_name='p', symmetrical=False)
#     children = models.ManyToManyField('self', null=True, blank=True, related_name='c', symmetrical=False)

class Parent:
    # group.permissions.set([permission_list])

    pass


class Child:
    pass


class Coach:
    pass
