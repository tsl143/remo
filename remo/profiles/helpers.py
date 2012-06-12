import urlparse

from datetime import datetime, timedelta

from django.conf import settings
from funfactory.helpers import urlparams
from jingo import register

from libravatar import libravatar_url

from remo.profiles.models import UserAvatar


@register.filter
def get_avatar_url(user, size=50):
    """Get a url pointing to user's avatar.

    The libravatar network is used for avatars. Return cached value if
    its last update was less than 24 hours before. Optional argument
    size can be provided to set the avatar size.

    """
    if not user:
        return None

    default_img_url = reduce(lambda u, x: urlparse.urljoin(u, x),
                             [settings.SITE_URL,
                              settings.MEDIA_URL,
                              'img/remo/remo_avatar.png'])

    user_avatar, created = UserAvatar.objects.get_or_create(user=user)
    now = datetime.utcnow()
    if user_avatar.last_update < now - timedelta(hours=24):
        user_avatar.avatar_url = libravatar_url(email=user.email)
        user_avatar.last_update = now
        user_avatar.save()

    avatar_url = urlparams(user_avatar.avatar_url, default=default_img_url)
    if size != -1:
        avatar_url = urlparams(avatar_url, size=size)

    return avatar_url
