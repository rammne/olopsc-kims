from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from simple_history.models import HistoricalRecords


class Inventory(models.Model):
	name = models.CharField(max_length=200)

	def __str__(self):
		return self.name

class Item(models.Model):
	inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE, null=True)
	name = models.CharField(max_length=100)
	image = models.ImageField(upload_to='item_pics')
	quantity = models.IntegerField(blank=True, null=True)
	student = models.ManyToManyField(User, through='AcceptedRequest', related_name='items')

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('item-detail', kwargs={'pk': self.pk})


class AcceptedRequest(models.Model):
	student = models.ForeignKey(User, on_delete=models.CASCADE)
	item = models.ForeignKey(Item, on_delete=models.CASCADE)
	date_issued = models.DateTimeField(auto_now=True, null=True)
	history = HistoricalRecords()
	remarks = models.TextField(blank=True, null=True)
	_history_date = None

	@property
	def _history_date(self):
		return self.__history_date

	@_history_date.setter
	def _history_date(self, value):
		self.__history_date = value
	

	PENDING = 1
	ACCEPT = 2
	DECLINE = 3
	REVERT = 4

	STATUS_CHOICES = (
		(PENDING, 'Pending'),
		(ACCEPT, 'Accepted'),
		(DECLINE, 'Declined'),
		(REVERT, 'Reverted')
		)

	status = models.IntegerField(
				choices=STATUS_CHOICES,
				default=PENDING,
		)

	def __str__(self):
		return str(self.student.username) + '|' + str(self.item.name) + '|' + str(self.status) + '|' + str(self.remarks)