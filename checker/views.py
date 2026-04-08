import time
from django.shortcuts import render
from django.contrib.postgres.search import TrigramSimilarity
from .models import Dictionary
from .utils import get_root, levenshtein_distance

def normalize_uzbek_word(word):
    """
    O'zbek tilidagi turli xil tutuq va O'/G' belgilarini standartlashtiradi.
    """
    if not word:
        return ""
    
    w = word.strip('.,!?:;"() ').lower()
    bad_chars = ['’', '‘', '`', '´', 'ʻ', 'ʼ', '’', '\u02bb', '\u02bc', '\u2018', '\u2019']
    for char in bad_chars:
        w = w.replace(char, "'")
    return w

def check_text(text):
    """
    Matnni tahlil qilish: Bazada yo'q har qanday uzun so'zni xato deb belgilaydi.
    """
    start_time = time.time()
    words_in_text = text.split()
    total_words = len(words_in_text)
    error_count = 0
    result = []

    for w in words_in_text:
        # 1. Normalizatsiya va Ildizni topish
        search_word = normalize_uzbek_word(w)
        root_word = get_root(search_word)
        no_apostrophe = search_word.replace("'", "")

        # 2. Bazadan qidirish (To'g'ridan-to'g'ri, belgisiz yoki ildiz bo'yicha)
        entry = Dictionary.objects.filter(word=search_word).first() or \
                Dictionary.objects.filter(word=no_apostrophe).first() or \
                Dictionary.objects.filter(word=root_word).first()

        if entry:
            # So'z bazada topildi (To'g'ri)
            result.append({
                "word": w, 
                "correct": True, 
                "suggestions": [],
                "definition": entry.definition
            })
        else:
            # 3. Bazada yo'q so'z - DEMAK BU XATO
            # Endi faqat foydalanuvchiga yordam sifatida variantlar qidiramiz
            candidates = Dictionary.objects.annotate(
                similarity=TrigramSimilarity('word', search_word),
            ).filter(similarity__gt=0.2).order_by('-similarity')[:5]
            
            suggestions = []
            for c in candidates:
                # Masofani 3 gacha kengaytirdik (uzunroq so'zlar uchun)
                if levenshtein_distance(search_word, c.word) <= 3:
                    suggestions.append(c.word)
            
            # 4. Qat'iy mantiq: Agar so'z 3 harfdan uzun bo'lsa va bazada yo'q bo'lsa - XATO
            if len(search_word) > 3:
                error_count += 1
                result.append({
                    "word": w, 
                    "correct": False, 
                    "suggestions": suggestions,
                    "definition": None
                })
            else:
                # Juda qisqa so'zlar (men, sen, u, va) lug'atda bo'lmasa ham to'g'ri deb o'tiladi
                result.append({
                    "word": w, 
                    "correct": True, 
                    "suggestions": [],
                    "definition": None
                })

    # Statistika hisoblash
    end_time = time.time()
    check_duration = round((end_time - start_time) * 1000, 2)
    accuracy = round(((total_words - error_count) / total_words * 100), 1) if total_words > 0 else 0

    stats = {
        "total": total_words, 
        "errors": error_count, 
        "accuracy": accuracy, 
        "duration": check_duration
    }
    return result, stats

def index(request):
    result = []
    stats = None
    text = ""
    if request.method == "POST":
        text = request.POST.get("text", "")
        if text.strip():
            result, stats = check_text(text)
    
    return render(request, "index.html", {
        "result": result, 
        "stats": stats, 
        "text": text
    })