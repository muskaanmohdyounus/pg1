from django.db import models

class Expense(models.Model):
    CATEGORY_CHOICES = [
        ('Rent', 'Rent'),
        ('Electricity', 'Electricity'),
        ('Groceries', 'Groceries'),
        ('Maintenance', 'Maintenance'),
        ('Salary', 'Salary'),
        ('Misc', 'Miscellaneous'),
    ]

    title = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    date = models.DateField()
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.title} - {self.amount}"
