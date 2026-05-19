# We import models from django.db so that we can build database tables using Django's pre-made field blocks.
from django.db import models
# We import our custom User model from the 'accounts' app because we need to link our messages to the actual registered users who write them.
from accounts.models import User

# ==============================================================================
# REAL-WORLD ANALOGY: The Message Bulletin Board and Sticky Notes
# ------------------------------------------------------------------------------
# Imagine you are setting up a physical wooden bulletin board in a community cafe.
# This bulletin board represents our database table for messages.
#
# Each sticky note pinned to this board represents a single "Message" object in our code.
# For a sticky note to be useful, it needs three specific things written on it:
# 1. The main message text itself (our content field).
# 2. A stamped date and time showing exactly when it was pinned up (our created_at field).
# 3. The name and signature of the person who wrote the note, so we know who it belongs to (our author field).
#
# If a person (User) leaves the cafe permanently (is deleted from the system), we don't
# want their old sticky notes hanging around creating clutter. So we tell our board to 
# automatically tear down and throw away all notes written by that person (CASCADE deletion).
# ==============================================================================

# We create our Message class, which inherits from models.Model.
# This inheritance tells Django: "Hey, turn this Python class into a real database table!"
class Message(models.Model):
    # We define 'content' as a TextField to hold the text of the message.
    # Analogy: A TextField is like a large, lined sheet of paper. Unlike a small index card
    # that only holds a few characters, a TextField allows users to write as much text as they want.
    content = models.TextField()

    # We define 'created_at' as a DateTimeField that automatically captures the creation time.
    # By setting 'auto_now_add=True', Django acts like a digital date-stamp machine.
    # The absolute split-second a new note is created, Django stamps the current date and time on it
    # and locks it in so it can never be changed or forged.
    created_at = models.DateTimeField(auto_now_add=True)

    # We define 'author' as a ForeignKey pointing to the User model we imported.
    # A ForeignKey represents a "One-to-Many" relationship: One User can write Many Messages,
    # but each individual Message has exactly One Author who wrote it.
    #
    # We set 'on_delete=models.CASCADE'. 
    # Analogy: This is the "Waterfall Cleanup Rule". If a user account is deleted from the system,
    # Django will automatically trigger a chain reaction that deletes all messages written by that user.
    # This prevents "orphan data"—messages in our database that point to an author who no longer exists.
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    # The __str__ method is a special Python method that tells Django how to display this object in the admin dashboard.
    # Instead of showing a generic text like "Message object (1)", it will display the author's email and a preview of the content.
    # Analogy: This is like writing a quick summary tag on the back of each sticky note so a librarian can see what it is at a glance.
    def __str__(self):
        # We return the author's email and the first 30 characters of the content so it is easy to read in the admin panel.
        return f"{self.author.email} - {self.content[:30]}"
