# Correct paragraph target

User screenshot clarifies the requested text belongs to hero introduction beneath name, not About. Put exact requested paragraph into .hero-copy:
A first-year International Economics and Finance student at Bocconi, curious about why markets move the way they do and what makes a good investment. This portfolio shares my projects, experience, leadership and extracurricular activities, and certifications, alongside my interests beyond finance.

Restore About .prose original three paragraphs from cf3a42a:index.html. Keep Leadership & Activities navigation change and all other current files/content unchanged. Builder HTML only; root brief/review. Check exact hero and restored About; targeted browser desktop1440/mobile390 for longer hero/no overflow/buttons/portrait/nav. No full regression suite needed. No commit/push.

## Review

Builder targeted Chromium checks passed at1440/390 for exact text, layout, buttons, portrait load and no overflow. Coordinator independently verified exact hero paragraph, About restored from cf3a42a and retained navigation label. HTML-only correction; whitespace check passed.
