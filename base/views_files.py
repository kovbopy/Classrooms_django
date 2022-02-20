import csv
import io
from django.http import HttpResponse, FileResponse
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from base.models import Classroom


classrooms = [f'Classroom : {classroom.name},\nTeacher: {classroom.teacher},\n'
              f'Students: {[b for a in classroom.students.values("username", "id") for b in a],}\n\n'
              for classroom in Classroom.objects.all()]

def classrooms_txt(request):
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename=classrooms.txt'
    response.writelines(classrooms)
    return response

def classrooms_pdf(request):
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
    textob = c.beginText()
    textob.setTextOrigin(inch, inch)
    textob.setFont('Helvetica', 12)

    for g in classrooms:
        textob.textLine(g)

    c.drawText(textob)
    c.showPage()
    c.save()
    buf.seek(0)
    return FileResponse(buf, as_attachment=True, filename='classrooms.pdf')

def classrooms_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=classrooms.csv'

    writer = csv.writer(response)
    writer.writerow(['Name', 'Teacher','Students'])

    for classroom in Classroom.objects.all():
        writer.writerow([classroom.name, classroom.teacher,
                         [b for a in classroom.students.values_list("name","id") for b in a]])
    return response
