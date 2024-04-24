from django.db import models
from school.models import School
from athletes.models import Athlete
from accounts.models import User
from django.urls import reverse

# Create your models here.
class TransferRequest(models.Model):
    sfrom = models.ForeignKey(
        School, verbose_name="", on_delete=models.CASCADE, related_name="from_school"
    )
    athlete = models.ForeignKey(Athlete, verbose_name="", on_delete=models.CASCADE)
    sto = models.ForeignKey(
        School, verbose_name="", on_delete=models.CASCADE, related_name="to_school"
    )
    initiation_date = models.DateField(auto_now_add=True)
    status = models.CharField(
        max_length=10,
        choices=[
            ("Pending", "Pending"),
            ("Accepted", "Accepted"),
            ("Rejected", "Rejected"),
        ],
        default="Pending",
    )


def __str__(self):
    return f"From {self.sfrom} to {self.sto} "



class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    transfer_request = models.ForeignKey(TransferRequest, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse("transfer_request_detail", args=[str(self.id)])

    def __str__(self):
        return f"{self.user.username} - Transfer Request #{self.transfer_request.id}"
