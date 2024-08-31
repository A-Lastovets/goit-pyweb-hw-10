from django.core.management.base import BaseCommand
from pymongo import MongoClient
from quotes.models import Author, Quote
from dotenv import load_dotenv
import os
from django.utils import timezone
from datetime import datetime
from bson import ObjectId

load_dotenv()

db_password = os.getenv('DB_PASSWORD')

class Command(BaseCommand):
    help = 'Migrate data from MongoDB to PostgreSQL'

    def handle(self, *args, **kwargs):
        # Підключення до MongoDB
        client = MongoClient(f'mongodb+srv://alastovets:{db_password}@clustera.jq75x.mongodb.net/')
        db = client.test

        authors = db.author.find()
        quotes = db.quote.find()

        # Міграція авторів
        for author in authors:
            born_date = author.get('born_date')
            if born_date:
                try:
                    if isinstance(born_date, str):
                        formats = ['%Y-%m-%d', '%B %d, %Y', '%d-%m-%Y', '%Y/%m/%d']
                        for fmt in formats:
                            try:
                                naive_date = datetime.strptime(born_date, fmt)
                                born_date = timezone.make_aware(naive_date, timezone.get_current_timezone())
                                break
                            except ValueError:
                                continue
                        else:
                            self.stdout.write(self.style.WARNING(f"Invalid date format for author {author.get('fullname')}: {born_date}"))
                            born_date = None
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Error processing date for author {author.get('fullname')}: {e}"))
                    born_date = None

            new_author = Author(
                id=str(author['_id']),
                fullname=author.get('fullname'),
                born_date=born_date,
                born_location=author.get('born_location'),
                description=author.get('description'),
            )
            new_author.save()

        # Міграція цитат
        for quote in quotes:
            try:
                # Перевірте і отримайте поле 'text' або 'quote' для тексту цитати
                text = quote.get('quote')  # MongoDB поле для тексту цитати
                if not text:
                    self.stdout.write(self.style.WARNING(f"Missing 'quote' field in MongoDB document: {quote}"))
                    continue

                # Конвертуйте MongoDB ObjectId в рядковий формат
                author_id = str(ObjectId(quote['author']))  # Якщо автори у MongoDB мають ObjectId
                author = Author.objects.get(id=author_id)

                new_quote = Quote(text=text, author=author)
                new_quote.save()
                self.stdout.write(self.style.SUCCESS(f"Quote '{text}' added successfully."))
            except Author.DoesNotExist:
                self.stdout.write(self.style.WARNING(f"Author '{quote['author']}' does not exist. Skipping quote."))
            except KeyError as e:
                self.stdout.write(self.style.ERROR(f"Missing field {e} in quote: {quote}"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error processing quote: {e}"))

        self.stdout.write(self.style.SUCCESS('Data successfully migrated from MongoDB to PostgreSQL'))
