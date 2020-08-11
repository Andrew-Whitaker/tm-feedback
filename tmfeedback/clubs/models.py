from django.db import models
from django.conf import settings
from django.urls import reverse
from datetime import date as dt_date
from datetime import timedelta


class Club(models.Model):
    name = models.CharField(max_length=100, unique=True)
    id = models.PositiveIntegerField(default=0, primary_key=True)
    description = models.TextField(max_length=1500, default='')
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='clubs')
    member_count = models.PositiveIntegerField(default=1)
    organizer = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='organizing',
                                  null=True, on_delete=models.SET_NULL)
    membership_requests = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='pending_clubs')

    def __str__(self):
        return self.name

    def has_member(self, user):
        return self.members.filter(pk=user.pk).exists()

    def has_pending_member(self, user):
        return self.membership_requests.filter(pk=user.pk).exists()

    def add_member(self, user):
        if not user.is_authenticated:
            raise RuntimeError('Attempting to add an unauthenticated User as a club member.')

        self.members.add(user)
        self.member_count += 1
        return

    def get_absolute_url(self):
        kwargs = {'club_id': self.id}
        return reverse('club_home', kwargs=kwargs)

    def get_meetings_in(self, month: int, year: int):
        """
        Return all the meetings of this club that have occurred in the specified month and year.

        :param month: Integer value between 1 and 12. January (1) .... December (12)
        :param year: Integer value including the millennium and century. Ex: 2018
        :return: Django Queryset of the list of Meetings.
        """
        month_str = str(month)
        year_str = str(year)
        meeting_query_set = self.meetings.filter(date__month=month_str, date__year=year_str)
        meeting_query_set = meeting_query_set.order_by('-date')
        return meeting_query_set

    def get_meetings_from_last_n_weeks(self, n: int, date=None):
        """
        Return all meetings of this club that have occurred in the last N weeks, including the current week.

        :param n: Positive non-zero integer.
        :param date: Date object from datetime. Leave blank if you want to use today's date.
        :return: Django Queryset of the list of Meetings.
        """
        if date is None:
            date = dt_date.today()

        n_weeks_delta = timedelta(weeks=n)
        start_date = date - n_weeks_delta

        start_date_str = dt_date.strftime(start_date, "%Y-%m-%d")
        end_date_str = dt_date.strftime(date, "%Y-%m-%d")
        meeting_query_set = self.meetings.filter(date__range=[start_date_str, end_date_str])
        meeting_query_set = meeting_query_set.order_by('-date')
        return meeting_query_set

    def get_roster(self):
        """
        Get the list of members in a club.

        :return: Django Queryset of the members in a club.
        """
        members = self.members.order_by('last_name')
        return members




