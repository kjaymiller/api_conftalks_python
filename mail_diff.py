diff --git a/mail.py b/mail.py
index abac898..afe02af 100644
--- a/mail.py
+++ b/mail.py
@@ -1,10 +1,24 @@
 from markdown import markdown
+from jinja2 import Template
+from pathlib import Path
 
 import requests
 import os
 import re
 from dataclasses import dataclass, field
 
+
+def email_templates(filename, markdown='.md', text='.txt'):
+    templates = {} 
+    for extension in (markdown, text)
+        file_path = Path(f"{os['MAIL_TEMPLATES_DIR']}/{filename}{extension}")
+        if file_path.isfile():
+            templates[extension] = (file_path.read())
+        )
+
+    return templates
+
+
 @dataclass
 class mailGunEmailData:
     to: str
@@ -35,7 +49,6 @@ class mailGunEmailData:
                 data=self.mail_gun_email_data())
                 
 
-
 # Authentication
 def send_confirmation_email(to, api_key):
     subject = 'Welcome to Conftalks - Your Conftalks API Key'
@@ -57,25 +70,22 @@ def send_confirmation_email(to, api_key):
             ).sendMessage().url)
 
 
-def send_reset_key_email(to, reset_key):
+def send_reset_key_email(to, conference, event, reminder):
     subject = 'Reset your api key - Conftalks.dev' 
-    with open('./email_templates/reset_key_request_email.md') as md_file:
-        raw_markdown = md_file.read()
-        md_email = re.sub(r'{{EXPIRATION}}', reset_key['expiration'], raw_markdown)
-        md_email = re.sub(r'{{RESET_LINK}}', os.environ['RESET_LINK'], md_email)
-        md_email = re.sub(r'{{AUTHORIZATION_KEY}}', reset_key['key'], md_email)
-        html = markdown(md_email)
-
-    with open('./email_templates/reset_key_request_email.txt') as txt_email:
-        raw_text = txt_email.read()
-        text = re.sub(r'{{EXPIRATION}}', reset_key['expiration'], raw_text)
-        text = re.sub(r'{{RESET_LINK}}', os.environ['RESET_LINK'], text)
-        text = re.sub(r'{{AUTHORIZATION_KEY}}', reset_key['key'], text)
+    emails = {}
+    
+    for base_template in email_templates('email_notification'):
+        template = Template(base_template['base_template']) 
+        emails[base_template] = template.render(
+                conference=conference,
+                event=event, 
+                reminder=reminder,
+                )
 
-    print(mailGunEmailData( 
+    return mailGunEmailData( 
             to=to,
             subject=subject,
-            text=text,
-            html=html,
-            tags=['api_key', 'reset', 'confirmation'],
+            text=emails['.txt'],
+            html=Markdown(emails['.md']),
+            tags=['reminder', 'event'],
             ).sendMessage())
