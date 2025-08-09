
from docx import Document
import re

path = "main/templates/documents/Справка с пасмотрными данными.docx"

context = {
            'ФИО': 'da',
            'Город_проживания': 'Moscow',
            'Дата_рождения': 'Today',
            'дата_выдачи': "now"
        }

doc = Document(path)
text = "\n".join([p.text for p in doc.paragraphs])
fields = re.findall(r'\{\{\s*([^}]+)\s*\}\}', text)
fields.append("Ешкин_кошкин")

not_match = []
keys = [i for i in context.keys()]

for i in fields:
    print(i)
    if i not in keys:
        not_match.append(i)

print(not_match)

