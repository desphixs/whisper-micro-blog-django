# We import the admin module from django.contrib to configure how our models look and behave in Django's built-in administration panel.
from django.contrib import admin
# We import our Message model from the local models file so we can register it.
from feed.models import Message

# ==============================================================================
# REAL-WORLD ANALOGY: The Admin Dashboard Registry
# ------------------------------------------------------------------------------
# Imagine the Django Admin Panel is the VIP Management Office of our community forum.
# It has a massive dashboard screen where moderators and admins can manage the database tables.
# By default, this office doesn't know our custom "Message" table exists, so it doesn't display it.
#
# Registering the Message model in this file is like hanging a directory sign inside the
# VIP office that reads: "Message Management Desk". Once registered, administrators can
# walk up to the desk, browse all posted messages, edit them if needed, or delete unwanted posts.
# ==============================================================================

# We register our Message model with the admin site.
# This registers the Message database table directly in Django's built-in Admin panel dashboard.
admin.site.register(Message)
