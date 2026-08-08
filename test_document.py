from pipeline import Document

doc = Document(

    id="1",

    text="Revenue increased.",

    source="Apple.pdf",

    document_type="pdf",

    access="public",

    page=1

)

print(doc)
print(doc.text)
print(doc.page)