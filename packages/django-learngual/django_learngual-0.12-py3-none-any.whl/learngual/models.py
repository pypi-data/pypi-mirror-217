import time
from typing import Any
from uuid import uuid4

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.gis.geoip2 import GeoIP2
from django.contrib.postgres.fields import ArrayField
from django.core.cache import cache
from django.db import models, transaction
from django.db.models import Q
from django.http.request import HttpRequest
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from geoip2.errors import AddressNotFoundError
from pydantic import BaseModel
from rest_framework_simplejwt.tokens import RefreshToken

from iam_service.accounts.manager import AccountManager
from iam_service.utilities import choices, utils
from iam_service.utilities.interfaces import PayableInterface
from iam_service.utilities.jwt_utils import decode_jwt_access_token
from iam_service.utilities.model_utils import BaseModelMixin, get_field_null_kargs

User = get_user_model()


class PersonnalMetadata(BaseModel):
    ...


class InstrctorMetadata(BaseModel):
    phone_number: str
    purpose: str


class EnterpriseMetadata(BaseModel):
    organization_name: str
    organization_type: str
    location: str
    company_url: str
    company_phone_number: str


class DeveloperMetadata(EnterpriseMetadata):
    purpose: str


def default_duration():
    return timezone.timedelta(seconds=0)


def profile_picture_default():
    return dict(
        url="https://learngual-bucket.sfo3.cdn.digitaloceanspaces.com/static/default-avatar.png",
        mimetype="image/png",
    )


class Account(PayableInterface, BaseModelMixin):
    objects: AccountManager.AccountQuerySet = AccountManager.AccountManager()
    owner = models.ForeignKey(User, verbose_name=_("owner"), on_delete=models.CASCADE)
    payment_fields = models.JSONField(_("payment_fields"), default=dict, blank=True)
    cover_photo = models.JSONField(_("cover_photo"), default=dict, blank=True)
    profile_photo = models.JSONField(
        _("profile_photo"), default=profile_picture_default, blank=True
    )
    type: choices.AccountType = models.CharField(
        _("type"),
        choices=choices.AccountType.choices,
        default=choices.AccountType.PERSONAL,
        max_length=50,
    )
    display_name = models.CharField(
        _("display name"), max_length=255, **get_field_null_kargs()
    )
    _metadata = models.JSONField(_("metdata"), default=dict)

    session_id = models.CharField(
        _("session_id"), max_length=225, **get_field_null_kargs()
    )

    analytics = models.JSONField(_("analytics"), default=dict, null=True, blank=True)
    activate_alert = models.BooleanField(_("activate_alert"), default=bool)
    first_timer = models.DateTimeField(_("first timer visit"), null=True, blank=True)
    used = models.BooleanField(_("used"), default=True, blank=True)

    @classmethod
    def get_metamodel(self, type):
        meta = {
            choices.AccountType.DEVELOPER.value: DeveloperMetadata,
            choices.AccountType.PERSONAL.value: PersonnalMetadata,
            choices.AccountType.ENTERPRISE.value: EnterpriseMetadata,
            choices.AccountType.INSTRUCTOR.value: InstrctorMetadata,
        }
        return meta.get(type, PersonnalMetadata)

    @property
    def metamodel(self):
        return self.get_metamodel(self.type)

    @property
    def metadata(
        self,
    ) -> (
        DeveloperMetadata | PersonnalMetadata | EnterpriseMetadata | InstrctorMetadata
    ):
        data = {}
        if self.type == choices.AccountType.DEVELOPER:
            data = {
                "organization_name": "demo",
                "organization_type": "demo",
                "location": "demo",
                "company_url": "demo",
                "company_phone_number": "demo",
                "purpose": "demo",
                **self._metadata,
            }
        elif self.type == choices.AccountType.ENTERPRISE:
            data = {
                "organization_name": "demo",
                "organization_type": "demo",
                "location": "demo",
                "company_url": "demo",
                "company_phone_number": "demo",
                **self._metadata,
            }
        elif self.type == choices.AccountType.INSTRUCTOR:
            data = {"phone_number": "demo", "purpose": "demo", **self._metadata}
        else:
            data = self._metadata

        return self.metamodel(**data)

    @metadata.setter
    def metadata(self, value: dict[str, Any]):
        Metadata = self.metamodel
        metadata: (
            DeveloperMetadata
            | PersonnalMetadata
            | EnterpriseMetadata
            | InstrctorMetadata
        ) = Metadata(**{**self._metadata, **value})
        self._metadata = metadata.dict()

    def get_receipt_item_data(self, *, product_id, **kwargs):

        return dict(
            id=product_id,
            name=f"upgrate account to {self.type.lower()} account",
            description=f"upgrate account to {self.type.lower()} account",
            quantity=1,
            callback_event="iam.accounts.payment_completed",
            callback_routing_key="iam.accounts.payment_completed",
            permission_data={
                "update_event": "iam.update_permission",
                "id": self.permission.id,
            },
            metadata=dict(
                model=self.__class__.__name__,
                id=self.id,
                **kwargs,
            ),
        )

    send_delete_request = models.BooleanField(_("send delete request"), default=False)
    send_delete_datetime = models.DateTimeField(
        _("send delete datetime"), null=True, blank=True
    )

    def task_delete_account(self):
        from iam_service.utilities.model_utils import TaskManager

        return TaskManager(
            self,
            "request_delete_account",
            task="iam_service.account.tasks.request_delete_account",
            args=(self.id,),
        )

    @transaction.atomic
    def request_delete_account(self):
        delete_date = timezone.now() + timezone.timedelta(days=30)
        task = self.task_delete_account()
        self.send_delete_request = True
        self.send_delete_datetime = delete_date
        self.save(update_fields=["send_delete_request", "send_delete_datetime"])
        task.create_clocked_task(datetime=delete_date)
        # return delete_date.isoformat()
        return delete_date

    @transaction.atomic
    def cancel_delete_account(self):
        task = self.task_delete_account()
        self.send_delete_request = False
        self.send_delete_datetime = None
        self.save(update_fields=["send_delete_request", "send_delete_datetime"])
        task.destroy_task()

    @classmethod
    def create_free_personal_account(cls, user: User):
        cls.objects.get_or_create(owner=user)

    @classmethod
    def get_api_key(cls, request):
        if request:
            api_key = str(
                request.META.get("HTTP_API_KEY", "") or request.GET.get("api-key", "")
            )

            return api_key

    @classmethod
    def get_api(cls, request):
        if request:
            api_key = str(
                request.META.get("HTTP_API_KEY", "") or request.GET.get("api-key", "")
            )
            if api_key:
                return ApiKey.objects.filter(key=api_key).first()

    @property
    def permission(self):
        permission = self.permission_set.first()
        if permission:
            return permission
        else:
            return Permission.objects.create(account=self)


