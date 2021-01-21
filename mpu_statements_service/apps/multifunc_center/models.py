from django.db import models
from django.urls import reverse


def category_directory_path(instance, filename):
    return 'blanks/{0}/{1}'.format(instance.get_category_display(), filename)


class Blank(models.Model):
    doc_category = 1
    student_category = 2
    teacher_category = 3
    CATEGORIES = (
        (doc_category, 'doc'),
        (student_category, 'student'),
        (teacher_category, 'teacher'),
    )
    title = models.CharField(max_length=200)
    blank = models.FileField(verbose_name="Файлы", upload_to=category_directory_path)
    slug = models.SlugField(unique=True, null=False)
    category = models.SmallIntegerField(choices=CATEGORIES)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blank', kwargs={'slug': self.slug})
