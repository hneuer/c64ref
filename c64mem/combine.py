#!/usr/bin/python3

import re, os
import pprint
import markdown

filenames = [
	'c64mem_prg.txt',
	'c64mem_sta_awsm.txt',
	'c64mem_mapc64.txt',
	'c64mem_64er.txt',
	'c64mem_64intern.txt',
	'c64mem_64map.txt',
	'c64mem_jb.txt',
]
names = [
	'Programmer\'s Reference Guide',
	'STA',
	'Mapping the Commodore 64',
	'Memory Map mit Wandervorschl&auml;gen',
	'Data Becker [German]',
	'64map',
	'Jim Butterfield',
]
links = [
	'https://...',
	'https://...',
	'https://...',
	'https://...',
	'https://...',
	'https://...',
	'https://...',
]
descriptions = [
	'...',
	'...',
	'...',
	'...',
	'...',
	'...',
	'...',
]


titlecolor = ['017100', '004D7F', '99195E', 'F8BA00', 'B51700', '017B76', '017B76']
darkcolor = ['D8F2CB', 'C6E2FC', 'BFB7E8', 'FCF6CD', 'F4D2E3', 'D2F6F0', 'D2F6F0']
lightcolor = ['E5F2DF','E3F0FC','D5D1E8','FCFAE6','F5E4EC','E1F5F2','E1F5F2']

asm_donor_index = 0
source_index = 0 # we treat the Microsoft/Commodore source differently

f = os.popen('git log -1 --pretty=format:%h .')
revision = f.read()
f = os.popen('git log -1 --date=short --pretty=format:%cd .')
date = f.read()

data = []
linenumber = []
address = []
for filename in filenames:
	d = []
	for f in filename.split(';'):
		d += [line.rstrip() for line in open(f)]
	data.append(d)
	linenumber.append(0)
	address.append(0)
files = len(filenames)

asmaddress = 0
asmlinenumber = 0

for i in range(0, files):
	while True:
		line = data[i][linenumber[i]]
		if len(line) > 0 and line[0] == '$':
			break
		linenumber[i] = linenumber[i] + 1


print('<meta http-equiv="Content-type" content="text/html; charset=utf-8" />')
print('<title>Ultimate Commodore 64 BASIC & KERNAL ROM Disassembly</title>')
print('')
print('<script language="javascript">')
print('    window.onload = init;')
print('    function init() {')
print('        var tbl = document.getElementById("disassembly_table");')
print('        for (var i = 0; i < ' + str(len(filenames)) + '; i++) {')
print('            var key = "column_" + i;')
print('            var element_name = "checkbox_" + i;')
print('            var checked = localStorage.getItem(key) != "hidden";')
print('            document.getElementById(element_name).checked = checked;')
print('            hideCol(i, checked);')
print('        }')
print('    }')
print('    function hideCol(col, checked) {')
print('        var tbl = document.getElementById("disassembly_table");')
print('        for (var i = 0; i < tbl.rows.length; i++) {')
print('            tbl.rows[i].cells[col+1].style.display = checked ? "" : "none";')
print('        }')
print('        var key = "column_" + col;')
print('        if (checked) {')
print('            localStorage.removeItem(key);')
print('        } else {')
print('            localStorage.setItem(key, "hidden");')
print('        }')
print('    }')
print('</script>')
print('')
# http://tholman.com/github-corners/
print('<a href="https://github.com/mist64/c64disasm" class="github-corner" aria-label="View source on GitHub"><svg width="80" height="80" viewBox="0 0 250 250" style="fill:#004080; color:#fff; position: absolute; top: 0; border: 0; right: 0;" aria-hidden="true"><path d="M0,0 L115,115 L130,115 L142,142 L250,250 L250,0 Z"></path><path d="M128.3,109.0 C113.8,99.7 119.0,89.6 119.0,89.6 C122.0,82.7 120.5,78.6 120.5,78.6 C119.2,72.0 123.4,76.3 123.4,76.3 C127.3,80.9 125.5,87.3 125.5,87.3 C122.9,97.6 130.6,101.9 134.4,103.2" fill="currentColor" style="transform-origin: 130px 106px;" class="octo-arm"></path><path d="M115.0,115.0 C114.9,115.1 118.7,116.5 119.8,115.4 L133.7,101.6 C136.9,99.2 139.9,98.4 142.2,98.6 C133.8,88.0 127.5,74.4 143.8,58.0 C148.5,53.4 154.0,51.2 159.7,51.0 C160.3,49.4 163.2,43.6 171.4,40.1 C171.4,40.1 176.1,42.5 178.8,56.2 C183.1,58.6 187.2,61.8 190.9,65.4 C194.5,69.0 197.7,73.2 200.1,77.6 C213.8,80.2 216.3,84.9 216.3,84.9 C212.7,93.1 206.9,96.0 205.4,96.6 C205.1,102.4 203.0,107.8 198.3,112.5 C181.9,128.9 168.3,122.5 157.7,114.1 C157.9,116.9 156.7,120.9 152.7,124.9 L141.0,136.5 C139.8,137.7 141.6,141.9 141.8,141.8 Z" fill="currentColor" class="octo-body"></path></svg></a><style>.github-corner:hover .octo-arm{animation:octocat-wave 560ms ease-in-out}@keyframes octocat-wave{0%,100%{transform:rotate(0)}20%,60%{transform:rotate(-25deg)}40%,80%{transform:rotate(10deg)}}@media (max-width:500px){.github-corner:hover .octo-arm{animation:none}.github-corner .octo-arm{animation:octocat-wave 560ms ease-in-out}}</style>')

