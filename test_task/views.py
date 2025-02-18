from .views.auth_views import (
    UserRegisterHTMLView,
    UserLoginHTMLView,
    UserLogoutView,
    PasswordChangeView,
    CustomPasswordChangeView
)
from .views.collection_views import (
    CollectionListView,
    CollectionCreateView,
    CollectionUpdateView,
    CollectionDeleteView,
    CollectionRemoveLinkView
)
from .views.link_views import (
    LinkListView,
    LinkCreateView,
    LinkUpdateView,
    LinkDeleteView
)
from .views.home_views import HomeView

__all__ = [
    'UserRegisterHTMLView',
    'UserLoginHTMLView',
    'UserLogoutView',
    'PasswordChangeView',
    'CustomPasswordChangeView',
    'CollectionListView',
    'CollectionCreateView',
    'CollectionUpdateView',
    'CollectionDeleteView',
    'CollectionRemoveLinkView',
    'LinkListView',
    'LinkCreateView',
    'LinkUpdateView',
    'LinkDeleteView',
    'HomeView'
]