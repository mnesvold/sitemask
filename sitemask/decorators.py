from django.shortcuts import render

from .masks import get_active_mask

def maskable(view):
    def wrapped_view(request, *args, **kwargs):
        active_mask = get_active_mask()
        if active_mask is not None:
            return render(request, 'sitemask/mask.html', {
                'title': active_mask.title,
                'subtitle': active_mask.subtitle,
                'image_url': active_mask.image_url,
            })
        return view(request, *args, **kwargs)
    return wrapped_view
