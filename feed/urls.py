# We import path from django.urls to register specific URL routes for our feed views.
from django.urls import path
# We import our views file from the current directory to link paths to our view functions.
from feed import views

# ==============================================================================
# REAL-WORLD ANALOGY: The Sub-Department Signposts
# ------------------------------------------------------------------------------
# Imagine the main Django project's urls.py is the giant signpost at the entrance 
# of a major shopping mall. 
# 
# Instead of listing every single item in the feed section right at the front 
# entrance (which would look cluttered and messy), the main entrance signpost simply 
# points to the "Feed Department" wing.
# 
# Creating this local `feed/urls.py` file is like setting up a dedicated, clean
# signpost *inside* the Feed Department wing, pointing shoppers specifically to
# the "Timeline" bulletin board (`/timeline/`).
# ==============================================================================

# We define the list of URL patterns that are active inside our feed app.
urlpatterns = [
    # We map the URL root path '' directly to our protected timeline_view function.
    # We give it the name 'index' to serve as our central homepage, so we can refer to it easily
    # in HTML templates or redirect statements using {% url 'index' %}.
    path('', views.timeline_view, name='index'),

    # We map the URL path 'edit/<int:id>/' directly to our protected edit_message view function.
    # Analogy: This is like assigning a dynamic mailbox extension key.
    # - '<int:id>' tells Django that this segment of the URL holds a dynamic integer number
    #   representing the message's primary key ID in the database.
    # - We name the pattern 'edit_message' so that templates and views can programmatically 
    #   construct URLs (like reversing or resolving {% url 'edit_message' message.id %}) safely.
    path('edit/<int:id>/', views.edit_message, name='edit_message'),

    # We map the URL path 'delete/<int:id>/' directly to our protected delete_message view function.
    # Analogy: Setting up a dynamic directory button in our mall signpost pointing to the secure shredder room.
    # - '<int:id>' represents the dynamic primary key integer ID of the specific whisper to shred.
    # - We nickname this route 'delete_message' so that our template buttons can link back here easily.
    path('delete/<int:id>/', views.delete_message, name='delete_message'),
]
