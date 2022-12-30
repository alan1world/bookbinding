#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import re, os, pypandoc, textwrap, argparse, sys, shutil

# bformat = 'md'
btitle = ' '
bauthor = ' '
bdate = ' '
# file_name = 'out.md'

def load_text(myinputfile):
	with open(myinputfile, 'r', encoding='utf-8') as infile:
		mytext = infile.read()
	return mytext

def convert_text(myinputfile):
    mymidtext = pypandoc.convert_file(myinputfile, 'latex')
    myheadtext = textwrap.dedent(r'''    \documentclass[11pt,twoside,openany]{book}
    % A Format paperheight=178mm,paperwidth=110mm
    % B Format paperheight=198mm,paperwidth=130mm
    % Trade Paperback paperheight=216mm,paperwidth=135mm
    % A5 paperheight=210mm,paperwidth=148mm
    \usepackage[paperheight=198mm,paperwidth=130mm,margin=18mm, headsep=5mm]{geometry}
    % \usepackage[paperheight=215mm,paperwidth=135mm,margin=15mm]{geometry}
    % \usepackage[paperheight=185mm,paperwidth=129mm,margin=5mm]{geometry}
    \usepackage[osf]{mathpazo} % to get old-style numbers
    % \usepackage[osf]{libertine} % alternate old-style numbers
    % \usepackage{tgpagella} % Palatino font - modern version
    \usepackage[none]{hyphenat} % turn off hyphenation
    % \usepackage[T1]{fontenc}
    % \usepackage{lmodern}
    \usepackage{amssymb,amsmath}
    \usepackage{float} % provides inline images with {H}
    \usepackage{needspace}% http://ctan.org/pkg/needspace
    \usepackage{sectsty} % centers sections
    \usepackage{array} % to provide multiline tables
    \usepackage{ifxetex,ifluatex}
    \usepackage{fixltx2e} % provides \textsubscript
    \usepackage{fancyhdr} % control over headers and footers
    \usepackage{multicol} % for multicolumns e.g. in the booklist at the start
    \usepackage{enumitem} % for multiline definitions
    % use upquote if available, for straight quotes in verbatim environments
    \IfFileExists{upquote.sty}{\usepackage{upquote}}{}
    \ifnum 0\ifxetex 1\fi\ifluatex 1\fi=0 % if pdftex
      \usepackage[utf8x]{inputenc}
    \else % if luatex or xelatex
      \ifxetex
        \usepackage{mathspec}
        \usepackage{xltxtra,xunicode}
      \else
        \usepackage{fontspec}
      \fi
      \defaultfontfeatures{Mapping=tex-text,Scale=MatchLowercase}
      \newcommand{\euro}{€}
    \fi
    % use microtype if available
    \IfFileExists{microtype.sty}{\usepackage{microtype}}{}
    \usepackage{longtable,booktabs}
    \usepackage{graphicx}
    % Redefine \includegraphics so that, unless explicit options are
    % given, the image width will not exceed the width of the page.
    % Images get their normal width if they fit onto the page, but
    % are scaled down if they would overflow the margins.
    \makeatletter
    \def\ScaleIfNeeded{%
      \ifdim\Gin@nat@width>\linewidth
        \linewidth
      \else
        \Gin@nat@width
      \fi
    }
    \makeatother
    \let\Oldincludegraphics\includegraphics
    {%
     \catcode`\@=11\relax%
     \gdef\includegraphics{\@ifnextchar[{\Oldincludegraphics}{\Oldincludegraphics[width=\ScaleIfNeeded]}}%
    }%
    \ifxetex
      \usepackage[setpagesize=false, % page size defined by xetex
                  unicode=false, % unicode breaks when used with xetex
                  xetex]{hyperref}
    \else
      \usepackage[unicode=true]{hyperref}
    \fi
    \hypersetup{breaklinks=true,
                bookmarks=true,
                pdfauthor={},
                pdftitle={},
                colorlinks=false, % colorlinks=true,
                citecolor=blue,
                urlcolor=blue,
                linkcolor=magenta,
                pdfborder={0 0 0}}
    \urlstyle{same}  % don't use monospace font for urls
    \usepackage{navigator}
    \setlength{\parindent}{0pt}
    \setlength{\parskip}{6pt plus 2pt minus 1pt}
    \setlength{\emergencystretch}{3em}  % prevent overfull lines
    \setcounter{secnumdepth}{0}
    \allsectionsfont{\centering} % from secsty
    \newcolumntype{C}{>{\centering\arraybackslash}m{4.7cm}} % from array
    \newcolumntype{J}{>{\arraybackslash}m{4.7cm}} % from array
    \newcolumntype{L}{>{\hangindent=2ex\raggedright\arraybackslash}b{6.8cm}} % from array
    % L should be 6.4 for a right of 3.1
    \newcolumntype{R}{>{\raggedleft\arraybackslash}p{3.1cm}} % from array
    \newcolumntype{T}{>{\raggedright\arraybackslash}b{3.1cm}} % from array

    \pagestyle{fancy} % apply the fancy header package instead of the default
    \fancyhf{}  % clear the default header and footer
    \renewcommand{\headrulewidth}{0pt} % removes the line between header and text

    \author{}
    \date{}

    \begin{document}
''')

    myendtext = r'\end{document}'
    return myheadtext+mymidtext+myendtext

