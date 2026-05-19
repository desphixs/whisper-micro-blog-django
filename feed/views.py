from django.shortcuts import render
# We import the login_required decorator which acts like a VIP room security bouncer.
# It ensures that only logged-in (authenticated) users can gain access to our timeline page.
# If an anonymous user tries to sneak in, the bouncer will catch them and politely redirect them
# to the login gate.
from django.contrib.auth.decorators import login_required

# We import the Message database model from our current app's models file.
# The Message model is the blueprint/template that Django uses to store and retrieve whispers.
from feed.models import Message

# Create your views here.

# We apply the bouncer decorator (@login_required) directly above our timeline view function.
# Think of this decorator as a security checkpost installed at the entrance of a VIP lounge.
# Before anyone can enter and execute the code inside 'timeline_view', Django checks if they are logged in.
@login_required
def timeline_view(request):
    """
    timeline_view handles displaying all the secret whispers shared by our community members.
    
    Analogy: Imagine a central community physical bulletin board.
    When a user walks up to it (sends a GET request), we must:
    1. Go to the storage room (database) and gather all the written notes (messages).
    2. Sort them so the newest, freshest notes are pinned on top of the pile.
    3. Hand the stack of notes over to our designer (the HTML template) to style and display.
    """
    
    # 1. Fetching whispers from the database.
    # We use Django's Object-Relational Mapper (ORM) to run a database query.
    # Message.objects.all() tells Django: "Go to the 'Message' table and grab every single row."
    # .order_by('-created_at') tells Django to sort them.
    # The minus sign '-' represents DESCENDING order (newest first).
    # This is like arranging your email inbox so that the email received 1 minute ago sits on top,
    # rather than an email from 3 years ago!
    messages = Message.objects.all().order_by('-created_at')
    
    # 2. Packing the whispers into a container (context) to send to the template.
    # The context is a standard Python dictionary (key-value pairs).
    # It acts like a custom delivery box. We label the box 'messages' (the key),
    # and we place our actual database query results inside it (the value).
    # This labels the data so that our HTML template knows how to refer to it.
    context = {
        'messages': messages,
    }
    
    # 3. Rendering and delivering the page.
    # The 'render' helper takes:
    # - the incoming user's 'request' (the digital visitor),
    # - the name of the blueprint template ('index.html') to construct the visual layout,
    # - and our 'context' delivery box filled with the database messages.
    # Render compiles all of this into pure HTML and sends it back to the user's browser.
    return render(request, 'index.html', context)