print('<style type="text/css">')
print('')
print('body {')
print('    background: #e0f0ff;')
print('    color: #004080;')
print('    font-family: Helvetica')
print('}')
print('')
print('a {')
print('    color: #0060a0;')
print('}')
print('')
print('h3 {')
print('    font-family: serif;')
print('}')
print('')
print('')
print('th.com {')
print('    font-weight: bold;')
print('}')
print('')
print('div {')
print('    padding: 1em;')
print('}')
print('')
print('div.disassembly_container {')
print('    padding: 1em 0em 1em 13em;')
print('    overflow: scroll;')
print('}')
print('')
print('table {')
print('    border-collapse: collapse;')
print('    border: solid 1px #0060a0;')
print('    color: black;')
print('}')
print('')
print('tr, td, th {')
print('    margin: 0px;')
print('    text-align:left;')
print('    vertical-align: text-top;')
print('}')
print('')
print('table.disassembly_table {')
print('    border: solid grey;')
print('    border-width:0px 0px 1px 0px;')
print('}')
print('')
print('table.disassembly_table td, table.disassembly_table th {')
print('    padding: 2px 4px;')
print('    border: solid grey;')
print('    border-width:0px 1px 0px 1px;')
print('}')
print('')
print('table.disassembly_table th.top_row {')
print('    border-width: 1px;')
print('    color: #e0f0ff;')
print('}')
print('')
print('table.disassembly_table th.left_column {')
print('    position: absolute;')
print('    width: 12em;')
print('    left: 8px;')
print('    z-index: 11;')
print('    border: 1px solid #000;')
print('    border-radius: 2px;')
print('    color: #e0f0ff;')
print('    background: #0060a0;')
print('}')
print('')
print('table.disassembly_table th.left_column a {')
print('    color: #e0f0ff;')
print('}')
print('')

for i in range(0, len(filenames)):
	print('table.disassembly_table th.top_row:nth-of-type(' + str(i+2) + ') {')
	print('    background: #' + titlecolor[i] + ';')
	print('}')
	print('')
	print('table.disassembly_table tr td:nth-of-type(' + str(i+1) + ') {')
	print('    background: #' + darkcolor[i] + ';')
	print('}')
	print('')
	print('table.disassembly_table tr:nth-child(even) td:nth-of-type(' + str(i+1) + ') {')
	print('    background: #' + lightcolor[i] + ';')
	print('}')
	print('')
	print('table.checkbox_table tr:nth-of-type(' + str(i+1) + ') {')
	print('    background: #' + lightcolor[i] + ';')
	print('}')
	print('')
	print('table.checkbox_table tr:nth-of-type(' + str(i+1) + ') td:nth-of-type(2) {')
	print('    background: #' + titlecolor[i] + ';')
	print('}')
	print('')

