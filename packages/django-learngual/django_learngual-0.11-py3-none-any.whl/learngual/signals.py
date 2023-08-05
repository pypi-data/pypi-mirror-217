from django.db.models import signals
from django.dispatch import receiver

from iam_service.accounts import tasks
from iam_service.accounts.models import Permission
from iam_service.accounts.signals_event import AccountEvent
from iam_service.users import tasks as users_tasks

# Account


@receiver(signals.post_save, sender="accounts.Account")
def on_account_postsave(sender, instance, created, *args, **kwargs):

    if created:
        tasks.on_account_created.delay(instance.id)
    else:
        tasks.on_account_updated.delay(instance.id)


# @receiver(signals.pre_save,sender='accounts.Account')
# def on_account_presave(sender,instance,*args, **kwargs):
#     print("transaction pre save")


# @receiver(signals.pre_init,sender='accounts.Account')
# def on_account_pre_init(sender,instance,*args, **kwargs):
#     print("transaction init")

# @receiver(signals.post_init,sender='accounts.Account')
# def on_account_post_init(sender,instance,*args, **kwargs):
#     print("post init")

# @receiver(signals.pre_delete,sender='accounts.Account')
# def on_account_pre_delete(sender,instance,*args, **kwargs):
#     pass


@receiver(signals.post_delete, sender="accounts.Account")
def on_account_post_delete(sender, instance, *args, **kwargs):
    tasks.on_account_deleted.delay(instance.id)


@receiver(AccountEvent.account_subscription_expire, sender="accounts.Account")
def on_account_subscription_expire(sender, instance, *args, **kwargs):
    tasks.on_account_subscription_expire.delay(instance.id)


@receiver(AccountEvent.new_account_subscription, sender="accounts.Account")
def on_new_account_subscription(sender, instance, *args, **kwargs):
    tasks.on_new_account_subscription.delay(instance.id)


@receiver(AccountEvent.new_friend_request, sender="accounts.FriendRequest")
def on_new_friend_request(sender, instance, *args, **kwargs):
    tasks.on_new_friend_request.delay(instance.id)


@receiver(signals.post_save, sender="accounts.Permission")
def on_permission_postsave(sender, instance: Permission, created, *args, **kwargs):
    if instance.account:
        tasks.on_account_updated.delay(instance.account.id)
    if instance.owner:
        users_tasks.on_user_updated.delay(instance.owner.id)
