from .models import Notification

def unread_notifications_count_babysitter(request):
    if request.user.is_authenticated:
        return {
            'unread_notifications_count_babysitter': Notification.objects.filter(user=request.user, read=False).count()
        }
    return {'unread_notifications_count_babysitter': 0}
def unread_notifications_count_parent(request):
    if request.user.is_authenticated:
        return {
            'unread_notifications_count_parent': Notification.objects.filter(user=request.user, read=False).count()
        }
    return {'unread_notifications_count_parent': 0}