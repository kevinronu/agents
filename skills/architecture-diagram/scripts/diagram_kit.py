"""Build draw.io architecture diagrams that follow references/standard.md.

A diagram is a small Python file that imports this module, places every piece on a
fixed grid and lists every arrow. `save` adds the legend on top and writes the
.drawio file; `export` renders the PNG to review.

    from diagram_kit import Diagram
    d = Diagram()
    d.container('fp', 'Face recognition pipeline', 0, 0, 900, 300)
    d.resource('sr', 'lambda', 'new', 'save-reference-frames', 'saves the frames', 665, 680)
    d.resource('ine', 'external', 'unchanged', 'INE middleware', 'not called with a scenario', 40, 400)
    d.group('checks', 'Synchronous checks (10)', 'Simulate: pass, reject or error', 300, 80, state='changed')
    d.call('e1', 'sr', 'vi', 'UpdateItem (rw)', 'reference_frames')
    d.save('arch.drawio')
    d.export('arch.drawio', 'arch.png')

A diagram of a system as it is uses the state 'plain' for every piece.
"""

import re
import shutil
import subprocess

SERVICES = {
    'lambda': ('lambda', '#ED7100', 'Lambda'),
    'dynamodb': ('dynamodb', '#C925D1', 'DynamoDB'),
    's3': ('s3', '#7AA116', 'S3 bucket'),
    'rekognition': ('rekognition', '#01A88D', 'Rekognition'),
    'sqs': ('sqs', '#E7157B', 'SQS queue'),
    'sns': ('sns', '#E7157B', 'SNS topic'),
    'eventbridge': ('eventbridge', '#E7157B', 'EventBridge'),
    'eventbridge_pipes': ('eventbridge_pipes', '#E7157B', 'EventBridge Pipe'),
    'step_functions': ('step_functions', '#E7157B', 'Step Functions'),
    'api_gateway': ('api_gateway', '#8C4FFF', 'API Gateway'),
    'elasticsearch': ('elasticsearch_service', '#8C4FFF', 'Elasticsearch'),
    'external': (None, '#0080F0', 'External'),
}
DESIGN_STATES = ('new', 'changed', 'unchanged')
PLAIN = 'plain'

ICON = ('sketch=0;outlineConnect=0;fontColor=#232F3E;fillColor={color};strokeColor=#ffffff;'
        'verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;fontSize={size};'
        'aspect=fixed;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.{icon};')
EXTERNAL = ('html=1;fillColor=none;strokeColor={color};strokeWidth=2;fontColor=#232F3E;'
            'verticalLabelPosition=bottom;verticalAlign=top;align=center;fontSize={size};'
            'shape=mxgraph.ios7.icons.cloud;')
UNCHANGED_OPACITY = 'opacity=70;textOpacity=100;'
BADGE = ('ellipse;whiteSpace=wrap;html=1;fontSize=13;fontStyle=1;align=center;verticalAlign=middle;'
         'strokeWidth=1.5;strokeColor=#232F3E;')
GROUPED = 'rounded=0;whiteSpace=wrap;html=1;fillColor=#E5E7EB;strokeColor=#9CA3AF;fontColor=#374151;fontSize=14;'
CONTAINER_FILL = '#F9FAFB'
CONTAINER = (f'rounded=0;whiteSpace=wrap;html=1;fillColor={CONTAINER_FILL};strokeColor=#D1D5DB;'
             'fontColor=#374151;fontSize=14;verticalAlign=top;spacingTop=4;')
GROUP_WIDTH = 250
GROUP_TEXT_MARGIN = 20
SUBTITLE_CHAR_WIDTH = 6.2
NAME_CHAR_WIDTH = 7.5
TEXT = 'text;html=1;fontSize=12;align=left;verticalAlign=middle;fontColor=#232F3E;'
LEGEND_TITLE = 'text;html=1;fontSize=12;fontStyle=1;align=left;verticalAlign=middle;fontColor=#232F3E;'
EDGE = 'edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;labelBackgroundColor={background};'

LEGEND_HEIGHT = 190
LEGEND_STEP = 95
LEGEND_RULES = ('Call: from the caller to what it calls.<br>'
                '&nbsp;&nbsp;Label: Operation (r / w / rw) + what it sends or gets<br>'
                'Event: from the source to what receives it.<br>'
                '&nbsp;&nbsp;Label: how it arrives, the filter, if any;<br>&nbsp;&nbsp;the delivery setting, if it matters<br>'
                'r = read, w = write, rw = read and write')
