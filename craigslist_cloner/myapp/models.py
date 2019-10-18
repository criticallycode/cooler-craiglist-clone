from django.db import models

# Create your models here.
class Search(models.Model):
    search = models.CharField(max_length=500)
    created = models.DateTimeField(auto_now=True)

    # controls how instances of the object are displayed
    def __str__(self):
        return '{}'.format(self.search)

    # controls attributes of the class, like how the plural version of the
    # class name is displayed
    class Meta:
        verbose_name_plural = "Searches"