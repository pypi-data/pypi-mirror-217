# -*- coding: utf-8 -*-

# ****************************************************************
# IDE:          PyCharm
# Developed by: macercha
# Date:         10/04/23 13:52
# Project:      Django Plugins
# Module Name:  models
# Description:
# ****************************************************************
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from timezone_utils.choices import ALL_TIMEZONES_CHOICES
from zibanu.django.db import models


class UserProfile(models.Model):

    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name="profile",
                                related_query_name="user")
    timezone = models.CharField(max_length=50, null=False, blank=False, default="UTC",
                                choices=ALL_TIMEZONES_CHOICES, verbose_name=_("Time Zone"))
    theme = models.CharField(max_length=50, null=True, blank=False, verbose_name=_("User Theme"))
    lang = models.CharField(max_length=3, null=False, blank=False, default="en", verbose_name=_("Language"))
    avatar = models.BinaryField(null=True, blank=False, verbose_name=_("Avatar"))
    messages_timeout = models.IntegerField(default=10, null=False, blank=False, verbose_name=_("Message's Timeout"))
    keep_logged_in = models.BooleanField(default=False, null=False, blank=False, verbose_name=_("Keep Logged In"))
    app_profile = models.JSONField(null=True, blank=False, verbose_name=_("Custom Application Profile"))

    def set(self, fields: dict):
        """
        Change field values from a field dict list
        :param fields: dictionary with key, value for field
        :return: None
        """
        for key, value in fields.items():
            if hasattr(self, key):
                setattr(self, key, value)
            self.save(force_update=True)


    class Meta:
        db_table = "zb_auth_user_profile"