DRAWIO_APP = '/Applications/draw.io.app/Contents/MacOS/draw.io'


def escape(text):
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')


def html_text(text):
    """Shows `<` and `>` literally (as in `<client_id>`) while keeping `<br>` as a line break."""
    return escape(text).replace('&lt;br&gt;', '<br>')


def name_and_subtitle(name, subtitle):
    if not subtitle:
        return escape(html_text(name))
    return escape(f'{html_text(name)}<br><font style="font-size: 11px;">{html_text(subtitle)}</font>')


def _label_width(cell):
    """Approximate pixel width of an icon's label: its longest line at about 7 px a character."""
    value = re.search(r'value="([^"]*)"', cell).group(1)
    text = re.sub(r'&lt;br&gt;|&amp;lt;br&amp;gt;', '\n', value)
    text = re.sub(r'&lt;.*?&gt;|&amp;lt;|&amp;gt;|&amp;\w+;', '', text)
    return max((len(line) for line in text.split('\n')), default=0) * 7


class Diagram:
    def __init__(self):
        self._cells = []
        self._services = []
        self._states = set()
        self._has_group = False

    def resource(self, cell_id, service, state, name, subtitle, x, y):
        """Place one resource as a 50x50 icon. `subtitle` says what it does in this change or flow."""
        if service not in SERVICES:
            raise ValueError(f'unknown service {service!r}: add it to SERVICES with its aws4 resIcon and color')
        self._use_state(state)
        if service not in self._services:
            self._services.append(service)
        self._icon(cell_id, name_and_subtitle(name, subtitle), service, state, x, y, size=14)

    def group(self, cell_id, name, subtitle, x, y, state='unchanged'):
        """Several resources that act as one step, drawn as one gray box of fixed width that grows
        down. `state` is the one all of them share; `subtitle` says what they do, not which they are."""
        self._use_state(state)
        self._check_fits_group(name, subtitle)
        self._has_group = True
        lines = subtitle.count('<br>') + 1 if subtitle else 0
        height = max(50, 36 + 15 * lines)
        y += LEGEND_HEIGHT
        self._cells.append(f'<mxCell id="{cell_id}" value="{name_and_subtitle(name, subtitle)}" style="{GROUPED}" '
                           f'vertex="1" parent="1"><mxGeometry x="{x}" y="{y}" width="{GROUP_WIDTH}" '
                           f'height="{height}" as="geometry"/></mxCell>')
        self._mark(cell_id, state, x + GROUP_WIDTH - 12, y - 10)

    def container(self, cell_id, title, x, y, width, height):
        """A frame that names a system around icons and group boxes. No arrow touches it.
        Declare it before its contents."""
        self._vertex(cell_id, escape(f'<b>{title}</b>'), CONTAINER, x, y, width, height)

    def call(self, cell_id, source, target, operation, payload='', **route):
        """Sync arrow from the caller to what it calls, labeled `Operation (r/w/rw)` / what travels."""
        self._edge(cell_id, source, target, self._two_lines(operation, payload), dashed=False, **route)

    def event(self, cell_id, source, target, source_name, condition='', **route):
        """Async arrow from the event source to what receives it, labeled source / condition."""
        self._edge(cell_id, source, target, self._two_lines(source_name, condition), dashed=True, **route)

    def save(self, path):
        self._check_unique_ids()
        legend = self._centered(self._legend())
        xml = ('<mxGraphModel adaptiveColors="auto"><root><mxCell id="0"/><mxCell id="1" parent="0"/>'
               + ''.join(legend + self._cells) + '</root></mxGraphModel>')
        with open(path, 'w') as file:
            file.write(xml)

    def _centered(self, legend):
        """Shifts the legend so its middle sits over the middle of the diagram below it."""
        legend_left, legend_right = self._horizontal_span(legend)
        body_left, body_right = self._horizontal_span(self._cells)
        shift = (body_left + body_right) / 2 - (legend_left + legend_right) / 2

        def move(match):
            return f'{match.group(1)}{float(match.group(2)) + shift:g}"'
        return [re.sub(r'(<mx(?:Geometry|Point) x=")([-\d.]+)"', move, cell) for cell in legend]

    @staticmethod
    def _horizontal_span(cells):
        """Left and right edge of what the cells draw, counting the text under an icon, which
        is wider than the icon."""
        edges = []
        for cell in cells:
            for x, width in re.findall(r'<mxGeometry x="([-\d.]+)"[^>]*?width="([\d.]+)"', cell):
                left, right = float(x), float(x) + float(width)
                text_width = _label_width(cell) if 'verticalLabelPosition=bottom' in cell else 0
                center = (left + right) / 2
                edges += [min(left, center - text_width / 2), max(right, center + text_width / 2)]
            edges += [float(x) for x in re.findall(r'<mxPoint x="([-\d.]+)"', cell)]
        return min(edges), max(edges)

    def _use_state(self, state):
        if state not in DESIGN_STATES + (PLAIN,):
            raise ValueError(f'state must be one of {DESIGN_STATES + (PLAIN,)}')
        self._states.add(state)
        if PLAIN in self._states and len(self._states) > 1:
            raise ValueError("'plain' is for a system as it is; a design uses only new, changed and unchanged")

    @staticmethod
    def _check_fits_group(name, subtitle):
        lines = [(name, NAME_CHAR_WIDTH)] + [(line, SUBTITLE_CHAR_WIDTH) for line in subtitle.split('<br>')]
        for line, char_width in lines:
            if len(line) * char_width > GROUP_WIDTH - GROUP_TEXT_MARGIN:
                raise ValueError(f'group text line too long: {line!r}. Say what the pieces do, '
                                 'not which they are, or break the line between two facts')

    def _check_unique_ids(self):
        ids = re.findall(r'<mxCell id="([^"]+)"', ''.join(self._cells))
        duplicated = sorted({cell_id for cell_id in ids if ids.count(cell_id) > 1})
        if duplicated:
            raise ValueError(f'duplicated cell ids: {duplicated}. draw.io would drop their arrows silently')

    @staticmethod
    def export(drawio_path, png_path):
        binary = DRAWIO_APP if shutil.which(DRAWIO_APP) else shutil.which('drawio')
        if not binary:
            raise RuntimeError('draw.io desktop is not installed: brew install --cask drawio')
        subprocess.run([binary, '-x', '-f', 'png', '-s', '2', '--border', '30', '-o', png_path, drawio_path],
                       check=True, capture_output=True)

    @staticmethod
    def _two_lines(first, second):
        return f'{first}<br>{second}' if second else first

    def _vertex(self, cell_id, value, style, x, y, width, height):
        self._cells.append(f'<mxCell id="{cell_id}" value="{value}" style="{style}" vertex="1" parent="1">'
                           f'<mxGeometry x="{x}" y="{y + LEGEND_HEIGHT}" width="{width}" height="{height}" '
                           f'as="geometry"/></mxCell>')

    def _icon(self, cell_id, value, service, state, x, y, size, top=LEGEND_HEIGHT):
        icon, color, _ = SERVICES[service]
        if icon is None:
            style = EXTERNAL.format(color=color, size=size)
        else:
            style = ICON.format(color=color, size=size, icon=icon)
        y += top
        if state == 'unchanged':
            style += UNCHANGED_OPACITY
        if state == 'new':
            self._cells.append(f'<mxCell id="{cell_id}_ring" value="" style="rounded=1;arcSize=12;fillColor=none;'
                               f'strokeColor={color};strokeWidth=3;" vertex="1" parent="1">'
                               f'<mxGeometry x="{x - 5}" y="{y - 5}" width="60" height="60" as="geometry"/></mxCell>')
        self._cells.append(f'<mxCell id="{cell_id}" value="{value}" style="{style}" vertex="1" parent="1">'
                           f'<mxGeometry x="{x}" y="{y}" width="50" height="50" as="geometry"/></mxCell>')
        self._mark(cell_id, state, x + 38, y - 10)

    def _mark(self, cell_id, state, x, y):
        """Draws the `+` or `~` that carries a new or changed state; the absolute `y` already counts the legend."""
        if state not in ('new', 'changed'):
            return
        mark, colors = (('+', 'fillColor=#232F3E;fontColor=#FFFFFF;') if state == 'new'
                        else ('~', 'fillColor=#FFFFFF;fontColor=#232F3E;'))
        self._cells.append(f'<mxCell id="{cell_id}_badge" value="{mark}" style="{BADGE}{colors}" vertex="1" '
                           f'parent="1"><mxGeometry x="{x}" y="{y}" width="20" height="20" as="geometry"/></mxCell>')

    def _edge(self, cell_id, source, target, value, dashed, ports='', points=(), label_position=None,
              label_shift_x=None, inside_container=False):
        """`ports` pins exits and entries, `points` are absolute waypoints in diagram coordinates,
        `label_position` slides the label along the line (-1 to 1), `label_shift_x` moves it sideways."""
        background = CONTAINER_FILL if inside_container else '#ffffff'
        style = EDGE.format(background=background) + ('dashed=1;' if dashed else '') + ports
        waypoints = ''.join(f'<mxPoint x="{x}" y="{y + LEGEND_HEIGHT}"/>' for x, y in points)
        array = f'<Array as="points">{waypoints}</Array>' if waypoints else ''
        position = f'x="{label_position}" ' if label_position is not None else ''
        shift = f'<mxPoint x="{label_shift_x}" y="0" as="offset"/>' if label_shift_x is not None else ''
        self._cells.append(f'<mxCell id="{cell_id}" value="{escape(html_text(value))}" style="{style}" edge="1" parent="1" '
                           f'source="{source}" target="{target}"><mxGeometry {position}relative="1" '
                           f'as="geometry">{array}{shift}</mxGeometry></mxCell>')

    def _legend(self):
        saved, self._cells = self._cells, []
        self._legend_text('legendServices', 'Service', 20, 0, LEGEND_TITLE)
        used = [service for service in SERVICES if service in self._services]
        for index, service in enumerate(used):
            self._icon(f'legendService{index}', escape(SERVICES[service][2]), service, 'plain',
                       20 + LEGEND_STEP * index, 28, size=12, top=0)

        lines_x = 20 + LEGEND_STEP * len(used) + 15
        if PLAIN not in self._states:
            states_x = lines_x
            self._legend_text('legendStates', escape('<b>State</b> <font color="#6B7280">(any service)</font>'),
                              states_x, 0, TEXT, width=200)
            for index, state in enumerate(DESIGN_STATES):
                self._icon(f'legendState{index}', state.capitalize(), 'lambda', state,
                           states_x + 5 + LEGEND_STEP * index, 28, size=12, top=0)
            lines_x = states_x + 5 + LEGEND_STEP * len(DESIGN_STATES)
        if self._has_group:
            group_x = lines_x
            self._legend_text('legendGroupTitle', 'Group', group_x, 0, LEGEND_TITLE, width=120)
            self._cells.append(f'<mxCell id="legendGroup" value="" style="{GROUPED}" '
                               f'vertex="1" parent="1"><mxGeometry x="{group_x}" y="28" width="100" height="50" '
                               f'as="geometry"/></mxCell>')
            lines_x = group_x + 100 + 30

        self._legend_line('legendSync', lines_x, 30, dashed=False)
        self._legend_text('legendSyncText', 'Sync: the caller waits for the answer', lines_x + 70, 20, TEXT, width=210)
        self._legend_line('legendAsync', lines_x, 60, dashed=True)
        self._legend_text('legendAsyncText', 'Async: the caller does not wait', lines_x + 70, 50, TEXT, width=210)
        self._legend_text('legendRules', escape(LEGEND_RULES), lines_x, 78, TEXT, width=285, height=100)
        legend, self._cells = self._cells, saved
        return legend

    def _legend_text(self, cell_id, value, x, y, style, width=300, height=20):
        self._cells.append(f'<mxCell id="{cell_id}" value="{value}" style="{style}" vertex="1" parent="1">'
                           f'<mxGeometry x="{x}" y="{y}" width="{width}" height="{height}" as="geometry"/></mxCell>')

    def _legend_line(self, cell_id, x, y, dashed):
        style = 'endArrow=classic;html=1;' + ('dashed=1;' if dashed else '')
        self._cells.append(f'<mxCell id="{cell_id}" value="" style="{style}" edge="1" parent="1">'
                           f'<mxGeometry relative="1" as="geometry"><mxPoint x="{x}" y="{y}" as="sourcePoint"/>'
                           f'<mxPoint x="{x + 60}" y="{y}" as="targetPoint"/></mxGeometry></mxCell>')
