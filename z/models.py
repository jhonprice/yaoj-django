from django.db import models
from django.contrib.auth.models import User


class Group(models.Model):
    name = models.CharField(max_length=32)
    desc = models.TextField('Group description')

    def __str__(self):
        return self.name


class Member(models.Model):
    user = models.OneToOneField(User)
    group = models.ForeignKey(Group)

    def __str__(self):
        return self.user.username

    @property
    def user_name(self):
        return self.user.username

    @property
    def group_name(self):
        return self.group.name


class Problem(models.Model):
    title = models.CharField(max_length=128)
    mem_limit = models.IntegerField('memory limit(in MB)', default=128)
    time_limit = models.IntegerField('time limit(in ms)', default=1000)
    desc = models.TextField('problem description')
    input_spec = models.TextField('input specification')
    output_spec = models.TextField('output specification')
    sample_input = models.TextField()
    sample_output = models.TextField()
    create_time = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User)
    test_input = models.TextField()
    test_output = models.TextField()

    def __str__(self):
        return self.title

    @property
    def ac_count(self):
        return self.submission_set.filter(verdict='Accepted').count()

    @property
    def submission_count(self):
        return self.submission_set.count()

    @property
    def ac_ratio(self):
        try:
            return self.ac_count/self.submission_count
        except ZeroDivisionError:
            return 0


class Submission(models.Model):
    author = models.ForeignKey(Member)
    problem = models.ForeignKey(Problem)
    create_time = models.DateTimeField(auto_now_add=True)
    mem_consumed = models.IntegerField('memory consumed(in MB)', default=0)
    time_consumed = models.IntegerField('time consumed(in ms)', default=0)
    verdict = models.CharField(max_length=32, default='')
    # 'pending', 'processing', 'done'
    state = models.CharField(max_length=16, default='pending')
    source_code = models.TextField()

    def set_verdict(self, v):
        self.verdict = v
        self.state = 'done'
        self.save()


class StaticPage(models.Model):
    slug = models.SlugField(max_length=32)
    content = models.TextField()

    def __str__(self):
        return self.slug
