from django.shortcuts import render, redirect, get_object_or_404
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
    timeline_view handles displaying all the secret whispers shared by our community members,
    and also processes new whisper submissions (via POST).
    
    Analogy: Imagine a central community physical bulletin board.
    When a user walks up to it (GET request), we show them all pinned notes.
    When a user writes a new note and pins it (POST request), we accept the paper,
    stamp their signature onto it, pin it to the board, and refresh their perspective.
    """
    
    # 1. Checking if the visitor is submitting data to the server.
    # request.method tells us the HTTP method. 'POST' means the user filled out our form and clicked submit!
    # Analogy: This is checking if the visitor brought a package to post on our bulletin board (POST),
    # rather than just walking up to read the existing notes (GET).
    if request.method == 'POST':
        
        # 2. Extract the message text directly from the form submission data.
        # request.POST is like a mailbox package containing all form input values by name.
        # We retrieve the content text using the name key 'content' matching our HTML textarea.
        # .strip() removes any accidental leading or trailing blank spaces typed by the user.
        content = request.POST.get('content', '').strip()
        
        # 3. Validation: Verify that the message is not blank.
        # Analogy: We want to make sure the user wrote something real and didn't just submit an empty sheet of paper!
        if content:
            
            # 4. Create and save the new message to the database.
            # We call the 'create' method on our Message model objects manager.
            # - content=content: Store the text we grabbed from the textarea.
            # - author=request.user: Permanently link this message to the logged-in user.
            # Analogy: This is like creating a brand new paper card, writing the secret on it,
            # and stamping the author's real ID card directly to it so we know who published it.
            Message.objects.create(
                content=content,
                author=request.user
            )
            
            # 5. Redirect back to the timeline home page ('index').
            # Analogy: Instead of having the user stay stuck looking at a successful delivery page,
            # we spin them back around to the entrance of the bulletin board.
            # This is crucial because it clears the POST request from the browser's history,
            # so if they hit "Refresh", they don't submit the exact same post twice!
            return redirect('index')
            
    # 6. Fetching whispers from the database.
    # We use Django's Object-Relational Mapper (ORM) to run a database query.
    # Message.objects.all() tells Django: "Go to the 'Message' table and grab every single row."
    # .order_by('-created_at') tells Django to sort them.
    # The minus sign '-' represents DESCENDING order (newest first).
    # This is like arranging your email inbox so that the email received 1 minute ago sits on top,
    # rather than an email from 3 years ago!
    messages = Message.objects.all().order_by('-created_at')
    
    # 7. Packing the whispers into a container (context) to send to the template.
    # The context is a standard Python dictionary (key-value pairs).
    # It acts like a custom delivery box. We label the box 'messages' (the key),
    # and we place our actual database query results inside it (the value).
    # This labels the data so that our HTML template knows how to refer to it.
    context = {
        'messages': messages,
    }
    
    # 8. Rendering and delivering the page.
    # The 'render' helper takes:
    # - the incoming user's 'request' (the digital visitor),
    # - the name of the blueprint template ('index.html') to construct the visual layout,
    # - and our 'context' delivery box filled with the database messages.
    # Render compiles all of this into pure HTML and sends it back to the user's browser.
    return render(request, 'index.html', context)


# We apply the VIP security check bouncer (@login_required) so that only logged-in members can access the editor.
# If a guest tries to navigate here, the bouncer boots them back to the login gateway.
@login_required
def edit_message(request, id):
    """
    edit_message allows the true author of a whisper to load a secure editor form
    and save updates to their whisper content, while locking out anyone else.
    
    Analogy: The private safety deposit box.
    1. A member presents a specific box key (message ID).
    2. We verify if the signature on the bank account details matches the key holder (author validation).
    3. If they don't match, we sound the alarm and escort them out of the building (redirect back to feed).
    4. If they match, they can open the box, wipe the old sheet clean, write their new secrets,
       and seal the box back up in the vault (POST processing and saving).
    """
    
    # 1. Fetch the specific whisper from the database using our helper shortcut.
    # We tell Django: "Look inside the 'Message' table and grab the row matching 'id=id'."
    # If a user tries to edit a message ID that doesn't exist, Django handles it and returns a 404 error page.
    message = get_object_or_404(Message, id=id)
    
    # 2. Security Author Validation Check.
    # We compare the message author's user ID with the user currently active in the request session.
    # Analogy: A security guard comparing the ID badge of the person trying to edit the document
    # against the name listed as the original author. If they don't match, we deny entry!
    if message.author != request.user:
        # Immediately eject the unauthorized user and redirect them back to the home global timeline.
        return redirect('index')
        
    # 3. Handling incoming update submissions (POST request).
    # If the author filled out the form and clicked "Save Changes", request.method is equal to 'POST'.
    if request.method == 'POST':
        # Extract the new updated message text from the submission data using the key 'content'.
        # We run .strip() to clean up any blank spaces.
        new_content = request.POST.get('content', '').strip()
        
        # 4. Validation: Verify that the message is not empty.
        # We don't want the user to clear out their entire whisper and save a blank note!
        if new_content:
            # Overwrite the message's content field with the new text.
            # Analogy: Erasing the previous text on the whiteboard and writing the new polished sentence.
            message.content = new_content
            
            # Save the updated object state back into our database table rows.
            # Analogy: Locking the safety deposit box back in the wall so it is permanently stored.
            message.save()
            
            # 5. Redirect back to the timeline page so they can see their updated post.
            # This also clears the POST submit history so browser refreshes are safe!
            return redirect('index')
            
    # 6. Handling the GET request (displaying the form).
    # If the user simply clicked "Edit Whisper", it's a GET request.
    # We must load the edit template and pass our message context so the input textarea is pre-filled.
    # Analogy: We pack our message object into our custom context delivery box labeled 'message'.
    context = {
        'message': message,
    }
    
    # Render the edit template compile, passing our context, and return the visual HTML layout.
    return render(request, 'edit.html', context)

