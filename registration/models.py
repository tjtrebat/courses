from django.db.models.signals import post_save
from django.dispatch import receiver
from teacher.models import *

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    teacher = models.ForeignKey(User, null=True, blank=True, related_name='profilesAsTeacher')
    courses = models.ManyToManyField(Course, null=True, blank=True)

    @models.permalink
    def get_absolute_url(self):
        return ('teacher:update_student', (self.user.id,), {})

    def is_student(self):
        if self.user.groups.filter(name="students").count() > 0:
            return True
        return False

    def is_teacher(self):
        if self.user.groups.filter(name="teachers").count() > 0:
            return True
        return False

    def __unicode__(self):
        return unicode(self.user)

@receiver(post_save, sender=User)
def create_profile(sender, **kwargs):
    UserProfile.objects.get_or_create(user=kwargs['instance'])