from fastapi.responses import RedirectResponse

def require_admin(request):
    user = request.session.get("user")

    if not user or user["role"] != "admin":
        return RedirectResponse("/")