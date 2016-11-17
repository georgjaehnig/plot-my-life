import svgwrite
import datetime
import yaml

import sys
import argparse


def has_53_weeks(year):
    date = datetime.date(year, 12, 31)
    week = date.isocalendar()[1]
    return (week == 53)

def generate(settings_files):

    settings = {}
    for settings_file in settings_files:
        with open(settings_file, 'r') as stream:
            current_settings = yaml.load(stream)
            settings = {**settings, **current_settings}

    if not sys.stdin.isatty():
        current_settings = yaml.load(sys.stdin)
        settings = {**settings, **current_settings}

    if not settings['birthday']:
        settings['birthday'] = datetime.date(1990, 1, 1)

    dwg = svgwrite.Drawing(filename=u'life-weeks.svg', size=(u'210mm', u'297mm'))
    g = dwg.g(style="font-family:Arial")

    for week in range(1,54):
        tspan = svgwrite.text.TSpan(
            str(week), 
            insert = (
                str(settings['weeks']['margins']['x'] + week * settings['boxes']['size']['width'] + settings['boxes']['size']['width']/2) + 'mm',
                str(settings['weeks']['margins']['y']) + 'mm'
            ), 
            style = settings['weeks']['style']
        )
        text = dwg.text('', style='font-size:10px')
        text.add(tspan)
        dwg.add(text)

    for life_year in range(0,80):
        tspan = svgwrite.text.TSpan(
            str(life_year), 
            insert = (
                str(settings['life_years']['margins']['x']) + 'mm', 
                str(settings['life_years']['margins']['y'] + life_year * settings['boxes']['size']['height']) + 'mm'
            ), 
            style = settings['life_years']['style']
        )
        text = dwg.text('', style='font-size:10px')
        text.add(tspan)
        dwg.add(text)

    for year in range(settings['birthday'].year,settings['birthday'].year+80):
        tspan = svgwrite.text.TSpan(
            str(year), 
            insert = (
                str(settings['years']['margins']['x']) + 'mm', 
                str(settings['years']['margins']['y'] + (year-settings['birthday'].year) * settings['boxes']['size']['height']) + 'mm'
            ), 
            style = settings['years']['style']
        )
        text = dwg.text('', style='font-size:10px')
        text.add(tspan)
        dwg.add(text)

    for year in range(settings['birthday'].year,settings['birthday'].year+80):
        for week in range(1,54):
            # Show weeks in first year only after settings['birthday'].
            if (year == settings['birthday'].year) and (week < settings['birthday'].isocalendar()[1]):
                continue
            # Show 53rd week only if exists.
            if (week == 53) and not has_53_weeks(year):
                continue
            rect = svgwrite.shapes.Rect(
                insert=(str(settings['boxes']['margins']['x'] + week * settings['boxes']['size']['width']) + 'mm', str(settings['boxes']['margins']['y'] + (year-settings['birthday'].year)  * settings['boxes']['size']['height']) + 'mm'), 
                size=(str(settings['boxes']['size']['width']) + 'mm', str(settings['boxes']['size']['height']) + 'mm'),
                style = settings['boxes']['style']
            )
            dwg.add(rect)
            # Show horizontal helper lines.
            if (year % 5 == 0) and (year > settings['birthday'].year):
                line = svgwrite.shapes.Line(
                    start = (
                        str(settings['boxes']['margins']['x'] + week * settings['boxes']['size']['width']) + 'mm', 
                        str(settings['boxes']['margins']['y'] + (year-settings['birthday'].year)  * settings['boxes']['size']['height']) + 'mm'
                    ), 
                    end = (
                        str(settings['boxes']['margins']['x'] + week * settings['boxes']['size']['width'] + settings['boxes']['size']['width']) + 'mm',
                        str(settings['boxes']['margins']['y'] + (year-settings['birthday'].year)  * settings['boxes']['size']['height']) + 'mm'
                    ), 
                    style="stroke:#000000;stroke-width:0.1mm"
                )
                dwg.add(line)
            # Show vertical helper lines.
            if (week % 5 == 0) and (week > 0):
                line = svgwrite.shapes.Line(
                    start = (
                        str(settings['boxes']['margins']['x'] + week * settings['boxes']['size']['width']) + 'mm', 
                        str(settings['boxes']['margins']['y'] + (year-settings['birthday'].year)  * settings['boxes']['size']['height']) + 'mm'
                    ), 
                    end = (
                        str(settings['boxes']['margins']['x'] + week * settings['boxes']['size']['width']) + 'mm', 
                        str(
                            settings['boxes']['margins']['y'] + 
                            (year - settings['birthday'].year) * settings['boxes']['size']['height'] + 
                            settings['boxes']['size']['height']) + 'mm'
                    ), 
                    style="stroke:#000000;stroke-width:0.1mm"
                )
                dwg.add(line)

    dwg.save()

ap = argparse.ArgumentParser()

ap.add_argument(
    "settings_file", 
    help="YAML file with settings.",
    type=str,
    nargs='+'
)

args = ap.parse_args()

if args.settings_file:
    generate(args.settings_file)