class ApiKey(BaseModelMixin):
    account = models.ForeignKey(
        "accounts.Account", verbose_name=_("account"), on_delete=models.CASCADE
    )
    name = models.CharField(_("name"), max_length=255)
    language = models.CharField(_("language"), max_length=255, default="--none--")
    key = models.CharField(
        _("key"), max_length=255, default=utils.generate_api_key, unique=True
    )
    status: choices.ApiStatus = models.CharField(
        _("status"),
        choices=choices.ApiStatus.choices,
        default=choices.ApiStatus.ACTIVE,
        max_length=50,
    )
    limit = models.IntegerField(_("limit"), default=10, blank=True, null=True)
    remaining_calls = models.IntegerField(
        _("remaining_calls"), default=10, blank=True, null=True
    )
    enable_limit = models.BooleanField(_("enable limit"), default=bool)
    _activities = models.JSONField(_("activites"), default=list)

    @property
    def activities(self):
        return self.activities

    @activities.setter
    def activities(self, value):
        self._activities.append(value)


class DeviceInfo(BaseModel):
    device: str
    location: str
    ip_address: str
    timezone: str

    @staticmethod
    def device_id_default():
        return uuid4().hex


class ConnectedDevice(BaseModelMixin):
    user = models.ForeignKey(User, verbose_name=_("user"), on_delete=models.CASCADE)
    device = models.CharField(_("device"), max_length=255, null=True, blank=True)
    device_id = models.CharField(
        _("device id"), max_length=255, default=DeviceInfo.device_id_default
    )
    last_connected_date = models.DateTimeField(
        _("last connected"), default=timezone.now
    )
    location = models.CharField(_("location"), max_length=255, null=True, blank=True)
    ip_address = models.CharField(
        _("ip address"), max_length=255, null=True, blank=True
    )
    status: choices.ConnectedDeviceStatus = models.CharField(
        _("status"),
        choices=choices.ConnectedDeviceStatus.choices,
        default=choices.ConnectedDeviceStatus.PENDING,
        max_length=50,
    )
    token = models.TextField(_("token"), null=True, blank=True)
    access_token_data = models.JSONField(_("access token data"), default=dict)
    timezone = models.CharField(_("timezone"), max_length=225, null=True, blank=True)

    class Meta:
        ordering = ["-last_connected_date"]

    @staticmethod
    def get_client_ip(request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip

    @staticmethod
    def get_client_timezone(request):
        try:
            tz = request.META.get("HTTP_TZ") or request.GET.get("_tz")
            if tz:
                return tz
            x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
            if x_forwarded_for:
                ip = x_forwarded_for.split(",")[0]
            else:
                ip = request.META.get("REMOTE_ADDR")
            g = GeoIP2()
            return g.city(ip).get("time_zone")
        except AddressNotFoundError:
            return time.tzname[time.localtime().tm_isdst] or settings.TIME_ZONE

    @staticmethod
    def get_location_ip(ip):
        g = GeoIP2()
        location = "unknown"
        try:
            if ip:
                address = g.city(ip)
                city = address["city"]
                country = address["country_name"]
                location = f"{city}, {country}"
        except AddressNotFoundError:
            ...
        return location

    @classmethod
    def extract_connected_device_info(cls, request: HttpRequest) -> DeviceInfo:
        # print("meta ",request.META)
        # device = request.META.get("HTTP_USER_AGENT")
        # https://github.com/selwin/django-user_agents
        browser = request.user_agent.browser.family
        browser_version = request.user_agent.browser.version_string
        operation_system = request.user_agent.os.family
        device = f"{browser} V{browser_version} ({operation_system})"

        ip_address = cls.get_client_ip(request)
        location = cls.get_location_ip(ip_address)
        timezone_str = (
            request.META.get("HTTP_TZ")
            or request.GET.get("_tz")
            or cls.get_client_timezone(request)
        )
        data = dict(
            device=device,
            location=location,
            ip_address=ip_address,
            timezone=timezone_str,
        )
        return DeviceInfo(**data)

    def notify_new_dev_connected(self):
        ...

    @classmethod
    def update_or_create(cls, *, request, user, device_id, refresh, access):
        access_token_data = decode_jwt_access_token(access)
        access_token_data["exp"] = max(
            [access_token_data.get("exp").total_seconds(), 0]
        )
        data = cls.extract_connected_device_info(request)
        connected_device = cls.objects.filter(
            Q(user=user, device_id=device_id)
            | Q(user=user, ip_address=data.ip_address, ip_address__isnull=False)
        ).first()
        if connected_device:
            connected_device.__dict__.update(data.dict())
            connected_device.token = refresh
            connected_device.last_connected_date = timezone.now()
            connected_device.access_token_data = (access_token_data,)
            connected_device.save()
            return connected_device, False
        else:
            connected_device = cls.objects.create(
                user=user,
                device_id=device_id,
                last_connected_date=timezone.now(),
                token=refresh,
                access_token_data=access_token_data,
                **data.dict(),
            )
            return connected_device, True

    def delete(self, *args, **kwargs):
        self.blacklist_token()
        return super().delete(*args, **kwargs)

    def blacklist_token(self):

        try:
            # Attempt to decode the token to get the token ID
            assert self.token, "token does not exists"
            token = RefreshToken(self.token)
            token.blacklist()
            jti = self.access_token_data.get("jti")
            total_seconds = self.access_token_data.get("exp")
            cache.set(jti, "blacklist token", timeout=total_seconds)
        except Exception as e:
            print(e)
            # If decoding fails, the token is invalid
            return False

        return True


class FriendRequest(BaseModelMixin):
    sender = models.ForeignKey(
        "accounts.Account",
        verbose_name=_("sender"),
        related_name="send_friend_requests",
        on_delete=models.CASCADE,
    )
    receiver = models.ForeignKey(
        "accounts.Account",
        verbose_name=_("receiver"),
        related_name="receieved_friend_requests",
        on_delete=models.CASCADE,
    )
    status: choices.FriendRequestStatus = models.CharField(
        _("status"),
        choices=choices.FriendRequestStatus.choices,
        default=choices.FriendRequestStatus.PENDING,
        max_length=50,
    )


class Permission(BaseModelMixin):
    owner = models.ForeignKey(
        User, verbose_name=_("owner"), on_delete=models.SET_NULL, null=True, blank=True
    )
    account = models.ForeignKey(
        "Account",
        verbose_name=_("account"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    name = models.CharField(_("name"), max_length=255, default=str, blank=True)
    url_regexs = ArrayField(
        base_field=models.CharField(
            _("url regex"), max_length=255, default="*", blank=True
        ),
        default=list,
        blank=True,
    )
    request_methods = ArrayField(
        base_field=models.CharField(_("request methods"), default="*", max_length=255),
        default=list,
        blank=True,
    )
    roles = ArrayField(
        base_field=models.CharField(_("request methods"), max_length=255),
        default=list,
        blank=True,
    )
    metadata = models.JSONField(_("metadata"), default=dict, blank=True)