def reg_section_headers(mytext):
	# convert section headers from paragraph text to centered text
    p = re.compile('paragraph{(\d+)}', re.IGNORECASE)
    mytext = p.sub(r'begin{center}\n\\textbf{\1}\n\\end{center}\n\\vspace{-16pt}\n', mytext)
    # remove the label
    p = re.compile('\\\\label{section-(\d+)}', re.IGNORECASE)
    mytext = p.sub(r'', mytext)
    # Not sure what this cleanup is here for! - Perhaps remove the blank line left by the label removal?
    p = re.compile('\n\n\n', re.MULTILINE)
    mytext = p.sub(r'\n\n', mytext)
    # Change all the section links to actual links
    p = re.compile('\\\\textbf{(\d+)}', re.IGNORECASE)
    mytext = p.sub(r'\\jumplink{section-\1}{\\textbf{\1}}', mytext)
    # The above change will alsout_temp.texo change the section headers, need to convert them to anchors for the above targets
    p = re.compile('begin{center}\n\\\\jumplink{section-(\d+)}{\\\\textbf{(\d+)}}', re.MULTILINE)
    mytext = p.sub(r'begin{center}\n\\anchor{section-\1}\\textbf{\1}', mytext)
    return mytext

def reg_section_headers2(mytext):
    p = re.compile('\\\\textbf{(\d+)}', re.IGNORECASE)
    mytext = p.sub(r'\\jumplink{section-\1}{\\textbf{\1}}', mytext)
    p = re.compile('paragraph{(\d+)}\\\\label{section-(\d+)}', re.IGNORECASE)
    mytext = p.sub(r'begin{center}\n\\anchor{section-\1}\\textbf{\1}\n\end{center}\n\\vspace{-16pt}\n', mytext)
    p = re.compile('\n\n\n', re.MULTILINE)
    mytext = p.sub(r'\n\n', mytext)
    return mytext

def reg_cleanup(mytext):
    p = re.compile(r'\\label{.*$', re.MULTILINE)
    mytext = p.sub(r'', mytext)
    p = re.compile('(\W)luck(\W)', re.IGNORECASE)
    mytext = p.sub(r'\1\\textsc{luck}\2', mytext)
    p = re.compile('(\W)skill(\W)', re.IGNORECASE)
    mytext = p.sub(r'\1\\textsc{skill}\2', mytext)
    p = re.compile('(\W)stamina(\W)', re.IGNORECASE)
    mytext = p.sub(r'\1\\textsc{stamina}\2', mytext)
    # p = re.compile('(\W)trail(\W)', re.IGNORECASE)
    # mytext = p.sub(r'\1\\textsc{trail}\2', mytext)
    return mytext

def cleanup_text(mytext):
    mytext = mytext.replace('[htbp]', '[H]')
    mytext = mytext.replace('\\caption{}\n', '')
    mytext = mytext.replace('\\tightlist\n', '')
    mytext = mytext.replace('\\subbegin{}\n', '')
    mytext = mytext.replace(r'Test Your \textsc{luck}', r'Test your Luck')
    mytext = mytext.replace(r'good \textsc{luck}', r'good luck')
    mytext = mytext.replace(r'Good \textsc{luck}', r'Good luck')
    mytext = mytext.replace(r'\paragraph{1}', '\\begin{center}\n\\anchor{section-1}\\textbf{1}\n\\end{center}\n\\vspace{-16pt}')
    mytext = mytext.replace(r'\end{longtable}', r'\end{tabular}')
    mytext = mytext.replace(r'\begin{longtable}[]{@{}ll@{}}', r'\begin{tabular}{LT}')
    mytext = mytext.replace(r'\begin{longtable}[]{@{}lr@{}}', r'\begin{tabular}{LT}')
    mytext = mytext.replace(r'\begin{longtable}[]{@{}lll@{}}', r'\begin{tabular}{lcc}')
    mytext = mytext.replace(r'\begin{longtable}[]{@{}lcc@{}}', r'\begin{tabular}{lcc}')
    mytext = mytext.replace(r'\begin{longtable}[]{@{}llr@{}}', r'\begin{tabular}{lcc}')
    mytext = mytext.replace(r'\begin{longtable}', r'\begin{tabular}')
    mytext = mytext.replace('\n\\toprule', r'')
    mytext = mytext.replace('\n\\bottomrule', r'')
    mytext = mytext.replace('\n\\endhead', r'')
    mytext = mytext.replace('\n\\midrule', r'')
    mytext = mytext.replace('\\tabularnewline', r'\\')
    return mytext

def add_book_details(mytext, btitled, bauthord, bdated):
    mytext = mytext.replace('title{}', 'title{'+btitled+'}')
    mytext = mytext.replace('author{}', 'author{'+bauthor+'}')
    mytext = mytext.replace('date{}', 'date{'+bdate+'}')
    return mytext

def write_out(mytext, myfinalfile):
	with open(myfinalfile, 'w') as myoutfile:
		myoutfile.write(mytext)
	
def main():
    parser = argparse.ArgumentParser(description='Transform Gamebooks')
    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument('--tex', action='store_true', help="Process a Latex file")
    group.add_argument('--md', action='store_true', help="Process a Markdown file")
    parser.add_argument('-f', '--file_name', default='out.md')
    parser.add_argument('-p', '--image_dir', default='abbyy_files')
    args = parser.parse_args()
    if args.tex == True:
        mytext = load_text(args.file_name)
    else:
        mytext = convert_text(args.file_name)
    # mytext = reg_section_headers2(mytext)
    # mytext = reg_cleanup(mytext)
    # mytext = cleanup_text(mytext)
    mytext = add_book_details(mytext, btitle, bauthor, bdate)
    os.makedirs('latex_working', exist_ok=True)
    # args.image_dir = 'warriorsway_files'
    shutil.copytree(args.image_dir, 'latex_working/'+args.image_dir)
    write_out(mytext, 'latex_working/out.tex')
    # os.rename("out_tempa.tex", "out_tempa_original.tex")
    # os.rename("out_temp1a.tex", "out_tempa.tex")

main()
