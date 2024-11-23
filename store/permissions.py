from rest_framework.permissions import BasePermission, SAFE_METHODS, DjangoModelPermissions


class IsAdminOrReadOnly(BasePermission):
    
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True 
        return bool(request.user and request.user.is_staff)


# Applying custom permission, that defined in Customer model in class Meta
class ViewCustomerHistoryPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('store.view_history')
    


#  Higher level of permission control
class FullDjangoModelPermissions(DjangoModelPermissions):
    def __init__(self) -> None:
        self.perms_map['GET'] = ['%(app_label)s.view_%(model_name)s']
