import uuid
from django.db import models


class Company(models.Model):
    STATUS = (
        ("ACTIVE", "active"),
        ("INACTIVE", "inactive")
    )

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid1,
        editable=False)
    name = models.CharField(max_length=250)
    status = models.CharField(max_length=20, choices=STATUS, default="ACTIVE")

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Companies"

    def __str__(self):
        return self.name


class Transaction(models.Model):
    STATUS = (
        ("CLOSE", "closed"),
        ("REVERSED", "reversed"),
        ("PENDING", "pending")
    )

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    company_id = models.ForeignKey(
        Company,
        related_name="transaction",
        on_delete=models.CASCADE,
        null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    date = models.DateField(auto_now_add=True)
    status_transaction = models.CharField(max_length=20, choices=STATUS)
    status_approved = models.BooleanField()
    final_charge_done = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if (self.status_transaction == "closed") and (self.status_approved == True):
            self.final_charge_done = True
        else:
            self.final_charge_done = False
        super().save(*args, **kwargs)

    class Meta:
        ordering = ["-date"]
        verbose_name_plural = "Transactions"

    def __str__(self):
        return f"{self.price} at {self.date}"