print('table.disassembly_table tr {')
print('    background: #f0f0f0;')
print('}')
print('')
print('table.disassembly_table tr:nth-child(even) {')
print('    background: #ffffff;')
print('}')
print('')
print('table.checkbox_table {')
print('    border-color: #0060a0;')
print('}')
print('')
print('table.checkbox_table a {')
print('    color: #e0f0ff;')
print('}')
print('')
print('table.checkbox_table tr, table.checkbox_table td {')
print('    padding: 4px 8px;')
print('    border: solid #0060a0;')
print('    border-width:1px 0px 1px 0px;')
print('}')
print('')
print('</style>')
print('<body>')

print('<h1>Ultimate Commodore 64 Memory Map</h1>')

print('<p><i>by <a href="http://www.pagetable.com/">Michael Steil</a>, <a href="https://github.com/mist64/c64disasm">github.com/mist64/c64disasm</a>. Revision ' + revision + ', ' + date + '</i></p>')

print('<b>This allows you to view different commentaries side-by-side. You can enable/disable individual columns:</b><br/><br/>')
print('<table class="checkbox_table">')
for i in range(0, len(filenames)):
	print('<tr><td><input type="checkbox" id="checkbox_' + str(i) + '" checked onclick="hideCol(' + str(i) + ', document.getElementById(\'checkbox_' + str(i) + '\').checked);" /></td><td style="white-space: nowrap;"><b><a href="' + links[i] + '">' + names[i] + '</a></b><td>' + descriptions[i] + '</td></tr>')
print('</table>')

print('<div class="disassembly_container">')
print('<table id="disassembly_table" class="disassembly_table">')

print('<tr>')
print('<th class="left_column">Disassembly</th>')
for i in range(0, files):
	print('<th class="top_row">' + names[i] + '</th>')
print('</tr>')

count = 0
while(True):
	count += 1
#	if count > 80:
#		break
	
	for i in range(0, files):
		if linenumber[i] >= len(data[i]):
			continue
		while len(data[i][linenumber[i]]) > 0 and (data[i][linenumber[i]][0] == '-' or data[i][linenumber[i]][0] == '#'):
			linenumber[i] = linenumber[i] + 1
	
	if asmlinenumber >= len(data[asm_donor_index]):
		break

	asm = data[asm_donor_index][asmlinenumber][0:21].rstrip()
	asmlinenumber = asmlinenumber + 1

	if len(asm) == 0:
		continue
	if asm[0] == '#' or asm[0] == '-':
		continue
	
	has_address = False
	if asm[0] == '$':
		hexaddress = asm[1:5]
		asmaddress = int(hexaddress, 16)
		has_address = True

	symbol = asm[13:19].rstrip()
	asm = asm[:13].rstrip()

	print('<tr>')
	print('<th class="left_column">')
	if has_address:
		print('<a name="' + hexaddress + '"/>')
	print(asm + ' <tt>' + symbol + '</tt>' + '</th>')

	for i in range(0, files):
		print('<td>')
		headings = []
		comments = []
		has_seen_blank_line = False
		while True:
			if linenumber[i] >= len(data[i]):
				break

			line = data[i][linenumber[i]]

			if line.startswith('$'):
				address[i] = int(line[1:5], 16)
			if address[i] > asmaddress:
				break
			comment = line[21:]

			hex_numbers = re.findall(r'\$[0-9A-F][0-9A-F][0-9A-F][0-9A-F]', comment)
			for hex_number in hex_numbers:
				if (hex_number[1] == 'A' or hex_number[1] == 'B' or hex_number[1] == 'E' or hex_number[1] == 'F'):
					comment = comment.replace(hex_number, '<a href="#' + hex_number[1:] + '">' + hex_number + '</a>')

			if not has_seen_blank_line:
				if len(comment.lstrip()) == 0:
					has_seen_blank_line = True
				else:
					headings.append(comment)
			else:
				scomment = comment.lstrip()
				comment = comment + '\n'
				comments.append(comment)

			linenumber[i] += 1

		if len(headings):
			print('<b>')
			all_text = ''
			for heading in headings:
				all_text += heading
			print(markdown.markdown(all_text))
			print('</b><br/>')

		if len(comments):
			all_text = ''
			for comment in comments:
				all_text += comment
			print(markdown.markdown(all_text, extensions=['tables']))
		else:
			print('&nbsp;')

		print('</td>')
	print('</tr>')

print('</table>'
      '</div>'
      '</body>')
