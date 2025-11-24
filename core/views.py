from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.views.decorators.csrf import ensure_csrf_cookie
import sqlite3
import os
import re

# Create your views here.
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATABASE_PATH = os.path.join(BASE_DIR, "db.sqlite3")

@ensure_csrf_cookie
def index(request):
    return render(request, "index.html")

#def basicSanitation(string):

def add_comment(request):
    if request.method != "POST":
       return HttpResponse("Bad Method );", status=405)
    if settings.VULNERABLE:
       username = request.POST.get("username", "").strip()
       comment = request.POST.get("comment", "").strip()
       connection_db = sqlite3.connect(DATABASE_PATH)
       cursor = connection_db.cursor()
       try:
          cursor.execute("""
            CREATE TABLE IF NOT EXISTS Comments (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              username TEXT,
              comment TEXT,
              count INT
            )
          """)
          cursor.execute(f"SELECT COUNT(*) FROM Comments WHERE username = '{username}'")
          count = cursor.fetchone()[0]
          if count >= 3:
             connection_db.close()
             return HttpResponse("Oops! You've reached the maximum comment limit );")
          count += 1
          cursor.execute(f"""
            INSERT INTO Comments (username, comment, count)
            VALUES ('{username}', '{comment}', '{count}')
          """)
          connection_db.commit()
       finally:
              connection_db.close()
    else:
        from .models import Comment
        from . import models
        username = request.POST.get("username", "").strip()
        comment = request.POST.get("comment", "").strip()
        count = Comment.objects.filter(base_username=username).count()
        if count >= 3:
           return HttpResponse("Oops! You've reached the maximum comment limit );")
        username_count = f"{username} quantity:{count + 1}"
        Comment.objects.create(
          base_username=username,
          user_count=count,
          user_comment=comment
        )
    response = {
      "status": "success",
      "message": f"Success! Comment added",
      "username": username,
      "comment": comment
    }
    return JsonResponse(response)

def list_comments(request):
    if request.method != "GET":
       return JsonResponse({"status": "error", "message": "Bad method );"})
    if settings.VULNERABLE:
        db_connection = sqlite3.connect(DATABASE_PATH)
        db_cursor = db_connection.cursor()
        try:
            db_cursor.execute("SELECT username, comment FROM Comments")
            rows = db_cursor.fetchall()
            comments_response = [{"username": username, "comment": comment} for username, comment in rows]
            db_connection.close()
            return JsonResponse({"status": "success", "message": comments_response})
        except Exception as error:
            return JsonResponse({"status": "error", "message": f"no answer {error}"})
    else:
        from .models import Comment
        try:
            comments_qs = Comment.objects.values("base_username", "user_comment")
            payload = [{"username": q["base_username"], "comment": q["user_comment"]} for q in comments_qs]
            return JsonResponse({"status": "success", "message": payload})
        except Exception as error:
            return JsonResponse({"status": "error", "message": f"no answer: {error}"})
