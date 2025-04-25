import logging

from datetime import datetime, timedelta

from user import models
from user import constants as c

from django.db.models.signals import post_save
from django.dispatch import receiver

logger = logging.getLogger('user_signals')
