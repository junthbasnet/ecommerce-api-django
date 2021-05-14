JAZZMIN_SETTINGS = {
    # title of the window
    "site_title": "Nebuyo Admin",

    # Title on the brand, and the login screen (19 chars max)
    "site_header": "Nebuyo",

    # Welcome text on the login screen
    "welcome_sign": "Welcome to the Nebuyo Admin",

    # Copyright on the footer
    "copyright": "Kagati Incorporation",

    # Field name on user model that contains avatar image
    'user_avatar': None,

    ############
    # Top Menu #
    ############

    # Links to put along the top menu
        'topmenu_links': [
                             # Url that gets reversed (Permissions can be added)
                             {'name': 'Home', 'url': 'admin:index',
                              'permissions': ['auth.view_user']},

                             # model admin to link to (Permissions checked against model)
                             {'model': 'users.User'},
                             {'app': 'products'},
                             {'app': 'core'},
                             # App with dropdown menu to all its models pages (Permissions checked against models)

                         ],

                         #############
                         # User Menu #
                         #############

                         # # Additional links to include in the user menu on the top right ('app' url type is not allowed)
                         # 'usermenu_links': [
                         #     {'model': 'auth.user'},
                         #     {'name': 'Support', 'url': 'https://ajaykarki.github.io',
                         #         'new_window': True},
                         # ],

                         #############
                         # Side Menu #
                         #############

                         # Whether to display the side menu
                         'show_sidebar': True,

# Whether to aut expand the menu
'navigation_expanded': True,

# Hide these apps when generating side menu e.g (auth)
'hide_apps': [],

# Hide these models when generating side menu (e.g auth.user)
'hide_models': [],

# List of apps to base side menu ordering off of (does not need to contain all apps)
# 'order_with_respect_to': ['accounts', 'polls'],

# Custom links to append to app groups, keyed on app name

# Custom icons for side menu apps/models See https://www.fontawesomecheatsheet.com/font-awesome-cheatsheet-5x/
# for a list of icon classes
'icons': {
    'auth': 'fas fa-users-cog',
    'auth.user': 'fas fa-user',
    'auth.Group': 'fas fa-users',
},
# 'custom_css': 'css/admin.css',
#  "show_ui_builder": True,

}

JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": "navbar-dark",
    "accent": "accent-primary",
    "navbar": "navbar-danger navbar-dark",
    "no_navbar_border": False,
    "sidebar": "sidebar-dark-danger",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": False,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False
}
