import os
from django.core.management.base import BaseCommand
from checker.models import Dictionary

class Command(BaseCommand):
    help = "TXT fayllardan so'zlarni bazaga yuklaydi"

    def handle(self, *args, **kwargs):
        # Fayllar joylashgan papka manzili
        data_dir = 'Data' 
        files = ["sport.txt", "education.txt", "economy.txt", "technology.txt"]
        
        words_to_create = []
        seen_words = set()

        for file_name in files:
            path = os.path.join(data_dir, file_name)
            if os.path.exists(path):
                self.stdout.write(f"{file_name} o'qilmoqda...")
                with open(path, 'r', encoding='utf-8') as f:
                    data = f.read().split()
                    for word in data:
                        clean_word = word.lower().strip('.,!?:;"()')
                        if clean_word and clean_word not in seen_words:
                            words_to_create.append(Dictionary(word=clean_word))
                            seen_words.add(clean_word)

        # Bazaga ommaviy yuklash (Tezroq ishlashi uchun)
        Dictionary.objects.bulk_create(words_to_create, ignore_conflicts=True)
        self.stdout.write(self.style.SUCCESS(f"Jami {len(words_to_create)} ta so'z bazaga yuklandi!"))