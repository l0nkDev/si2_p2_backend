html_1 = '''
<!doctype html>
<html lang="en">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
    <meta name="viewport"
        content="width=device-width, user-scalable=no, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>report</title>
    <style>
        h4 {
            margin: 0;
        }
        .margin-top {
            margin-top: 1.25rem;
        }
        table {
            width: 100%;
            border-spacing: 0;
        }
        td, tr, th, div {
            font-size: 12px;
            font-family: Arial, Helvetica, sans-serif;
        }
        table, th, td {
            border: 0.05px solid black;
        }
        .simple {
            border: 0px solid black;
        }
    </style>
</head>
<body>
<div style="text-align: center">
    <br><br>
    <b style="font-size: 30px">REPORTE DE '''
html_2 = '</b><br></div><br><div><table class="products simple"><tr>'
html_3 = '</tr>'
html_4 = '</table></div></body></html>'
    
from django.http import HttpResponse
from requests import Response
import pdfkit
import pandas
from io import BytesIO

def create_pdf_header(headers: list):
    string = ''
    for item in headers:
        string += "<th><b>{0}</b></th>".format(item)
    return string
        
def create_pdf_contents(res):
    string = ''
    for item in res:
        string += "<tr>"
        for i in item:
            string += '<td style="text-align: center">{0}</td>'.format(i)
        string += "</tr>"
    return string
        
def create_excel(headers, res):
    item = []
    items = []
    items.append(headers)
    for i in res:
        for j in i:
            item.append(j)
        items.append(item)
        item = []
    return items


def reportes(title, table, headers, format):
    if format == 'pdf':
        html = html_1 + title + html_2 + create_pdf_header(headers) + html_3 + create_pdf_contents(table) + html_4
        pdf = pdfkit.from_string(html, False)  
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'filename="report.pdf"'
        return response
    if format == 'excel':
        df = pandas.DataFrame.from_records(create_excel(headers, table))
        out = BytesIO()
        wri = pandas.ExcelWriter(out)
        df.to_excel(wri)
        wri.close()
        response = HttpResponse(out.getvalue(), content_type='application/excel')
        response['Content-Disposition'] = 'filename="report.xlsx"'
        return response
    if format == 'html':
        html = html_1 + title + html_2 + create_pdf_header(headers) + html_3 + create_pdf_contents(table) + html_4
        response = HttpResponse(html)
        return response
    if format == 'csv':
        df = pandas.DataFrame.from_records(create_excel(headers, table))
        out = BytesIO()
        df.to_csv(out)
        response = HttpResponse(out.getvalue(), content_type='application/csv')
        response['Content-Disposition'] = 'filename="report.csv"'
        return response
    print(format)
    return Response(status=400)

['Santiago', 'Diego', 'Mateo', 'Jose', 'Iván', 'Sebastián', 'Camilo', 'Leonardo', 
 'Iker', 'Matías', 'Dominic', 'José', 'Teotriste', 'Luis', 'Abalgamar', 'Carlos', 
 'Atilio', 'Juan', 'Aristipio', 'Jorge', 'Abaracuatira', 'Emiliano', 'Angel',
 'David', 'Miguel', 'Daniel', 'Fernando', 'Alexander', 'Emmanuel', 'Alejandro', 'Maximiliano',
 'Jesus', 'Gael', 'Pedro', 'Manuel', 'Oscar', 'Miguel', 'John', 'Jaime', 'Francisco', 'Rafael',
 'Julio', 'Esteban', 'Mateo', 'Simon', 'Nicolas', 'Santiago', 'Sofia', 'Azucena', 'Maria', 'Valentina',
 'Amalia', 'Ximena', 'Martina', 'Regina', 'Britany', 'Mariana', 'Daniela', 'Natalia', 'Valeria', 'Isabella',
 'Camila', 'Manuela', 'Renata', 'Juliana', 'Victoria', 'Alejandra', 'Romina', 'Gabriela', 'Fernanda', 'Sara',
 'Andrea', 'Paula', 'Alexa', 'Laura', 'Guadalupe', 'Samantha', 'Paola', 'Melissa', 'Angie', 'Elizabeth', 'Vanessa',
 'Yamileth', 'Isabel', 'Fátima', 'Ana', 'Aitana', 'Luisa', 'Abigail', 'Paulina']