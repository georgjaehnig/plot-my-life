import svgwrite
import datetime


def has_53_weeks(year):
    date = datetime.date(year, 12, 31)
    week = date.isocalendar()[1]
    return (week == 53)

birthday = datetime.date(1980, 3, 20)

dwg = svgwrite.Drawing(filename=u'life-weeks.svg', size=(u'210mm', u'297mm'))
g = dwg.g(style="font-family:Arial")

box_width = 3.5
box_height = 3.5

weeks_x_margin = 4
weeks_y_margin = 5

life_years_x_margin = 5
life_years_y_margin = 8.6

years_x_margin = 200
years_y_margin = 8.6

boxes_x_margin = 4
boxes_y_margin = 6

for week in range(1,54):
    tspan = svgwrite.text.TSpan(
        str(week), 
        insert=(str(weeks_x_margin + week * box_width + box_width/2) + 'mm', str(weeks_y_margin) + 'mm'), 
        style='text-align:center;text-anchor:middle'
    )
    text = dwg.text('', style='font-size:10px')
    text.add(tspan)
    dwg.add(text)

for life_year in range(0,80):
    tspan = svgwrite.text.TSpan(
        str(life_year), 
        insert=(str(life_years_x_margin) + 'mm', str(life_years_y_margin + life_year * box_height) + 'mm'), 
        style='text-align:right;text-anchor:end'
    )
    text = dwg.text('', style='font-size:10px')
    text.add(tspan)
    dwg.add(text)

for year in range(birthday.year,birthday.year+80):
    tspan = svgwrite.text.TSpan(
        str(year), 
        insert=(str(years_x_margin) + 'mm', str(years_y_margin + (year-birthday.year) * box_height) + 'mm'), 
        style='text-align:right;text-anchor:end'
    )
    text = dwg.text('', style='font-size:10px')
    text.add(tspan)
    dwg.add(text)

#for life_year in range(0,80):
for year in range(birthday.year,birthday.year+80):
    for week in range(1,54):
        # Show 53rd week only if exists.
        if (week == 53) and not has_53_weeks(year):
            continue
        rect = svgwrite.shapes.Rect(
            insert=(str(boxes_x_margin + week * box_width) + 'mm', str(boxes_y_margin + (year-birthday.year)  * box_height) + 'mm'), 
            size=(str(box_width) + 'mm', str(box_height) + 'mm'),
            style="fill:#ffffff;stroke:#c0c0c0;stroke-width:0.1mm"
        )
        dwg.add(rect)

dwg.save()
