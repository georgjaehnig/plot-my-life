import svgwrite

dwg = svgwrite.Drawing(filename=u'life-weeks.svg', size=(u'210mm', u'297mm'))
g = dwg.g(style="font-family:Arial")

box_width = 3.5
box_height = 3.5

weeks_y_margin = 5

for week in range(1,54):
    tspan = svgwrite.text.TSpan(
        str(week), 
        insert=(str(week * box_width + box_width/2) + 'mm', str(weeks_y_margin) + 'mm'), 
        style='text-align:center;text-anchor:middle'
    )
    text = dwg.text('', style='font-size:10px')
    text.add(tspan)
    dwg.add(text)

boxes_y_margin = 6

for life_year in range(0,80):
    for week in range(1,54):
        rect = svgwrite.shapes.Rect(
            insert=(str(week * box_width) + 'mm', str(boxes_y_margin + life_year * box_height) + 'mm'), 
            size=(str(box_width) + 'mm', str(box_height) + 'mm'),
            style="fill:#ffffff;stroke:#c0c0c0;stroke-width:1px"
        )
        dwg.add(rect)


dwg.save()

