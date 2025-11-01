from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
import json

@login_required
@require_http_methods(["POST"])
def save_push_subscription(request):
    """ذخیره subscription کاربر برای Push Notifications"""
    try:
        data = json.loads(request.body)
        subscription = data.get('subscription')
        
        # ذخیره subscription در پروفایل کاربر
        # اینجا می‌توانید subscription را در دیتابیس ذخیره کنید
        request.user.profile.push_subscription = json.dumps(subscription)
        request.user.profile.save()
        
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})

@login_required
def pwa_manifest(request):
    """برگرداندن manifest پویا"""
    manifest = {
        "name": "Team Workspace",
        "short_name": "Workspace", 
        "description": "سیستم مدیریت پروژه تیمی",
        "lang": "fa",
        "dir": "rtl",
        "theme_color": "#2563eb",
        "background_color": "#ffffff",
        "display": "standalone",
        "scope": "/",
        "start_url": "/",
        "icons": [
            {
                "src": "/static/icons/icon-192x192.png",
                "sizes": "192x192",
                "type": "image/png"
            },
            {
                "src": "/static/icons/icon-512x512.png", 
                "sizes": "512x512",
                "type": "image/png"
            }
        ]
    }
    return JsonResponse(manifest)
