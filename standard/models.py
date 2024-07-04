from django.db import models


class standard_master(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    # school_id = models.CharField(max_length=5, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.name)
    
    class Meta:
        db_table = 'standard_master'
        ordering = ['created_at']
        verbose_name = "Standard-Master"
        verbose_name_plural = "Standard-Master"
