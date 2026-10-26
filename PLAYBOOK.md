# NeriaTech – מדריך הפקה שבועי

מדריך לכל סשן (כולל משימה מתוזמנת) שמכין תוכן ל-@neria.tech.
כל התקשורת עם נריה – בעברית.

## הקשר
- **חשבון:** @neria.tech (אינסטגרם, מחובר לעמוד הפייסבוק NeriaTech).
- **קהל:** בעלי עסקים קטנים בישראל. נריה מפתח Full Stack פרילנסר: אתרים, אפליקציות, מערכות, אוטומציות, תמונות וסרטוני AI לעסקים.
- **נריה לא מופיע מול מצלמה** – רק תוכן גרפי ומונפש.
- **קריאה לפעולה:** "שלחו לי הודעה" / "כתבו בתגובות".

## לו״ז קבוע
| יום | פורמט |
|---|---|
| א׳ | קרוסלה |
| ג׳ | ריל |
| ה׳ | קרוסלה |
| מוצ״ש | ריל (או קרוסלה כשאין חומר לריל) |
כל הפרסומים ב-19:30 שעון ישראל. סנריו Make מס׳ 8167166 ("NeriaTech – פרסום אינסטגרם") רץ בימים א׳–ה׳ ובמוצ״ש, קורא את `posts/YYYY-MM-DD.json` ואת `stories/YYYY-MM-DD.json`, ומפרסם רק כש-`"approved": true`.

**סטוריז** (3 בשבוע, 19:30): ב׳ – שאלה לקהל ("ענו לי בהודעה"; אין סקרים דרך ה-API), ד׳ – טיזר לריל של ג׳, מוצ״ש – טיזר לפוסט של אותו ערב. קובץ: `{"approved":false,"image_url":".../media/stories/YYYY-MM-DD.jpg"}`. תמונה JPEG ‏1080×1920 עם `tools/render_story.py`. הסטורי מתפרסם דרך HTTP + Graph API עם המפתח "NeriaTech IG Token" (Make key 272135).

## מקורות אמת
- **לוח התוכן (נושאים וסטטוס):** https://claude.ai/artifact/Ah3XVgXkYmey3EkRtQS64M – אוסף `posts`, מזהה מסמך = תאריך. שדות: date, day, format (קרוסלה/ריל/סטורי), topic, status (רעיון / בהכנה / ממתין לאישור / מאושר / פורסם), note.
- **נוהל ניהול החשבון:** https://claude.ai/artifact/VgR2ucMS5A2JQj6vB8Kb7W
- **הריפו הזה:** קבצי פוסטים ומדיה ציבוריים.
- **תיק העבודות של נריה (פרטי):** באותו לוח תוכן, אוסף `portfolio`. כל מסמך = עבודה אמיתית: title, service (אתר / אפליקציה / מערכת / אוטומציה / AI), client_type, problem, solution, results, can_publish (true/false), assets (תיאור), added_at. **לא מעתיקים את התוכן הזה לריפו הציבורי** מעבר למה שנכנס לפוסט מאושר.
  - בונים פוסטים רק על שירותים שמופיעים שם, ועל עבודות עם `can_publish: true`.
  - מספרים ותוצאות רק כפי שנכתבו שם. לא ממציאים.
  - כשאין מספיק עבודות לשבוע – חוזרים לתוכן חינוכי כללי.

## פורמט קובץ פוסט
```json
{"type":"carousel","approved":false,
 "files":[{"media_type":"IMAGE","image_url":"https://raw.githubusercontent.com/neriaok/neriatech-content/main/media/<תיקייה>/01.jpg"}],
 "caption":"..."}
```
ריל: `{"type":"reel","approved":false,"video_url":".../reel.mp4","caption":"..."}`.
קרוסלה: 2–10 תמונות JPEG 1080×1350. ריל: MP4 ‏1080×1920, H.264 + AAC, 3 שניות עד 15 דקות.

## כלים (`tools/`)
- `render_carousel.py <dir> <dir>/out <slides.json>` – מרנדר שקפים. בתיקייה צריכים להיות `assets/*` (פונטים + logo.png). ראו `slides_example.json` (kind: cover / item / cta, אפשר `btn`).
- `reel_template_whatsapp.html` + `render_reel.py <html> <frames_dir> <sec> 15` ואז ffmpeg (ראו למטה) – ריל מונפש. הפונקציה `setT(t)` מציירת כל פריים.
- `build_week_preview.py <repo> tools/assets/logo.png <out.html> <dates...>` – קובץ תצוגה מקדימה בסגנון אינסטגרם לכל פוסטי השבוע.
- קידוד ריל:
  `ffmpeg -framerate 15 -i frames/f%04d.jpg -f lavfi -i anullsrc=r=48000:cl=stereo -shortest -r 30 -c:v libx264 -profile:v high -pix_fmt yuv420p -b:v 4M -maxrate 4.5M -bufsize 9M -g 30 -c:a aac -b:a 128k -ar 48000 -movflags +faststart reel.mp4`

## סגנון
רקע כחול-לילה (#070D1C) עם הילות כחולות, טקסט לבן, הדגשה #4D9BFF, פונט Heebo, מספרים במתאר, לוגו + "NeriaTech" למעלה, `@neria.tech` למטה. משפטים קצרים, עברית פשוטה, בלי אימוג׳י בשקפים. הדגמות עם עסק דמיוני מסומנות "הדגמה · עסק דמיוני". לא ממציאים לקוחות, ביקורות או מספרים.

## כללי אישור
- כל פוסט חדש נכתב עם `"approved": false`.
- מסמנים `true` **רק** אחרי שנריה אישר במפורש בצ׳אט.
- נושא שדורש חומר אמיתי שלא התקבל – מחליפים לנושא שלא דורש אותו, ומעדכנים את הלוח.
