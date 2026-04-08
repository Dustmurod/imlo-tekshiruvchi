def get_root(word):
    """
    O'zbek tilidagi qo'shimchalarni zanjirsimon (birin-ketin) olib tashlaydi.
    Masalan: ayroportlarda -> ayroportlar -> ayroport
    """
    # Qo'shimchalar ro'yxati (eng uzunidan boshlab qidirish kerak)
    suffixes = [
        # Kelishik va egalik
        'ning', 'ni', 'ga', 'dan', 'da', 'lar', 'im', 'm', 'ing', 'si', 'i', 'u', 'yu',
        # Fe'l zamonlari va shaxslari
        'dilar', 'dingiz', 'ding', 'dim', 'di', 'tik', 'gan', 'kan', 'qan', 
        'yap', 'moqda', 'moq', 'ish', 'ush', 'miz', 'siz'
    ]
    
    temp_word = word.lower()
    # Uzun qo'shimchalar birinchi tekshirilishi uchun tartiblaymiz
    sorted_suffixes = sorted(suffixes, key=len, reverse=True)

    # Toki qo'shimcha topilib, qirqib tashlanar ekan, sikl davom etadi
    while True:
        found_suffix = False
        for suffix in sorted_suffixes:
            # Agar so'z shu qo'shimcha bilan tugasa va o'zak kamida 3 harf qolsa
            if temp_word.endswith(suffix) and len(temp_word) > len(suffix) + 2:
                temp_word = temp_word[:-len(suffix)]
                found_suffix = True
                break # Ichki for'dan chiqib, yangilangan so'z bilan while'ni boshidan boshlaydi
        
        # Agar birorta ham qo'shimcha topilmasa, sikldan chiqamiz
        if not found_suffix:
            break
            
    return temp_word

def levenshtein_distance(s1, s2):    
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)
    if len(s2) == 0:
        return len(s1)
    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    return previous_row[-1]