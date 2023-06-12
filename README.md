# Honyaku Assist

A webapp for comparing output from the DeepL and Google Translate machine translation engines.<br>
(Useful for tired translators needing some inspiration.)

- Retrieves translation results from the DeepL and Google Translate APIs.
- Keeps track of monthly usage relative to the free tier limits offered through these APIs<br>
  (both APIs have monthly limits of 500,000 characters).
- Results are displayed on the same page using HTMX for partial page reloads.

### Built using:

* Python 3.10
* Django 4.1.3
* Bootstrap 5
* HTMX
* Docker
* Gunicorn
* Nginx
* PostgreSQL

### Example:

https://github.com/4ka0/honyaku_assist/assets/39420293/9b6cebab-6cd7-45eb-9d5f-a0ff58154959
